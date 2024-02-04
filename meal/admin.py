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
        'name', 'description', 'plan', 'eating_type'
    )

 
@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'price', 'number_of_meals',
        'eating_type', 'tag', 'validity'
    )
    list_editable = ('tag',)


@admin.register(PlanPurchase)
class MealAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'plan', 'remaining_meals', 'total_meals', 'transaction', 'status'
    )
    list_editable = ('remaining_meals', 'status')


@admin.register(MealRequestDaily)
class MealRequestDailyAdmin(admin.ModelAdmin):
    list_display = (
       'id', 'plan', 'meal', 'date', 'delivery_person', 'status'
    )


@admin.register(DailyMealMenu)
class DailyMealMenuAdmin(admin.ModelAdmin):
    list_display = ('date', 'id', 'created_at')
