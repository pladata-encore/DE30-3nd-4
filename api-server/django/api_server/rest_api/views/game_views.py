# Views for game play

from django.http import JsonResponse
from rest_framework.decorators import api_view

from rest_api.models import User, Game

from rest_api.serializers import GameSerializer

from rest_api.modules.update_ranking import update_ranking


@api_view(['POST'])
def savegame(request):
    gameSerializer = GameSerializer(data=request.data)
    # 전달 받은 Body가 형식에 올바른지 판단
    # 올바르면,
    if gameSerializer.is_valid():
        # DB에 저장
        gameSerializer.save()
        # 전달 받은 Body로부터 user_id 추출
        user_id = gameSerializer.data['user_id']
        # user_id에 해당하는 User 객체 받아오기
        user_data = User.objects.get(user_id=user_id)
        # 해당 유저의 play_count 갱신
        # Game 로그 수로 play_count 설정
        user_data.play_count = Game.objects.filter(user_id=user_id).count()
        # 해당 유저의 best_score 갱신
        user_data.best_score = Game.objects.filter(user_id=user_id).aggregate(Max('score'))['score__max']
        # 평균 점수 계산 (이전 평균 값은 무시하고 새로 계산)
        total_score = sum(game_data.score for game_data in Game.objects.filter(user_id=user_id))
        # 해당 유저의 average_score 갱신
        user_data.average_score = total_score / user_data.play_count
        # 유저 정보 저장
        user_data.save()
        # 각 User의 랭킹을 update
        update_ranking()
        # 성공메시지, 200 반환
        return JsonResponse({
            "message": "Game log added, User game statistics and Entire user's rankings updated successfully."
        }, status=200)
    # 올바르지 않으면,
    else:
        return JsonResponse({
            "message": "Bad Request"
        }, status=400)


@api_view(['GET'])
def leaderboard(request):
    try:
        # 전달 받은 Query로부터 출력할 상위 User수 받아오기
        n = int(request.GET.get('n', 10))
        # 전체 User수 구하기
        total_users = User.objects.count()
        # n이 전체 User 수보다 큰지 판단
        if n > total_users:
            # 크면, n을 전체 User 수로 바꾸기
            n = total_users
        # User 중 ranking 기준으로 상위 n명을 가져오기
        top_users = User.objects.order_by('ranking')[:n]
        # 필요한 필드들만 직렬화
        leaderboard_data = [
            {
                'name': u.name,
                'best_score': u.best_score,
                'average_score': u.average_score,
                'ranking': u.ranking,
                'play_count': u.play_count
            } for u in top_users
        ]
        # 상위 n명의 leaderboard, 200 반환
        return JsonResponse(leaderboard_data, safe=False, status=200)
    # 예외 발생 시,
    except Exception as e:
        # 예외 발생 error 메시지, 400 반환
        return JsonResponse({
            "message": str(e)
        }, status=400)
