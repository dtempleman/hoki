from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)


class Player(models.Model):
    name = models.CharField(max_length=100)
    team = models.ForeignKey(Team, on_delete=models.DO_NOTHING)
    jersey_num = models.IntegerField()
    position = models.CharField(max_length=100)


class Stats(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    positioning = models.FloatField()
    accuracy = models.FloatField()
    strength = models.FloatField()
    iq = models.FloatField()


class Contract(models.Model):
    team = models.ForeignKey(Team, on_delete=models.DO_NOTHING)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    aav = models.FloatField()
    start = models.IntegerField()
    end = models.IntegerField()


class Position(models.Model):
    name = models.TextField(max_length=20)


class PlayerPosition(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
