from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.db.models import Q
from .serializers import *
from .exceptions import *



# User Registration Api
class UserRegisterView(ModelViewSet):
    serializer_class = UserRegisterSerializer
    # queryset = User.objects.all()
    http_method_names = ('post',)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                data={
                    "status": status.HTTP_200_OK,
                    "message": "Success",
                    "data": serializer.data
                },
                status=200
            )
        errors = serializer.errors
        error_message = ""
        for key in list(errors):
            error_message += f"{errors[key][0]}"
            break
        return Response(
            data={
                "status": status.HTTP_400_BAD_REQUEST,
                "message": error_message,
                "errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )



# User Verify Account with otp after Registration Api View
class UserVerifyAccountView(ModelViewSet):
    serializer_class = UserVerifyAccountSerializer
    http_method_names = ('post',)
    
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(mobile_number=serializer.validated_data['mobile_number'])
            user.is_active = True
            user.save()
            return Response(
                data={
                    "status": status.HTTP_200_OK,
                    "message": "Success",
                },
                status=200
            )
        errors = serializer.errors
        error_message = ""
        for key in list(errors):
            error_message += f"{key} - {errors[key][0]}"
            break
        return Response(
            data={
                "status": status.HTTP_400_BAD_REQUEST,
                "message": error_message,
                "errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )



# Send Otp to User Login Api Views
class SendLoginOtpView(ModelViewSet):
    serializer_class = SendOtpSerializer
    http_method_names = ('post',)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['mobile_number']
            email = serializer.validated_data['email']
            try:
                user.email = email
                user.save()
            except:
                pass
            if send_otp(user):
                return Response(
                    {   'status': status.HTTP_200_OK,
                        'message': "Otp sent.",
                    }
                )
            return Response(
                status = status.HTTP_500_INTERNAL_SERVER_ERROR,
                data = {   
                    'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'message': "Unable to send otp.",
                }
            )
        
        return Response(
            data={
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "User not found.",
                "errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )



# User Login Api Views
class LoginView(ModelViewSet):
    serializer_class = LoginSerializer
    http_method_names = ('post',)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['mobile_number']
            user.fcm_token = serializer.validated_data.get('fcm_token', user.fcm_token)
            user.is_active = True
            user.save()
            token, _created = Token.objects.get_or_create(
                user = user
            )
            return Response(
                {   'status': status.HTTP_200_OK,
                    'message': "Login Success.",
                    'token': token.key,
                    'data': UserProfileSerializer(user).data
                }
            )
        errors = serializer.errors
        error_message = ""
        for key in list(errors):
            error_message += f"{key} - {errors[key][0]}"
            break
        return Response(
            data={
                "status": status.HTTP_400_BAD_REQUEST,
                "message": error_message,
                "errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )



# Delete User account permanentaly Views
class DeleteUserAccountView(ModelViewSet):
    http_method_names = ('post',)
    permission_classes = [IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        user = request.user
        user.is_active = False
        user.save()
        return Response(
            data={
                "status": status.HTTP_204_NO_CONTENT,
                "message": "DELETED"
            },
            status=status.HTTP_204_NO_CONTENT
        )



# Forget User Password Api Views
class ForgetPasswordView(ModelViewSet):
    serializer_class = ForgetPasswordSerializer
    http_method_names = ('post',)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            return Response(
                {   'status': status.HTTP_200_OK,
                    'message': "Otp sent on email, please verify..",
                }
            )
        errors = serializer.errors
        error_message = ""
        for key in list(errors):
            error_message += f"{key} - {errors[key][0]}"
            break
        return Response(
            data={
                "status": status.HTTP_400_BAD_REQUEST,
                "message": error_message,
                "errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )




# Forget User Password Api Views
class ConfirmForgetPasswordView(ModelViewSet):
    serializer_class = ConfirmForgetPasswordSerializer
    http_method_names = ('post',)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(email=serializer.validated_data['email'])
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response(
                {   'status': status.HTTP_200_OK,
                    'message': "OK",
                }
            )
        errors = serializer.errors
        error_message = ""
        for key in list(errors):
            error_message += f"{key} - {errors[key][0]}"
            break
        return Response(
            data={
                "status": status.HTTP_400_BAD_REQUEST,
                "message": error_message,
                "errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )



# User Change Password
class ChangePasswordView(ModelViewSet):
    serializer_class = ChangePasswordSerializer
    http_method_names = ('post',)
    permission_classes = (IsAuthenticated,)
    
    def create(self, request, *args, **kwargs):
        user = request.user
        email = user.email
        try:
            request.data['email'] = email
        except:
            request.data._mutable = True
            request.data['email'] = email
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            try:
                request.user.auth_token.delete()
            except:
                pass
            return Response(
                {   'status': status.HTTP_200_OK,
                    'message': "Success.",
                }
            )
        errors = serializer.errors
        error_message = ""
        for key in list(errors):
            error_message += f"{key} - {errors[key][0]}"
            break
        return Response(
            data={
                "status": status.HTTP_400_BAD_REQUEST,
                "message": error_message,
                "errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )



# User logout api view - here we delete user auth token
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    if request.method == 'POST':
        try:
            # Delete the user's token to logout
            request.user.auth_token.delete()
            return Response({'status': 200, 'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': 500, 'errors': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



""" User Profile View. """
class ProfileView(ModelViewSet):
    http_method_names = ('get', 'post')
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer
    
    def get_queryset(self):
        return User.objects.get(id=self.request.user.id)
    
    def get_object(self):
        return User.objects.get(id=self.request.user.id)

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            instance = request.user,
            data = request.data
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                data={
                    "status": status.HTTP_200_OK,
                    "message": "OK",
                }
            )
        return Response(
            status = status.HTTP_400_BAD_REQUEST,
            data={
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "BAD REQUEST",
                "errors": serializer.errors
            }
        )



"""
    Notification Setting View.
"""
class NotificationSettingView(ModelViewSet):
    http_method_names = ('get', 'post')
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSettingSerializer
    
    def get_queryset(self):
        try:
            return NotificationSetting.objects.get(user=self.request.user)
        except NotificationSetting.DoesNotExist:
            return NotificationSetting.objects.create(user=self.request.user)
    
    def get_object(self):
        return NotificationSetting.objects.get(id=self.request.user.id)

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            instance = self.get_object(),
            data = request.data
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                data={
                    "status": status.HTTP_200_OK,
                    "message": "OK",
                }
            )
        return Response(
            status = status.HTTP_400_BAD_REQUEST,
            data={
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "BAD REQUEST",
                "errors": serializer.errors
            }
        )



"""
    User Notification List View.
"""
class NotificationView(ModelViewSet):
    http_method_names = ("get",)
    permission_classes = [IsAuthenticated]
    serializer_class = UserNotificationSerializer
    
    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)



""" User Address View. """
class UserAddressView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserAddressSerializer
    
    
    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)
    
    
    def create(self, request, *args, **kwargs):
        user = request.user
        try:
            request.data['user'] = user.id
        except:
            request.data._mutable = True
            request.data['user'] = user.id
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "status": 200,
                    "message": "OK",
                    "data": serializer.data
                }
            )
        return Response(
            {
                "status": 400,
                "message": "BAD REQUEST",
                "errors": serializer.errors
            }
        )
    
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = UserAddressUpdateSerializer(
            instance=instance, data=request.data
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "status": 200,
                    "message": "OK",
                    "data": serializer.data
                }
            )
        return Response(
            {
                "status": 400,
                "message": "BAD REQUEST",
                "errors": serializer.errors
            }
        )



""" Transaction List View. """
class TransactionListView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    http_method_names = ('get',)
    serializer_class = TransactionSerializer
    
    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)
