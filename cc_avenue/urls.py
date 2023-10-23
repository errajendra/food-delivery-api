from django.urls import path
from .response_handler import payment_verify, payment_cancel


urlpatterns = [
    path('check/', payment_verify, name='check-cc-payment'),
    path('cancel/', payment_cancel, name='cancel-cc-payment'),
]
