from django.urls import path
from .views import *


urlpatterns = [
    path('create', create, name='industry_add'),
    path('update', update, name='industry_update'),
    path('all', all, name='industry_list'),
]