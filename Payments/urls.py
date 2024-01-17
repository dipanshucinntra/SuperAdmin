from django.urls import path
from .views import *

urlpatterns = [
    path('create', create, name="create_payment_history"),
    path('update', update, name='update_payment_history'),
    path('payment_list', payment_list, name='all_payment_history'),
    path('payment_detail', payment_detail, name='payment_history_detail')
]