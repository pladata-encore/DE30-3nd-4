# auth/

from django.urls import path
from rest_api.views.auth_views import register, login


urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
]
