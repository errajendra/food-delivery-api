from django.urls import path
from .views import *


urlpatterns = [
    path('login-user/', singIn, name="login_user"),
    path('index/', index, name="index"),
    path('logout/', logout, name="logout"),
    path('transaction/', transaction, name="transaction"),
    path('setting/', setting, name="setting"),
    path('table/', table, name="table"),
    path('customer-list/', customerList, name="customer_list"),
    path('menu-list/', menuList, name="menu_list"),
    path('subscription-list/', subscriptionList, name="subscription_list"),
]
