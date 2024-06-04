# admin/

from django.urls import path
from .admin_views import all_users, all_games, update


urlpatterns = [
    path('users/', all_users, name='all_users'),
    path('games/', all_games, name='all_games'),
    path('update/', update, name='update'),
]
