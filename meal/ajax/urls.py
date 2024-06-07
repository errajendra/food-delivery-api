from django.urls import path
from .views import *


urlpatterns = [
    #update help active url
    path('update-help-active/', update_help_active, name='update-help-active-ajax'),
    path("update-plan-active-ajax/", update_plan_active_ajax, name="update_plan_active_ajax")
    
]

