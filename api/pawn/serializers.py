from rest_framework import serializers

from .models import Pawn, PawnBody


class PawnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pawn
        fields = [
            "id",
            "first_name",
            "last_name",
            "birthday",
            "iq",
            "positioning",
            "shooting",
            "passing",
            "goaltending",
            "skating",
            "checking",
            "balancing",
        ]


class PawnBodySerializer(serializers.ModelSerializer):
    class Meta:
        model = PawnBody
        fields = [
            "id",
            "pawn",
            "head",
            "torso",
            "arm_right",
            "arm_left",
            "leg_right",
            "leg_left",
        ]
