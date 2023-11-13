from django.urls import path, include
from .views import *


urlpatterns = [
    
    path('delivery-person-list/', delivery_person_list, name='delivery_person_list'),
    
    path('add-delivery-person/', add_delivery_person, name='add-delivery-person'),
    path('delete-delivery-person/<int:id>/', delete_delivery_person, name='delete-delivery-person'),
    
      
]
