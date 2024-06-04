# lookup/

from django.urls import path
from .lookup_views import user, game, usergames


urlpatterns = [
    path('user/', user, name='user'),
    path('game/', game, name='game'),
    path('usergames/', usergames, name='usergames'),
]
