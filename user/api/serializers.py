from rest_framework import serializers
from user.otp import send_otp, verify_otp
from user.utils import validate_password
from ..models import (
    CustomUser as User,
    Notification, NotificationSetting,
    Address,
    Transaction,
)
from datetime import datetime, timedelta
import pytz
utc = pytz.UTC



"""" User Registration Serializer."""
class UserRegisterSerializer(serializers.ModelSerializer):
    mobile_number = serializers.CharField()
    class Meta:
        model = User
        fields = ('name', 'email', 'mobile_number', 'fcm_token')
        # extra_kwargs = {
        #     'password': {'write_only': True}
        # }
    
    def validate_mobile_number(self, data):
        users = User.objects.filter(mobile_number=data)
        if users.exists():
            user = users.first()
            if user.is_active:
                raise serializers.ValidationError('Mobile Number already exists.')
            user.delete()
        return data



""" Use in Medicine upload or add by csv data. """
class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
  


class UserVerifyAccountSerializer(serializers.Serializer):
    mobile_number = serializers.CharField()
    otp = serializers.IntegerField()
    
    def validate_mobile_number(self, data):
        try:
            self.user = User.objects.get(mobile_number=data)
            return data
        except User.DoesNotExist:
            raise serializers.ValidationError('User not found.')
    
    def validate_otp(self, data):
        try:
            if self.user:
                user = self.user
            else:
                user = None
        except Exception as e:
            user = None
        if user:
            if verify_otp(user, data):
                return data
        raise serializers.ValidationError("Invalid Otp.")


"""" User Profile Serializer."""
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'image', 'fcm_token')
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['mobile_number'] = instance.mobile_number
        return data



"""" User Info Serializer for other user 
"""
class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'image')



# User Login and Register Serializer
class SendOtpSerializer(serializers.Serializer):
    mobile_number = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)

    def validate_email(self, data):
        try:
            return User.objects.get(email=data)
        except:
            raise serializers.ValidationError("User Does not exits.")
        
    def validate_mobile_number(self, data):
        try:
            user, _created = User.objects.get_or_create(mobile_number=data)
            if user.is_active:
                return user
            else:
                raise serializers.ValidationError("User is not active or deleted plese contact to customer support.")
        except:
            raise serializers.ValidationError("User Does not exits.")




# User Login Serializer
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    mobile_number = serializers.CharField(required=False)
    otp = serializers.CharField()
    fcm_token = serializers.CharField(required=False)

    def validate_email(self, data):
        try:
            qs = User.objects.get(email=data)
            self.user = qs
            return qs
        except:
            raise serializers.ValidationError("No active user found with this email.")

    def validate_mobile_number(self, data):
        try:
            return User.objects.get(mobile_number=data)
        except:
            raise serializers.ValidationError("No active user found.")

    def validate_otp(self, data):
        try:
            mobile_number = self.context['request'].data['mobile_number']
        except:
            mobile_number = None
            
        try:
            email = self.context['request'].data['email']
        except:
            email = None
            
        if mobile_number or email:
            try:
                if mobile_number:
                    user = User.objects.get(mobile_number=mobile_number)
                elif email:
                    user = User.objects.get(email=email)
                if verify_otp(user, data):
                    return data
                else:
                    raise serializers.ValidationError("Invalid otp.")
            except:
                raise serializers.ValidationError("Otp verification failed.")
        raise serializers.ValidationError("Invalid data.")



# User Forget password Serializer
class ForgetPasswordSerializer(serializers.Serializer):
    email = serializers.CharField()

    def validate_email(self, data):
        try:
            qs = User.objects.get(email=data)
            send_otp(qs)
            return data
        except:
            raise serializers.ValidationError("User not found with this email.")



# User Confirm Forget password Serializer
class ConfirmForgetPasswordSerializer(serializers.Serializer):
    email = serializers.CharField()
    new_password = serializers.CharField()
    otp = serializers.CharField()

    def validate_email(self, data):
        try:
            qs = User.objects.get(email=data)
            self.user = qs
            return data
        except:
            self.user = None
            raise serializers.ValidationError("User not found with this email.")
    
    def validate_new_password(self, data):
        if not validate_password(data):
            raise serializers.ValidationError("Use alfanumeric min 6 digit strong password.")
        return data
    
    # def validate_otp(self, data):
    #     user = self.user
    #     if user:
    #         if verify_otp(user, data):
    #             return data
    #     else:
    #         raise serializers.ValidationError("No user to validate otp.")
    #     raise serializers.ValidationError("Invalid otp.")
    
    def validate_otp(self, data):
        try:
            user = self.user
        except Exception as e:
            user = None

        if user and self.verify_otp(user, data):
            return data

        raise serializers.ValidationError("Invalid OTP.")





# Change Password Serializer
class ChangePasswordSerializer(LoginSerializer):
    new_password = serializers.CharField()

    def validate_new_password(self, data):
        try:
            email = self.context['request'].data['email']
        except:
            email = None
        if email:
            user = User.objects.get(email=email)
            if user.check_password(data):
                raise serializers.ValidationError("New password should be different.")
            else:
                return data
        return data



# Wallet History Serializer
class NotificationSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationSetting
        fields = ('push', 'email')



# User Notification Serializer
class UserNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"



# User Address Serializer
class UserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['full_address'] = instance.full_address
        return data
    
    
# User Address Update Serializer
class UserAddressUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        exclude = ('user',)



# Transaction Serializer
class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"



# Get User Auth Token Serializer
class GetUserAuthTokenSerializer(serializers.Serializer):
    whatsapp_token = serializers.CharField(max_length=256)
    mobile_number = serializers.CharField(max_length=12)
    
    def validate_mobile_number(self, data):
        try:
            return User.objects.get(mobile_number=data)
        except:
            raise serializers.ValidationError("User Does not exits.")
    
    def validate_whatsapp_token(self, token):
        if token == "iu&^5v7HysrYUtB&bu":
            return token
        raise serializers.ValidationError("Invailid Token.")
