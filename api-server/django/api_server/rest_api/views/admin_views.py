# Views for admin

from django.http import JsonResponse
from rest_framework.decorators import api_view

from rest_api.models import User, Game

from rest_api.serializers import UserSerializer, GameSerializer, AdminSerializer

from rest_api.modules.update_ranking import update_ranking


@api_view(['GET'])
def all_users(request):
    try:
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return JsonResponse(serializer.data, safe=False, status=200)
    except Exception as e:
        # 예외 발생 error 메시지, 400 반환
        return JsonResponse({
            "message": str(e)
        }, status=400)


@api_view(['GET'])
def all_games(request):
    try:
        games = Game.objects.all()
        serializer = GameSerializer(games, many=True)
        return JsonResponse(serializer.data, safe=False, status=200)
    except Exception as e:
        # 예외 발생 error 메시지, 400 반환
        return JsonResponse({
            "message": str(e)
        }, status=400)


@api_view(['POST'])
def update(request):
    # 관리자 식별용 key
    SECRET_KEY = "7276"
    adminSerializer = AdminSerializer(data=request.data)
    # 전달 받은 Body가 형식에 올바른지 판단
    # 올바르면,
    if adminSerializer.is_valid():
        # 관리자 신원인지 확인
        # 관리자가 맞으면,
        if SECRET_KEY == adminSerializer.data['SECRET_KEY']:
            # 전체 User를 순회하면서 각 User의 기록을 게임 로그들에 맞게 최신화
            users = User.objects.all()
            for u in users:
                # 플레이 카운트 갱신
                u.play_count = Game.objects.filter(user_id=u.user_id).count()
                # 게임 기록이 존재하는지 판단
                # 존재하면,
                if u.play_count > 0:
                    # 최고 점수 갱신
                    u.best_score = Game.objects.filter(user_id=u.user_id).aggregate(Max('score'))['score__max']
                    # 평균 점수 갱신
                    u.average_score = Game.objects.filter(user_id=u.user_id).aggregate(Avg('score'))['score__avg']
                # 존재하지 않으면,
                else:
                    # 0으로 저장
                    u.best_score = 0
                    u.average_score = 0
                # 유저 정보 저장
                u.save()
            # 최신화한 정보를 바탕으로 ranking 최신화
            update_ranking()
            # 성공메시지, 200 반환
            return JsonResponse({
                "message": "Update database"
            }, status=200)
        # 관리자가 아니면,
        else:
            # 에러메시지, 403 반환
            return JsonResponse({
                "message": "Incorrect password."
            }, status=403)
    # 올바르지 않으면,
    else:
        return JsonResponse({
            "message": "Bad Request"
        }, status=400)
