from django.db import models


class Pawn(models.Model):
    first_name = models.CharField(max_length=256, null=False)
    last_name = models.CharField(max_length=256, null=False)
    birthday = models.DateField(null=True)

    # pawn attributes
    iq = models.FloatField(null=True, default=0.0)
    positioning = models.FloatField(null=True, default=0.0)
    shooting = models.FloatField(null=True, default=0.0)
    passing = models.FloatField(null=True, default=0.0)
    goaltending = models.FloatField(null=True, default=0.0)
    skating = models.FloatField(null=True, default=0.0)
    checking = models.FloatField(null=True, default=0.0)
    balancing = models.FloatField(null=True, default=0.0)

    def __str__(self):
        return f"{self.id} {self.first_name} {self.last_name}"


class PawnBody(models.Model):
    pawn = models.ForeignKey(Pawn, null=False, on_delete=models.CASCADE)
    head = models.FloatField(default=1.0)
    torso = models.FloatField(default=1.0)
    arm_right = models.FloatField(default=1.0)
    arm_left = models.FloatField(default=1.0)
    leg_right = models.FloatField(default=1.0)
    leg_left = models.FloatField(default=1.0)
