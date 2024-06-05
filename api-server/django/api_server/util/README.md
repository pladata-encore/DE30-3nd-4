## sampledata_generator
- 무작위 값으로 샘플 User, Game 데이터 생성 후 MySQL DB에 직접 SQL 쿼리로 삽입
- 데이터 생성, 삽입 후 /admin/update/ 실행하여 값 알맞게 갱신할 것
- `pip install mysql-connector-python`
-   SQL query로 테이블의 데이터 초기화, AUTO_INCREMENT값 1부터 다시 시작하도록 초기화
  ```SQL
  DELETE FROM users;
  ALTER TABLE users AUTO_INCREMENT = 1;
  ALTER TABLE games AUTO_INCREMENT = 1;
  ```
