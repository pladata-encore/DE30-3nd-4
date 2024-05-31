from django.urls import path
from . import views

urlpatterns = [
    path('user/', views.user_list, name='user-list'),
    path('game/', views.game_list, name='game-list'),
]
