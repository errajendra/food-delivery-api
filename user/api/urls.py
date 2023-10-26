from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserRegisterView, LoginView, ChangePasswordView, user_logout,
    ProfileView,
    UserVerifyAccountView,
    NotificationSettingView, NotificationView,
    ForgetPasswordView, ConfirmForgetPasswordView,
    DeleteUserAccountView,
    UserAddressView,
    TransactionListView,
)

router = DefaultRouter()

""" User Register, Login and Profile Urls. """
router.register('register', UserRegisterView, basename="user-register-api")
router.register('verify-account-with-otp', UserVerifyAccountView,
                basename="verify-account-with-otp")
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

urlpatterns = [
    path('', include(router.urls)),
    path('logout/', user_logout, name='user-logout-api'),
]
