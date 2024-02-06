from django.urls import path
from .views import *


urlpatterns = [
    #update help active url
    path('update-help-active/', update_help_active, name='update-help-active-ajax'),
    
    
]

