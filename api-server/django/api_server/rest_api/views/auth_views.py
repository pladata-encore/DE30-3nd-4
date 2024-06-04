# Views for authorization

from django.http import JsonResponse
from rest_framework.decorators import api_view

from rest_api.models import User

from rest_api.serializers import InputNamePWSerializer, UserSerializer


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
