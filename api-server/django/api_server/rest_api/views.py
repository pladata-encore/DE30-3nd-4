from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User, Game
from .serializers import UserSerializer, GameSerializer

# Create your views here.


@api_view(['GET'])
def user_list(request):
    if request.method == 'GET':
        users = User.objects.all()
        print(users)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def game_list(request):
    if request.method == 'GET':
        games = Game.objects.all()
        print(games)
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)
