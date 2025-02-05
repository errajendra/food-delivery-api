from django.contrib import admin
from django.urls import path, include
from user.utils import render_index_page
from django.conf import settings
from django.conf.urls.static import static
from .constance_config_view import update_confi_setting

admin.site.site_header = 'Food Delivery (ATM) Adminsitration'
admin.site.index_title = ''
admin.site.site_title = 'ATM - Food Delivery Admin'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include("user.urls")),
    path('meal/', include("meal.urls")),
    path('payment/', include("razor_pay.urls")),
    path('delivery/', include("delivery.urls")),
    path('update-constance-setting/', update_confi_setting, name="update-constance"),
    path("", render_index_page),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
