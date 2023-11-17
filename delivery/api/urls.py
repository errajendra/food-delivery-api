from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import(
    OrderDeliverView, change_order_status
)

router = DefaultRouter()

router.register('order-to-deliver', OrderDeliverView, basename='order-to-deliver-api'),



urlpatterns = [
    path('', include(router.urls)),
    path('change-status/', change_order_status),
]
