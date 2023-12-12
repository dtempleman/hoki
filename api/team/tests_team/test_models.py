from django.test import TestCase
from pawn.models import Pawn
from team.models import Team, TeamContract


# Create your tests here.
class TeamModelTests(TestCase):
    def create_team(self):
        return Team.objects.create(
            name="name",
            location="location",
        )

    def create_team_contract(self, team, pawn):
        return TeamContract.objects.create(team=team, player=pawn, jersey_number=1)

    def create_pawn(self):
        return Pawn.objects.create(
            first_name="first",
            last_name="last",
            birthday="2000-01-01",
        )

    def test_team(self):
        team = self.create_team()
        self.assertTrue(isinstance(team, Team))

    def test_team_contract(self):
        pawn = self.create_pawn()
        team = self.create_team()
        contract = self.create_team_contract(team, pawn)

        self.assertTrue(isinstance(contract, TeamContract))
