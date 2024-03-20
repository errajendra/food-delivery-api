from django.urls import path, include
from .views import *


urlpatterns = [
    path('api/', include('user.api.urls')),
    path('ajax/', include('user.ajax.urls')),
    path('dashbord/', index, name='index'),
    path('login/', admin_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('profile/', user_profile, name='profile'),
    
    # User MS
    path('add-user/', user_add, name='add_user'),
    path('users/', user_list, name='users'),
    path('user/<int:id>/', user_edit, name='edit_user'),
]

