from django.urls import path
from .views import *


urlpatterns = [
    path('create', create, name='customer_create'),
    path('update', update, name='customer_update'),
    path('detail', detail, name='customer_detail'),
    path('all', all, name='customer_all'),    
    path('add_employee', add_employee, name='add_employee'), 
    path('update_employee', update_employee, name='update_employee'), 
    path('all_emp_per_customer', all_emp_per_customer, name='all_emp_per_customer'), 

    ################ VARUN URLS #######################################
    path('customers', customer_list, name='customer_list'),
    path('customers/<int:pk>', customer_detail, name='customer_detail'), 
]
