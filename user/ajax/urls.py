from django.urls import path
from .views import *


urlpatterns = [
    #update user active url
    path('update-user-active/', update_user_active, name='update-user-active-ajax'),
]
