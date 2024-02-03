from django.urls import path, include
from .views import *


urlpatterns = [
    path('api/', include('meal.api.urls')),
    # path('ajax/', include('user.ajax.urls')),
    
    # Meal Urls
    path('meal-list/', meal_list, name='meal_list'),
    path('add-meal/', meal_add, name='add_meal'),
    path('edit-meal/<int:id>/', meal_edit, name='edit_meal'),
    path('delete-meal/<int:id>/', meal_delete, name='delete_meal'),
    
    # Plan Urls
    path('plan-list/', plan_list, name='plan_list'),
    path('add-plan/', plan_add, name='add_plan'),
    path('edit-plan/<int:id>/', plan_edit, name='edit_plan'),
    path('delete-plan/<int:id>/', plan_delete, name='delete_plan'),
    
    path('plan-purchase-list/', plan_purchase_list, name='plan_purchase_list'),
    
    path('daily-meal-request-list/', daily_meal_request_list, name='daily_meal_request_list'),
    path('add-daily-meal/', add_daily_meal, name='add_daily_meal'),
    
    path('transaction-list/', transaction_list, name='transaction_list'),
    
    path('update-delivery-person/', update_delivery_person, name='update_delivery_person'),
    
    path('get-delivery-person-list-popup/', get_delivery_person_list_popup, name='get_delivery_person_list_popup'),
    
    # Daily Meal Menu Urls
    path('daily-meal-menu-list/', daily_meal_menu_list, name='daily_meal_menu_list'),
    path('add-daily-meal-menu/', add_daily_meal_menu, name='add_daily_meal_menu'),
    path('edit-daily-meal-menu/<int:id>/', daily_meal_menu_edit, name='edit_daily_meal_menu'),
    path('delete-daily-meal-menu/<int:id>/', daily_meal_menu_delete, name='delete_daily_meal_menu'),
    
    
]
