from django.db.models import Max, Avg
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .models import User, Game
from .serializers import UserSerializer, GameSerializer, \
    InputNamePWSerializer, IDSerializer, \
    AdminSerializer


# Function: 전체 user의 ranking 갱신
def update_ranking():
    users = User.objects.order_by('-best_score')

    for rank, user in enumerate(users, start=1):
        user.ranking = rank
        user.save()


# Create your views here.
@api_view(['POST'])
def register(request):
    inputNamePWSerializer = InputNamePWSerializer(data=request.data)
    # 전달 받은 Body가 형식에 올바른지 판단
    # 올바르면,
    if inputNamePWSerializer.is_valid():
        input_name = inputNamePWSerializer.validated_data['name']
        input_password = inputNamePWSerializer.validated_data['password']
        # ID가 DB에 이미 존재 하는지 판단
        # 존재하지 않으면,
        if not User.objects.filter(name=input_name).exists():
            # 새 User의 JSON data 생성
            new_user_JSON_data = {
                "name": input_name,
                "password": input_password,
                "best_score": 0,
                "average_score": 0,
                "play_count": 0
            }
            # JSON -> User django model 직렬화
            userSerializer = UserSerializer(data=new_user_JSON_data)
            # DB에 저장
            userSerializer.save()
            # 새로운 User가 부여 받은 user_id, 코드 200 반환
            new_user = User.objects.get(name=input_name)
            new_user_id = new_user.user_id
            responseBody = {
                "user_id": new_user_id
            }
            return JsonResponse(responseBody, status=200)
        # 존재하면,
        else:
            # 에러메시지, 409 반환
            return JsonResponse({
                "message": "The ID already exists."
            }, status=409)
    # 올바르지 않으면,
    else:
        # 입력한 ID 혹은 password가 비어있거나 20자를 초과, 410 반환
        if len(request.data['name']) > 20 or len(request.data['name']) == 0 or \
                len(request.data['password']) > 20 or len(request.data['password']) == 0:
            return JsonResponse({
                "message": "Input is empty or exceeded 20 characters."
            }, status=410)
        # 그 외의 error들, 400 반환
        else:
            return JsonResponse({
                "message": "Bad Request"
            }, status=400)


@api_view(['POST'])
def login(request):
    inputNamePWSerializer = InputNamePWSerializer(data=request.data)
    # 전달 받은 Body가 형식에 올바른지 판단
    # 올바르면,
    if inputNamePWSerializer.is_valid():
        input_name = inputNamePWSerializer.validated_data['name']
        input_password = inputNamePWSerializer.validated_data['password']
        # ID가 DB에 존재하는지 판단
        # 존재하면,
        if User.objects.filter(name=input_name).exists():
            # ID에 해당하는 User 객체 받아오기
            user = User.objects.get(name=input_name)
            # ID에 해당하는 password와 입력받은 password가 일치하는지 판단
            # 일치하면,
            if input_password == user.password:
                # 해당 User의 user_id, 200 반환
                responseBody = {
                    "user_id": user.user_id
                }
                return JsonResponse(responseBody, status=200)
            # 일치하지 않으면,
            else:
                # 에러메시지, 403 반환
                return JsonResponse({
                    "message": "Incoreect password."
                }, status=403)
        # 존재하지 않으면,
        else:
            # 에러메시지, 409 반환
            return JsonResponse({
                "message": "ID does not exist."
            }, status=409)
    # 올바르지 않으면,
    else:
        # 입력한 ID 혹은 password가 비어있거나 20자를 초과, 410 반환
        if len(request.data['name']) > 20 or len(request.data['name']) == 0 or \
                len(request.data['password']) > 20 or len(request.data['password']) == 0:
            return JsonResponse({
                "message": "Input is empty or exceeded 20 characters."
            }, status=410)
        # 그 외의 error들, 400 반환
        else:
            return JsonResponse({
                "message": "Bad Request"
            }, status=400)


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
