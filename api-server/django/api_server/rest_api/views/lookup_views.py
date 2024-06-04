# Views for looking up data

from django.http import JsonResponse
from rest_framework.decorators import api_view

from rest_api.models import User, Game

from rest_api.serializers import IDSerializer, GameSerializer


@api_view(['POST'])
def user(request):
    idSerializer = IDSerializer(data=request.data)
    # 전달 받은 Body가 형식에 올바른지 판단
    # 올바르면,
    if idSerializer.is_valid():
        user_id = idSerializer.validated_data['user_or_game_id']
        # user_id가 DB에 존재하는지 확인
        # 존재하면,
        if User.objects.filter(user_id=user_id).exists():
            # user_id에 해당하는 User 객체 받아오기
            user_data = User.objects.get(user_id=user_id)
            # 반환해줄 User 정보에 대한 JSON data 생성
            responseBody = {
                "name": user_data.name,
                "best_score": user_data.best_score,
                "average_score": user_data.average_score,
                "ranking": user_data.ranking,
                "play_count": user_data.play_count
            }
            # 해당 User의 정보, 200 반환
            return JsonResponse(responseBody, status=200)
        # 존재하지 않으면,
        else:
            # 에러메시지, 409 반환
            return JsonResponse({
                "message": "User does not exist."
            }, status=409)
    # 올바르지 않으면,
    else:
        # 그 외의 error들, 400 반환
        return JsonResponse({
            "message": "Bad Request"
        }, status=400)

@api_view(['POST'])
def game(request):
    idSerializer = IDSerializer(data=request.data)
    # 전달 받은 Body가 형식에 올바른지 판단
    # 올바르면,
    if idSerializer.is_valid():
        game_id = IDSerializer.validated_data['user_or_game_id']
        # game_id가 DB에 존재하는지 확인
        # 존재하면,
        if Game.objects.filter(game_id=game_id).exists():
            # game_id에 해당하는 Game 객체 받아오기
            game_data = Game.objects.get(game_id=game_id)
            # 반환해줄 Game 정보에 대한 JSON data 생성
            responseBody = {
                "user_id": game_data.user_id,
                "when_played": game_data.when_played,
                "kill_count": game_data.kill_count,
                "elapsed_time": game_data.elapsed_time,
                "score": game_data.score
            }
            # 해당 Game의 정보, 200 반환
            return JsonResponse(responseBody, status=200)
        # 존재하지 않으면,
        else:
            # 에러메시지, 409 반환
            return JsonResponse({
                "message": "Game does not exist."
            }, status=409)
    # 올바르지 않으면,
    else:
        # 그 외의 error들, 400 반환
        return JsonResponse({
            "message": "Bad Request"
        }, status=400)


@api_view(['POST'])
def usergames(request):
    idSerializer = IDSerializer(data=request.data)
    # 전달 받은 Body가 형식에 올바른지 판단
    # 올바르면,
    if idSerializer.is_valid():
        user_id = idSerializer.validated_data['user_or_game_id']
        # user_id가 DB에 존재하는지 확인
        # 존재하면,
        if User.objects.filter(user_id=user_id).exists():
            # user_id에 해당하는 Game 객체들 받아오기
            game_data = Game.objects.filter(user_id=user_id)
            # Game 객체들을 List 형태로 직렬화
            gameSerializer = GameSerializer(game_data, many=True)
            # List를 순회하면서,
            for o in gameSerializer.data:
                # user_id 필드 빼주기
                del o['user_id']
            # 해당 User의 Game 정보들, 200 반환
            return JsonResponse(gameSerializer.data, safe=False, status=200)
        # 존재하지 않으면,
        else:
            # 에러메시지, 409 반환
            return JsonResponse({
                "message": "User does not exist."
            }, status=409)
    # 올바르지 않으면,
    else:
        # 그 외의 error들, 400 반환
        return JsonResponse({
            "message": "Bad Request"
        }, status=400)
