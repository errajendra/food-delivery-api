from django.urls import path
from .views import verify_payment

urlpatterns = [
    path('check-payment/', verify_payment, name='verify-payment-api'),
]
