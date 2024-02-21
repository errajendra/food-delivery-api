from django.contrib import admin
from .models import *


@admin.register(MealType)
class MealTypeAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'description'
    )


@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'meal_type', 'description', 'eating_type'
    )
    list_filter = ('meal_type', 'eating_type')
    search_fields = ('meal_type', 'description', 'eating_type')

 
@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'price', 'number_of_meals',
        'eating_type', 'tag', 'validity'
    )
    list_editable = ('tag',)
    list_filter = ('number_of_meals', 'eating_type', 'tag', 'validity', )


@admin.register(PlanPurchase)
class MealAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'plan', 'remaining_meals', 'total_meals', 'transaction', 'status'
    )
    list_editable = ('remaining_meals', 'status')


@admin.register(MealRequestDaily)
class MealRequestDailyAdmin(admin.ModelAdmin):
    list_display = (
       'id', 'plan', 'meal', 'date', 'address', 'instruction', 'status'
    )
    list_filter = ('meal', 'date', 'status')
    list_editable = ('status',)
    search_fields = ('meal__name', 'address', 'instruction',)


@admin.register(DailyMealMenu)
class DailyMealMenuAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'meal_type', 'eating_type', 'items', 'created_at')
    list_filter = ('date', 'meal_type', 'eating_type', 'created_at')


@admin.register(CustomerSupport)
class CustomerSuportAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'message')
    list_filter = ('status',)


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('id', 'alt', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('alt',)
