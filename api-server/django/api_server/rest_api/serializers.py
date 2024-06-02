from rest_framework import serializers
from .models import User, Game


# User Model
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'name', 'password', 'best_score', 'average_score', 'ranking', 'play_count']


# Game Model
class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['game_id', 'user_id', 'when_played', 'kill_count', 'elapsed_time', 'score']


# register, login
class InputNamePWSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=20)
    password = serializers.CharField(max_length=20)


# user, game, usergames
class IDSerializer(serializers.Serializer):
    user_or_game_id = serializers.IntegerField()


# update
class AdminSerializer(serializers.Serializer):
    SECRET_KEY = serializers.CharField()
