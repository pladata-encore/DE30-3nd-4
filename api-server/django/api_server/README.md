# Django API server 사용 방법
## 개발 환경
- python version: 3.10
- OS: Windows 10
- IDE: pycharm
- packages:
  - asgiref==3.8.1
  - Django==5.0.6
  - djangorestframework==3.15.1
  - mysqlclient==2.2.4
  - pip==24.0
  - setuptools==65.5.0
  - sqlparse==0.5.0
  - tzdata==2024.1
## 설치 과정
#### * 본 repository의 django project 이름은 'api_server', APP 이름은 'rest_api'.
### 1. 프로젝트 및 앱 생성
1. 프로젝트 root로 사용할 디렉토리 생성
2. 터미널을 실행하고 현재경로를 프로젝트 root로 지정
3. 터미널에서 `python -m venv [가상환경이름]` 입력하여 가상환경 생성
4. `.\[가상환경이름]\Scripts\activate` 입력하여 가상환경 실행
5. requirements.txt 파일을 프로젝트 root에 두기
6. `pip install -r .\requirements.txt` 입력하여 필요한 패키지 설치
7. `django-admin startproject [프로젝트이름] .` 입력하여 현재 경로에 django 프로젝트 생성
8. `python manage.py startapp [앱이름]` 입력하여 현재 경로에 앱 생성
9. `python manage.py runserver` 입력하여 서버 실행했다가 종료
#### Directory Tree
- root<br>
&nbsp;&nbsp;&nbsp;|----[가상환경폴더]<br>
&nbsp;&nbsp;&nbsp;|<br>
&nbsp;&nbsp;&nbsp;|----[프로젝트폴더]<br>
&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|<br>
&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|----프로젝트 파일들<br>
&nbsp;&nbsp;&nbsp;|<br>
&nbsp;&nbsp;&nbsp;|----[앱폴더]<br>
&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|<br>
&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|----앱 파일들<br>
&nbsp;&nbsp;&nbsp;|<br>
&nbsp;&nbsp;&nbsp;|----manage.py<br>
&nbsp;&nbsp;&nbsp;|<br>
&nbsp;&nbsp;&nbsp;|----requirements.txt
### 2. [프로젝트폴더]\settings.py, urls.py : 프로젝트 설정 파일 수정
- 본 repository의 파일을 그대로 덮어쓰지 않고 참고만 하여,
- 찾기 기능을 활용하여 MODIFY로 주석처리된 부분만 수정합니다.
### 3. 나머지 파일들 : 덮어쓰기
### 4. 관리자 계정 만들기
- `python manage.py createsuperuser`
### 5. DB에 적용할 변경사항을 마이그레이션 파일로 생성
- `python manage.py makemigrations`
### 6. 마이그레이션 파일을 실제 DB에 적용
- `python manage.py migrate`
- -> Django 모델 정의가 데이터베이스 테이블로 변환된다!
### 7. 서버 실행
- `python manage.py runserver 0.0.0.0:[port]`
- 지정한 ip와 port로 서버를 엽니다.
- 비우면 기본값 localhost:8000


# API 명세서
## 전체 API 일람
- /api/register/ : 회원가입
- /api/login/ : 로그인
- /api/user/ : 유저 정보
- /api/game/ : 게임 정보
- /api/usergames/ : 특정 유저의 게임 정보
- /api/leaderboard/ : 리더보드
- /api/savegame/ : 게임 기록 저장
- ~~/api/users/ : 모든 유저 정보~~
- ~~/api/games/ : 모든 게임 정보~~
- ~~/api/update/ : 유저 정보 갱신~~
## 노출될 API
### 회원가입
- Request
  - Method: `POST`
  - URL: `/api/register/`
  - Body:
    ```json
    {
      "name": "john",
      "password": "1q"
    }
    ```
- Response
  - Status: `200`
  - Body:
    ```json
    {
      "user_id": 1
    }
    ```
- Error Response
  - Status: `409`
    - ID가 이미 존재
    - Body:
      ```json
      {
        "message": "The ID already exists."
      }
      ```
  - Status: `410`
    - 입력한 ID 혹은 password가 비어있거나 20자를 초과
    - Body:
      ```json
      {
        "message": "Input is empty or exceeded 20 characters."
      }
      ```
  - Status: `400`
    - 그 외의 error들
    - Body:
      ```json
      {
        "message": "Bad Request"
      }
      ```
### 로그인
- Request
  - Method: `POST`
  - URL: `/api/login/`
  - Body:
    ```json
    {
      "name": "john",
      "password": "1q"
    }
    ```
- Response
  - Status: `200`
  - Body:
    ```json
    {
      "user_id": 1
    }
    ```
- Error Response
  - Status: `403`
    - password가 일치하지 않음
    - Body:
      ```json
      {
        "message": "Incorrect password."
      }
      ```
  - Status: `409`
    - ID가 존재하지 않음
    - Body:
      ```json
      {
        "message": "ID does not exist."
      }
      ```
  - Status: `410`
    - 입력한 ID 혹은 password가 비어있거나 20자를 초과
    - Body:
      ```json
      {
        "message": "Input is empty or exceeded 20 characters."
      }
      ```
  - Status: `400`
    - 그 외의 error들
    - Body:
      ```json
      {
        "message": "Bad Request"
      }
      ```
### 유저 정보
- Request
  - Method: `POST`
  - URL: `/api/user/`
  - Body:
    ```json
    {
      "user_id": 1
    }
    ```
- Response
  - Status: `200`
  - Body:
    ```json
    {
      "name": "john",
      "best_score": 999,
      "average_score": 456.6,
      "ranking": 789,
      "play_count": 12
    }
    ```
- Error Response
  - Status: `409`
    - 존재하지 않는 user
    - Body:
      ```json
      {
        "message": "User does not exist."
      }
      ```
  - Status: `400`
    - 그 외의 error들
    - Body:
      ```json
      {
        "message": "Bad Request"
      }
      ```
### 게임 정보
- Request
  - Method: `POST`
  - URL: `/api/game/`
  - Body:
    ```json
    {
      "game_id": 23
    }
    ```
- Response
  - Status: `200`
  - Body:
    ```json
    {
      "user_id": 3,
      "when_played": "2024-06-19T09:00:00+09:00",
      "kill_count": 19,
      "elapsed_time": 14.6307316744986,
      "score": 159
    }
    ```
- Error Response
  - Status: `409`
    - 존재하지 않는 game
    - Body:
      ```json
      {
        "message": "Game does not exist."
      }
      ```
  - Status: `400`
    - 그 외의 error들
    - Body:
      ```json
      {
        "message": "Bad Request"
      }
      ```
### 특정 유저의 게임 정보
- Request
  - Method: `POST`
  - URL: `/api/usergames/`
  - Body:
    ```json
    {
      "user_id": 1
    }
    ```
- Response
  - Status: `200`
  - Body:
    ```json
    [
      {
        "game_id": 1,
        "when_played": "2024-05-01T19:00:00+09:00",
        "kill_count": 5,
        "elapsed_time": 15.5,
        "score": 1000
      },
      {
        "game_id": 2,
        "when_played": "2024-05-02T21:00:00+09:00",
        "kill_count": 8,
        "elapsed_time": 20,
        "score": 1500
      }
    ]
    ```
- Error Response
  - Status: `409`
    - 유저가 존재하지 않음
    - Body:
      ```json
      {
        "message": "User does not exist."
      }
      ```
  - Status: `400`
    - 그 외의 error들
    - Body:
      ```json
      {
        "message": "Bad Request"
      }
      ```
### 리더보드
#### 랭킹 상위 n명의 유저 정보
- Request
  - Method: `GET`
  - URL: `/api/leaderboard/`
  - query:
    - n: 출력할 상위 n명, default: 10
- Response
  - Status: `200`
  - Body:
    ```json
    [
      {
        "name": "john",
        "best_score": 999,
        "average_score": 456.6,
        "ranking": 1,
        "play_count": 5
      },
      {
        "name": "jane",
        "best_score": 888,
        "average_score": 433.6,
        "ranking": 2,
        "play_count": 31
      },
      {
        "name": "doe",
        "best_score": 777,
        "average_score": 231.6,
        "ranking": 3,
        "play_count": 15
      },
      {
        "name": "doee",
        "best_score": 666,
        "average_score": 123.6,
        "ranking": 4,
        "play_count": 123
      },
      ...
    ]
    ```
### 게임 기록 저장
#### 플레이한 유저의 정보, 전체 유저의 순위 update 포함
- Request
  - Method: `POST`
  - URL: `/api/savegame/`
  - Body:
    ```json
    {
      "user_id": 5,
      "when_played": "2024-06-02T15:30:00Z",
      "kill_count": 5,
      "elapsed_time": 12.34,
      "score": 150
    }
    ```
- Response
  - Status: `200`
  - Body:
    ```json
    {
      "message": "Game log added, User game statistics and Entire user's rankings updated successfully."
    }
    ```
- Error Response
  - Status: `400`
  - Body:
    ```json
    {
      "message": "Bad Request"
    }
    ```
## 개발/디버그 용 API
### 모든 유저 정보 가져오기
- Request
  - Method: `GET`
  - URL: `/api/users/`
  - query: x
- Response
  - Status: `200`
  - Body: 
    ```json
    [
      {
        "user_id": 1,
        "name": "john",
        "password": "1q",
        "best_score": 0,
        "average_score": 0,
        "ranking": 5,
        "play_count": 0
      },
      {
        "user_id": 2,
        "name": "doe",
        "password": "2w",
        "best_score": 0,
        "average_score": 0,
        "ranking": 111,
        "play_count": 0
      },
      ...
    ]
    ```
### 모든 게임 정보 가져오기
- Request
  - Method: `GET`
  - URL: `/api/games/`
  - query: x
- Response
  - Status: `200`
  - Body: 
    ```json
    [
      {
        "game_id": 1,
        "user_id": 1,
        "when_played": "2024-05-01T19:00:00+09:00",
        "kill_count": 5,
        "elapsed_time": 15.5,
        "score": 1000
      },
      {
        "game_id": 2,
        "user_id": 1,
        "when_played": "2024-05-02T21:00:00+09:00",
        "kill_count": 8,
        "elapsed_time": 20,
        "score": 1500
      },
      {
        "game_id": 3,
        "user_id": 2,
        "when_played": "2024-05-01T20:00:00+09:00",
        "kill_count": 10,
        "elapsed_time": 25.5,
        "score": 2000
      },
      {
        "game_id": 4,
        "user_id": 2,
        "when_played": "2024-05-03T23:00:00+09:00",
        "kill_count": 6,
        "elapsed_time": 18.5,
        "score": 1200
      }
    ]
    ```
### 유저 정보 갱신
#### 무작위 값으로 생성한 테스트 데이터들의 값들을 알맞게 수정
- Request
  - Method: `POST`
  - URL: `/api/update/`
  - Body:
    ```json
    {
      "SECRET_KEY": "admin_password"
    }
    ```
- Response
  - Status: `200`
  - Body:
    ```json
    {
      "message": "Updated database"
    }
    ```
- Error Response
  - Status: `403`
    - password가 일치하지 않음
    - Body:
      ```json
      {
        "message": "Incorrect password."
      }
      ```
  - Status: `400`
    - 그 외의 error들
    - Body:
      ```json
      {
        "message": "Bad Request"
      }
      ```
