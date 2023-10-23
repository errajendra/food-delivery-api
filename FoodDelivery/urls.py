from django.contrib import admin
from django.urls import path, include
from user.utils import render_index_page
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = 'Food Delivery Adminsitration'
admin.site.index_title = ''
admin.site.site_title = 'Food Delivery Admin'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include("user.urls")),
    path('meal/', include("meal.urls")),
    path('payment/', include("cc_avenue.urls")),
    path("", render_index_page),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
