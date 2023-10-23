from django.contrib import admin
from .models import *

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    
@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'description')
    
@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'description', 'price', 'eating_type',
        'category', 'sub_category'
    )
    
@admin.register(Plan)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'price', 'duration',
        'saving_per_day', 'eating_type', 'tag'
    )
    list_editable = ('tag',)

@admin.register(PlanPurchase)
class MealAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'plan', 'remaining_meals', 'transaction', 'status', 'address'
    )
