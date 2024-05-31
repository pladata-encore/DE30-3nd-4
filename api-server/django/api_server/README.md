# Database Scheme
- users

  | Column Name   | Data Type   | Constraints   |
  |---------------|-------------|---------------|
  | user_id       | INT         | PK, AI        |
  | name          | VARCHAR(20) | UQ            |
  | password      | VARCHAR(20) | NN            |
  | best_score    | INT         | NN, DEFAULT=0 |
  | average_score | DOUBLE      | NN, DEFAULT=0 |
  | ranking       | INT         |               |
  | play_count    | INT         | NN, DEFAULT=0 |

- games

  | Column Name  | Data Type   | Constraints       |
  |--------------|-------------|-------------------|
  | game_id      | INT         | PK, AI            |
  | user_id      | VARCHAR(20) | FK(users.user_id) |
  | when_played  | DATETIME    | NN                |
  | kill_count   | INT         | NN                |
  | elapsed_time | DOUBLE      | NN                |
  | score        | INT         | NN                |
