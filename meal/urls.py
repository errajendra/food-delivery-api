from django.urls import path, include
from .views import *


urlpatterns = [
    path('api/', include('meal.api.urls')),
    # path('ajax/', include('user.ajax.urls')),
    
    # Category Urls
    path('category-list/', category_list, name='category_list'),
    path('add-category/', category_add, name='add_category'),
    path('edit-category/<int:id>/', category_edit, name='edit_category'),
    
    path('subcategory-list/', subcategory_list, name='subcategory_list'),
    path('add-subcategory/', subcategory_add, name='add_subcategory'),
    path('edit-subcategory/<int:id>/', subcategory_edit, name='edit_subcategory'),
    
    # Meal Urls
    path('meal-list/', meal_list, name='meal_list'),
    path('add-meal/', meal_add, name='add_meal'),
    path('edit-meal/<int:id>/', meal_edit, name='edit_meal'),
]
