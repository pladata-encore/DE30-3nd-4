# API 명세서
## API 일람
- /api/register/ : 회원가입
- /api/login/ : 로그인
- /api/user/ : 유저 정보
- /api/game/ : 게임 정보
- /api/usergames/ : 특정 유저의 게임 정보
- /api/leaderboard/ : 리더보드
- /api/save/ : 게임 기록 저장
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
  - URL: `/api/save/`
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
### 모든 사용자 정보 가져오기
- Request
  - Method: `GET`
  - URL: `/api/users/`
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
