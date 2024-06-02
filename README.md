# Database Scheme
## users
| Column Name   | Data Type   | Constraints   |
|---------------|-------------|---------------|
| user_id       | INT         | PK, AI        |
| name          | VARCHAR(20) | UQ            |
| password      | VARCHAR(20) | NN            |
| best_score    | INT         | NN, DEFAULT=0 |
| average_score | DOUBLE      | NN, DEFAULT=0 |
| ranking       | INT         |               |
| play_count    | INT         | NN, DEFAULT=0 |
- user_id
    - 각 유저들에게 부여되는 고유 ID
    - 통신용
    - 편의상 Integer, Auto Increment.
    - 실제 서비스에서는 암호화된 인증키가 될 것
- name
    - 유저가 직접 정하는 ID
- password
    - ID에 대한 비밀번호
    - 실제 서비스에서는 암호화. 보안 조치
- best_score
    - 해당 유저의 최고 점수
- average_score
    - 해당 유저의 평균 점수
- ranking
    - 해당 유저의 순위
    - best_score 기준
- play_count
    - 해당 유저가 플레이한 게임의 횟수
## games
| Column Name  | Data Type | Constraints       |
|--------------|-----------|-------------------|
| game_id      | INT       | PK, AI            |
| user_id      | INT       | FK(users.user_id) |
| when_played  | DATETIME  | NN                |
| kill_count   | INT       | NN                |
| elapsed_time | DOUBLE    | NN                |
| score        | INT       | NN                |
- game_id
    - 각 게임에게 부여되는 고유 ID
    - 통신용
    - 편의상 Integer, Auto Increment.
    - 실제 서비스에서는 암호화
- user_id
    - 해당 게임을 플레이한 유저의 고유 ID
    - users.user_id를 참조
- when_played
    - 해당 게임을 플레이한 시간
- kill_count
    - 해당 게임에서 얻은 적 격추 수
- elapsed_time
    - 해당 게임에서 게임오버까지 버틴 시간
- score
    - 해당 게임에서 얻은 점수
## users:games =  1:N (user_id)
