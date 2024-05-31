from django.db import models


# Create your models here.
class User(models.Model):
    _id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=20)
    best_score = models.IntegerField()
    average_score = models.FloatField()
    ranking = models.IntegerField()
    play_count = models.IntegerField()

    def __str__(self):
        return self.user_id


class Game(models.Model):
    _id = models.ForeignKey(User, on_delete=models.CASCADE, db_column='_id')
    when_played = models.DateTimeField()
    kill_count = models.IntegerField()
    elapsed_time = models.FloatField()
    score = models.IntegerField()

    class Meta:
        unique_together = ('_id', 'when_played')

    def __str__(self):
        return f'Game played by {self._id.user_id} on {self.when_played}'