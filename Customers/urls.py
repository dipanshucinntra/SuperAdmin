from django.urls import path
from .views import *


urlpatterns = [
    path('create', create, name='customer_create'),
    path('customers', customer_list, name='customer_list'),
    path('customers/<int:pk>', customer_detail, name='customer_detail'), 
    path('add_employee', add_employee, name='add_employee'), 
    path('update_employee', update_employee, name='update_employee'), 
]
