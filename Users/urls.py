from django.urls import path
from .views import *

urlpatterns = [
    path('create', create, name="create_user"),
    path('update', update, name='update_user'),
    path('login', login, name='user_login'),
    path('logout', logout, name='logout'),
    path('detail', detail, name='user_detail'),
]