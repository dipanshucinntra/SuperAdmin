from django.urls import path
from .views import *

urlpatterns = [
    path('create', create, name='application_add'),
    path('update', update, name='application_update'),
    path('all', all, name='application_list'),
]