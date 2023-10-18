from rest_framework import serializers
from user.otp import send_otp, verify_otp
from user.utils import validate_password
from django.db.models import Q
from ..models import (
    CustomUser as User,
    Wallet, Notification, NotificationSetting,
)
from datetime import datetime, timedelta
import pytz
utc = pytz.UTC



"""" User Registration Serializer."""
class UserRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    class Meta:
        model = User
        fields = ('name', 'email', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def validate_email(self, data):
        users = User.objects.filter(email=data)
        if users.exists():
            user = users.first()
            if user.is_active:
                raise serializers.ValidationError('Email already exists.')
            user.delete()
        return data



"""" User Verify Account with otp Serializer."""
class UserVerifyAccountSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.IntegerField()
    
    def validate_email(self, data):
        try:
            user = User.objects.get(email=data)
            self.user = user
            return data
        except:
            self.user = None
        raise serializers.ValidationError('User not fount.')
    
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
        fields = ('name', 'mobile_number', 'image')
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['email'] = instance.email
        return data



"""" User Info Serializer for other user 
"""
class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'image')



# User Login Serializer
class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate_email(self, data):
        try:
            qs = User.objects.get(email=data, is_active=True)
            return data
        except:
            raise serializers.ValidationError("No active user found with this email.")

    def validate_password(self, data):
        try:
            mob = self.context['request'].data['email']
        except:
            mob = None
        if mob:
            try:
                user = User.objects.get(email=mob)
                if user.check_password(data):
                    return data
            except:
                pass
        raise serializers.ValidationError("Invalid password.")



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
    
    def validate_otp(self, data):
        user = self.user
        if user:
            if verify_otp(user, data):
                return data
        else:
            raise serializers.ValidationError("No user to validate otp.")
        raise serializers.ValidationError("Invalid otp.")



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
class WalletHistrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = '__all__'



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
