#pip install mysql-connector-python

import random
import string
from datetime import datetime, timedelta
import mysql.connector

# 데이터베이스 연결 설정
conn = mysql.connector.connect(
    host="your_host",
    user="your_user",
    password="your_password",
    database="your_database"
)
cursor = conn.cursor()

# 랜덤 비밀번호 생성 함수
def generate_random_password(length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))

# 사용자 데이터 생성
user_sql = "INSERT INTO users (name, password, best_score, average_score, ranking, play_count) VALUES "
user_values = []
for i in range(1, 2001):
    name = f'user{i}'
    password = generate_random_password(12)  # 12자리 랜덤 비밀번호 생성
    best_score = 0
    average_score = 0
    ranking = 'NULL'
    play_count = 0
    user_values.append(f"('{name}', '{password}', {best_score}, {average_score}, {ranking}, {play_count})")

user_sql += ",".join(user_values) + ";"

# 사용자 데이터 삽입
cursor.execute(user_sql)
conn.commit()

# 각 사용자당 100개의 게임 데이터 생성
game_sql = "INSERT INTO games (user_id, when_played, kill_count, elapsed_time, score) VALUES "
game_values = []
for i in range(1, 2001):
    for j in range(100):
        user_id = i
        when_played = datetime.now() - timedelta(days=random.randint(0, 365))
        when_played_str = when_played.strftime('%Y-%m-%d %H:%M:%S')
        kill_count = random.randint(0, 100)
        elapsed_time = random.uniform(0.1, 60.0)
        score = random.randint(0, 1000)
        game_values.append(f"({user_id}, '{when_played_str}', {kill_count}, {elapsed_time}, {score})")

        # 너무 많은 값을 한 번에 삽입하면 안 되기 때문에 일정한 갯수마다 삽입
        if len(game_values) >= 1000:
            game_sql += ",".join(game_values) + ";"
            cursor.execute(game_sql)
            conn.commit()
            game_sql = "INSERT INTO games (user_id, when_played, kill_count, elapsed_time, score) VALUES "
            game_values = []

if game_values:
    game_sql += ",".join(game_values) + ";"
    cursor.execute(game_sql)
    conn.commit()

cursor.close()
conn.close()
