from rest_framework import serializers
from .models import User, Game


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'name', 'password', 'best_score', 'average_score', 'ranking', 'play_count']


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['game_id', 'user_id', 'when_played', 'kill_count', 'elapsed_time', 'score']
