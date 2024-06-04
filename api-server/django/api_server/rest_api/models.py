from django.db import models


# User model
class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=20)
    best_score = models.IntegerField(default=0)
    average_score = models.FloatField(default=0)
    ranking = models.IntegerField(null=True, blank=True)  # Allowing null and blank values
    play_count = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'users'


# Game model
class Game(models.Model):
    game_id = models.AutoField(primary_key=True, db_column='game_id')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id')
    when_played = models.DateTimeField()
    kill_count = models.IntegerField()
    elapsed_time = models.FloatField()
    score = models.IntegerField()

    def __str__(self):
        return f'Game played by {self.user_id.name if self.user_id else "Unknown User"} on {self.when_played}'

    class Meta:
        db_table = 'games'
