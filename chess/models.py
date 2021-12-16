from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Game(models.Model):
    room_code = models.CharField(max_length = 240)
    game_creator = models.CharField(max_length = 240)
    game_opponent = models.CharField(max_length = 100, blank=True, null=True)
    is_over = models.BooleanField(default = False)

class Chess(models.Model):
    name = models.CharField(max_length=4 , primary_key=True)
    value = models.CharField(max_length=7)
