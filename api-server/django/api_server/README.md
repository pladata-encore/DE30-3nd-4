# Database Scheme
- users

  | Column Name   | Data Type   | Constraints |
  |---------------|-------------|-------------|
  | _id           | INT         | PK, AI      |
  | user_id       | VARCHAR(20) | UQ          |
  | password      | VARCHAR(20) | NN          |
  | best_score    | INT         | NN          |
  | average_score | DOUBLE      | NN          |
  | ranking       | INT         | NN          |
  | play_count    | INT         | NN          |

- games

  | Column Name  | Data Type | Constraints        |
  |--------------|-----------|--------------------|
  | _id          | INT       | PK, FK (users._id) |
  | when_played  | DATETIME  | PK, NN             |
  | kill_count   | INT       | NN                 |
  | elapsed_time | DOUBLE    | NN                 |
  | score        | INT       | NN                 |
