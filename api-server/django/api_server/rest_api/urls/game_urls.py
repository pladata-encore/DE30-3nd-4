# game/

from django.urls import path
from rest_api.views.game_views import savegame, leaderboard


urlpatterns = [
    path('savegame/', savegame, name='savegame'),
    path('leaderboard/', leaderboard, name='leaderboard'),
]
