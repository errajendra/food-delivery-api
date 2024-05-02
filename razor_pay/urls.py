from django.urls import path
from .views import verify_payment, verify_payment_link_signature

urlpatterns = [
    path('check-payment/', verify_payment, name='verify-payment-api'),
    path('check-payment-by-link/', verify_payment_link_signature, name='verify-payment-api-by-link'),
]
