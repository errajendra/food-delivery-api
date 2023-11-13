from django.contrib import admin
from .models import *


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'date_joined', 'is_active', 'is_delivery_person')
    list_editable = ('is_active', 'is_delivery_person')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title', 'description', 'seen')
    list_editable = ('seen',)


@admin.register(NotificationSetting)
class NotificationSettingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'email', 'push')
    list_editable = ('email', 'push')


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'city', 'state', 'zip')


@admin.register(Transaction)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'amount', 'tracking_id', 'status')
