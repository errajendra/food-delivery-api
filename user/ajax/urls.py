from django.urls import path
from .views import *


urlpatterns = [
    #update user active url
    path('update-user-active/', update_user_active, name='update-user-active-ajax'),
    path('update-plan-purchase-active/', update_plan_purchase_active, name='update-plan-purchase-active-ajax'),
    
    path('update-meal-active-ajax/', update_meal_active_ajax, name='update-meal-active-ajax'),
    
    
]

