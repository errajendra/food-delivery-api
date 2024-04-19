from django.urls import path, include
from .views import *


urlpatterns = [
    path('api/', include('meal.api.urls')),
    path('ajax/', include('meal.ajax.urls')),
    
    # MealType Urls
    path('meal-type-list/', meal_type_list, name='meal_type_list'),
    path('add-meal-type/', meal_type_add, name='add_meal_type'),
    path('edit-meal-type/<int:id>/', meal_type_edit, name='edit_meal_type'),
    path('delete-meal-type/<int:id>/', meal_type_delete, name='delete_meal_type'),
    
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
    
    # Plan Puchese Urls
    path('add-plan-purchese/', plan_purchese_add, name='add_plan_purchese'),
    path('plan-purchase-list/', plan_purchase_list, name='plan_purchase_list'),
    
    path('daily-meal-request-list/', daily_meal_request_list, name='daily_meal_request_list'),
    path('add-daily-meal/', add_daily_meal, name='add_daily_meal'),
    path('update-daily-meal/<int:id>/', update_daily_meal, name='update_daily_meal'),
    
    path('transaction-list/', transaction_list, name='transaction_list'),
    
    path('update-delivery-person/', update_delivery_person, name='update_delivery_person'),
    
    path('get-delivery-person-list-popup/', get_delivery_person_list_popup, name='get_delivery_person_list_popup'),
    
    # Daily Meal Menu Urls
    path('daily-meal-menu-list/', daily_meal_menu_list, name='daily_meal_menu_list'),
    path('add-daily-meal-menu/', add_daily_meal_menu, name='add_daily_meal_menu'),
    path('edit-daily-meal-menu/<int:id>/', daily_meal_menu_edit, name='edit_daily_meal_menu'),
    path('delete-daily-meal-menu/<int:id>/', daily_meal_menu_delete, name='delete_daily_meal_menu'),
    
    # Banner Urls
    path('banner-list/', banner_list, name='banner_list'),
    path('add-banner/', add_banner, name='add_banner'),
    path('edit-banner/<int:id>/', banner_edit, name='edit_banner'),
    path('delete-banner/<int:id>/', banner_delete, name='delete_banner'),
    
    # coupan Urls
    path('coupan-list/', coupan_list, name='coupan_list'),
    path('add-coupan/', add_coupan, name='add_coupan'),
    path('edit-coupan/<int:id>/', coupan_edit, name='edit_coupan'),
    path('delete-coupan/<int:id>/', coupan_delete, name='delete_coupan'),
    
    # Sales Connect Urls
    path('sales-connect-list/', sales_connect_list, name='sales_connect_list'),
    path('edit-sales-connect/<int:id>/', sales_connect_edit, name='edit_sales_connect'),
    path('delete-sales-connect/<int:id>/', sales_connect_delete, name='delete_sales_connect'),
    
    
    # Kitchen Off Urls
    path('add-kitchen-off/', add_kitchen_off, name='add_kitchen_off'),
    path('kitchen-off-list/', kitchen_off_list, name='kitchen_off_list'),
    path('edit-kitchen-off/<int:id>/', kitchen_off_edit, name='edit_kitchen_off'),
    path('delete-kitchen-off/<int:id>/', kitchen_off_delete, name='delete_kitchen_off'),
    
    # Support Urls
    path('supports/', supprt_list, name="supports"),
    
    # Master Data 
    path("masterdata/", master_data, name='masterdata'),
    
    
]
