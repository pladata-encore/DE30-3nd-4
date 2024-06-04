# auth/

from django.urls import path
from rest_api.views.auth_views import register, login, withdrawal


urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('withdrawal/', withdrawal, name='withdrawal'),
]
