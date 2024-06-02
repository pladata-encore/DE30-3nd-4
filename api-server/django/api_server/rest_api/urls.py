from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register),
    path('login/', views.login),
    path('user/', views.user),
    path('game/', views.game),
    path('usergames/', views.usergames),
    path('leaderboard/', views.leaderboard),
    path('savegame/', views.savegame),

    path('users/', views.all_users),
    path('games/', views.all_games),
    path('update/', views.update),

]
