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
        'name', 'description', 'price', 'eating_type'
        
    )
    
@admin.register(Plan)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'price', 'duration',
        'eating_type', 'tag', 'validity'
    )
    list_editable = ('tag',)

@admin.register(PlanPurchase)
class MealAdmin(admin.ModelAdmin):
    def max_meals(self, instance):
        return instance.plan.duration
    
    list_display = (
        'user', 'plan', 'remaining_meals', 'max_meals', 'transaction', 'status', 'address'
    )
    list_editable = ('remaining_meals', 'status', 'address')

@admin.register(MealRequestDaily)
class MealRequestDailyAdmin(admin.ModelAdmin):
    list_display = (
       'id', 'plan', 'meal', 'date', 'delivery_person', 'status'
    )
    
@admin.register(DailyMealMenu)
class DailyMealMenuAdmin(admin.ModelAdmin):
    list_display = ('date', 'id', 'created_at')
