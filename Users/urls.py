from django.urls import path
from .views import *

urlpatterns = [
    path('create', create, name="create_user"),
    path('update', update, name='update_user'),
    path('login', login, name='user_login'),
    path('logout', logout, name='logout'),
    path('detail', detail, name='user_detail'),
    path('change_password', password_change, name='change_password'),
    path('forgot_password_link', forgot_password_link, name='forgot_password_link'),
    path('forgot_password/<uid>/<token>', forgot_password, name='forgot_password'),
    path('application_add', application_create, name='application_add')
]