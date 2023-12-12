from colorfield.fields import ColorField
from django.db import models
from pawn.models import Pawn


# Create your models here.
class Team(models.Model):
    name = models.CharField(max_length=256, null=False)
    location = models.CharField(max_length=256, null=False)
    primary_color = ColorField()
    secondary_color = ColorField()

    def __str__(self):
        return f"{self.location} {self.name}"


class TeamContract(models.Model):
    player = models.ForeignKey(Pawn, null=False, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, null=False, on_delete=models.CASCADE)
    jersey_number = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.player.name} {self.team.name}"
