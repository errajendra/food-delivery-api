from django.contrib import admin
from .models import *


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'mobile_number', 'name', 'date_joined', 'is_active', 'is_delivery_person', 'is_cook')
    list_editable = ('is_active', 'is_delivery_person')
    list_filter = ('date_joined', 'is_active', 'is_delivery_person', 'is_cook')
    search_fields = ('mobile_number', 'name', 'email')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title', 'description', 'seen')
    list_editable = ('seen',)
    list_filter = ('seen',)


@admin.register(NotificationSetting)
class NotificationSettingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'email', 'push')
    list_editable = ('email', 'push')


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'type', 'city', 'state', 'zip', 'latitude', 'longitude')
    search_fields = ('city', 'state', 'user__mobile_number', 'user__name', 'user__email')
    list_filter = ('type', )


@admin.register(Transaction)
class AddressAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'amount', 'tracking_id', 'discount_code', 'discount_amount',
        'status'
    )
    list_filter = ('status', 'created_at')
    search_fields = ('tracking_id',)
