from rest_framework import serializers

from .models import Team, TeamContract


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = [
            "id",
            "name",
            "location",
            "primary_color",
            "secondary_color",
        ]


class TeamContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamContract
        fields = [
            "id",
            "player",
            "team",
            "jersey_number",
        ]
