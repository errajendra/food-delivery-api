from django.contrib import admin
from .models import *


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'wallet_amount', 'date_joined', 'is_active')
    list_editable = ('is_active',)
    
    @admin.display(empty_value="0")
    def wallet_amount(self, obj):
        return obj.wallet_amount

@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('user', 't_type', 'coins', 'status', 'remark')
