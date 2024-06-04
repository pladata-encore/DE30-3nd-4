import os
from datetime import timedelta

import pandas as pd
from django.http import JsonResponse
from pycaret.time_series import *
from rest_framework.decorators import api_view
from rest_framework.response import Response

from ml_server import settings
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


# # 날짜 변형 함수 (when_played 시간을 30분대로 변형)
# def round_to_nearest_minutes(dt):
#     dt = pd.to_datetime(dt)
#     # Calculate the minute remainder when divided by 60 (15 * 4)
#     minute_remainder = dt.minute % 60
#     # Determine the rounding threshold based on the remainder
#     if minute_remainder >= 45:
#         dt += timedelta(hours=1)
#         dt = dt.replace(minute=0, second=0, microsecond=0)
#     elif minute_remainder >= 15:
#         dt = dt.replace(minute=30, second=0, microsecond=0)
#     else:
#         dt = dt.replace(minute=0, second=0, microsecond=0)
#     return dt


def preprocess_newdata(data):
    df = pd.DataFrame(data)
    print(df)
    df = df[['when_played', 'elapsed_time', 'kill_count']]
    df = df.sort_values(by='when_played')
    # print(df)
    df['when_played'] = pd.to_datetime(df['when_played']).dt.strftime("%Y-%m-%d")
    # 데이터 프레임의 when_played 열 변환
    # df['when_played'] = df['when_played'].apply(lambda x: round_to_nearest_minutes(x))
    df = df.groupby('when_played').agg({'elapsed_time': 'mean', 'kill_count': 'mean'}).reset_index()
    df.columns = ['when_played', 'elapsed_time', 'kill_count']
    df = df[df['when_played']=='2024-06-04']
    # print(df)
    df = df.sort_values(by='when_played')
    df.set_index('when_played', inplace=True)
    print(df)
    return df


def preprocess_alreadydata(filename):
    csv_file_path = os.path.join(settings.STATICFILES_DIRS[0], 'data', filename)
    df = pd.read_csv(csv_file_path)
    # print(df)
    # 데이터 프레임의 when_played 열 변환
    df.set_index('when_played', inplace=True)
    # print(df)
    return df


def predict_future_exog(df):
    # 1. 사용할 외생변수 추출
    exog_vars = ['elapsed_time', 'kill_count']
    data = df[exog_vars]
    data.index = pd.to_datetime(data.index)
    # print(f"Data type before processing: {type(data)}")
    # print(data.tail())
    if not isinstance(data, pd.DataFrame):
        data = pd.DataFrame(data)
    # print(data)
    # sktime의 데이터 형식으로 변환
    # from sktime.datatypes import check_raise
    # from sktime.datatypes import SCITYPE_REGISTER

    # # 데이터 형식 검사
    # try:
    #     check_raise(data, mtype="pd.DataFrame", scitype="Series")
    # except Exception as e:
    #     print(f"Data format error: {e}")

    # 2 : 외생변수 각각에 대한 시계열 예측 수행
    exog_exps = []
    exog_models = []
    for exog_var in exog_vars:
        # 외생변수에 대한 예측을 도출하기 위하여 시계열 실험 생성
        exog_exp = TSForecastingExperiment()
        # setup
        exog_exp.setup(
            data=data[[exog_var]],
            target=exog_var,
            fh=1,
            session_id=42,
            verbose=False,
        )
        print('**')
        # 모델 비교 및 최종 모델 선택
        best = exog_exp.compare_models(
            sort="mae",
            verbose=False,
        )
        print('***')
        final_exog_model = exog_exp.finalize_model(best)
        exog_exps.append(exog_exp)
        exog_models.append(final_exog_model)

    # 3: 외생 변수에 대한 미래 예측 얻기
    future_exog = [exog_exp.predict_model(exog_model) for exog_exp, exog_model in zip(exog_exps, exog_models)]
    print(f"future_exog:{future_exog}")
    # 4. 예측값 concat
    future_exog = pd.concat(future_exog, axis=1)
    future_exog.columns = exog_vars
    # 데이터 형식 확인
    print(f"Data type after processing: {type(future_exog)}")
    print(future_exog.head())
    return future_exog


@api_view(['GET'])
def predict_score(request, user_id):
    if request.method == 'GET':
        # 외부 DB에서 데이터 가져오기
        games = Game.objects.filter(user_id=user_id)
        serializer = GameSerializer(games, many=True)
        serialized_data = serializer.data
        # print(serialized_data)
        if not serialized_data:
            return JsonResponse({"error": "No data found for the user."}, status=404)
        # 외부 db에 적재된 데이터를 갖고와 전처리 후 df화
        df_new = preprocess_newdata(serialized_data)
        # 기존의 학습 데이터
        df_already = preprocess_alreadydata('alreadydata.csv')
        print(f"df_new type: {type(df_new)}, columns: {df_new.columns}")
        print(f"df_already type: {type(df_already)}, columns: {df_already.columns}")
        df_final = pd.concat([df_already, df_new], axis=0)
        # 데이터 형식 확인
        print(f"df_final type: {type(df_final)}, columns: {df_final.columns}")
        print(df_final.tail())
        # 예측 외생 변수 도출
        future_exog = predict_future_exog(df_final)
        # print(future_exog)
        # 미래 예측용 시계열 실험 생성
        exp_future = TSForecastingExperiment()
        # 훈련된 PyCaret 모델 로드
        model_path = os.path.join(settings.STATICFILES_DIRS[0], 'model', 'pycaret_model')
        # print(model_path)
        final_slim_model = exp_future.load_model(model_path)
        # 최종 예측
        future_preds = exp_future.predict_model(
            final_slim_model,  # 모델 입력
            X=future_exog,  # 외생변수 입력
        )
        # print(f'future_preds type : {type(future_preds)}, column : {future_preds.columns}')
        print(future_preds)
        # 결과를 JSON 형식으로 변환하여 반환
        predictions_json = future_preds['y_pred'].to_json()
        return Response(predictions_json, content_type='application/json')
