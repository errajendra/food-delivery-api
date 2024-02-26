from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserRegisterView, SendLoginOtpView, LoginView, ChangePasswordView, user_logout,
    ProfileView,
    UserVerifyAccountView,
    NotificationSettingView, NotificationView,
    ForgetPasswordView, ConfirmForgetPasswordView,
    DeleteUserAccountView,
    UserAddressView,
    TransactionListView,
    UserAddByFile,
    UserMealPlanPurcheseAddByFile,
)

router = DefaultRouter()

""" User Register, Login and Profile Urls. """
router.register('register', UserRegisterView, basename="user-register-api") # Not Using
router.register('verify-account-with-otp', UserVerifyAccountView,
                basename="verify-account-with-otp") # Not Using
router.register('send-login-otp', SendLoginOtpView, basename="send-login-otp-api")
router.register('login', LoginView, basename="user-login-api")
router.register('delete-account-permanentaly',
                DeleteUserAccountView, basename="delete-account-permanentaly")
router.register('profile', ProfileView, basename="user-profile-api")
router.register('change-password', ChangePasswordView,
                basename="user-change-password-api")
router.register('forget-password', ForgetPasswordView,
                basename="user-forget-password-api")
router.register('confirm-forget-password', ConfirmForgetPasswordView,
                basename="user-confirm-forget-password-api")
router.register(
    'user-address', UserAddressView, basename="uaser-address-api"
)

""" Wallete or Coins URLs"""
router.register('notification-setting', NotificationSettingView,
                basename="notification-setting-api")
router.register('notification', NotificationView,
                basename="notification-api")

""" Transactions Url"""
router.register('transactions', TransactionListView, 
                basename="user-transaction-list-api")

# Upload User by CSV
router.register('user-upload', UserAddByFile, basename="user-upload")
router.register('user-meal-plan-upload',
                UserMealPlanPurcheseAddByFile, basename="user-meal-plan-upload")


urlpatterns = [
    path('', include(router.urls)),
    path('logout/', user_logout, name='user-logout-api'),
]
