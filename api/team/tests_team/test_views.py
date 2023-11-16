import ast

from django.test import TestCase
from django.urls import reverse
from pawn.models import Pawn
from team import views
from team.models import Team, TeamContract
from team.serializers import TeamContractSerializer, TeamSerializer

# Create your tests here.


def decode_response_content(resp):
    return ast.literal_eval(resp.content.decode("UTF-8"))


class TeamViewTests(TestCase):
    def create_team(self):
        return Team.objects.create(
            name="name",
            location="location",
        )

    def create_team_contract(self, team_id, pawn_id):
        return TeamContract.objects.create(
            team_id=team_id, player_id=pawn_id, jersey_number=1
        )

    def create_pawn(self):
        return Pawn.objects.create(
            first_name="first",
            last_name="last",
            birthday="2000-01-01",
        )

    def test_list_teams(self):
        _ = self.create_team()
        resp = self.client.get(
            reverse(views.list_teams),
        )
        self.assertEqual(resp.status_code, 200)

    def test_get_tema(self):
        team = self.create_team()
        resp = self.client.get(
            reverse(views.get_team, args=[team.id]),
        )
        self.assertEqual(resp.status_code, 200)

    def test_set_team(self):
        resp = self.client.post(
            reverse(views.set_team),
            data={
                "name": "name",
                "location": "location",
            },
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, 200)

    def test_delete_team(self):
        team = self.create_team()
        resp = self.client.delete(
            reverse(views.delete_team, args=[team.id]),
        )
        self.assertEqual(resp.status_code, 200)

        resp = self.client.get(
            reverse(views.get_team, args=[team.id]),
        )
        self.assertEqual(resp.status_code, 404)

    def test_update_team(self):
        team = self.create_team()
        serializer = TeamSerializer(team)
        data = serializer.data
        data["location"] = "new location"

        resp = self.client.put(
            reverse(views.update_team, args=[team.id]),
            data=data,
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, 200)

        resp = self.client.get(
            reverse(views.get_team, args=[team.id]),
        )
        content = decode_response_content(resp)
        self.assertEqual(content["location"], "new location")

    def test_set_contract(self):
        team = self.create_team()
        pawn = self.create_pawn()
        resp = self.client.post(
            reverse(views.set_contract),
            data={
                "team": team.id,
                "player": pawn.id,
                "jersey_number": 1,
            },
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, 200)

    def test_delete_contract(self):
        team = self.create_team()
        pawn = self.create_pawn()
        contract = self.create_team_contract(team.id, pawn.id)
        resp = self.client.delete(
            reverse(views.delete_contract, args=[contract.id]),
        )
        self.assertEqual(resp.status_code, 200)

        resp = self.client.get(
            reverse(views.get_player_contract, args=[pawn.id]),
        )
        self.assertEqual(resp.status_code, 404)

    def test_update_contract(self):
        team = self.create_team()
        pawn = self.create_pawn()
        contract = self.create_team_contract(team.id, pawn.id)
        serializer = TeamContractSerializer(contract)
        data = serializer.data
        data["jersey_number"] = 2

        resp = self.client.put(
            reverse(views.update_contract, args=[contract.id]),
            data=data,
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, 200)

        resp = self.client.get(
            reverse(views.get_player_contract, args=[pawn.id]),
        )
        content = decode_response_content(resp)
        self.assertEqual(content["jersey_number"], 2)

    def test_list_team_contracts(self):
        team = self.create_team()
        pawns, contracts = [], []
        for i in range(5):
            pawn = self.create_pawn()
            contract = self.create_team_contract(team.id, pawn.id)
            pawns.append(pawn)
            contracts.append(contract)
        resp = self.client.get(
            reverse(views.list_team_contracts, args=[team.id]),
        )
        self.assertEqual(resp.status_code, 200)
        content = decode_response_content(resp)
        self.assertEqual(len(content), 5)

    def test_get_player_contract(self):
        team = self.create_team()
        pawn = self.create_pawn()
        self.create_team_contract(team.id, pawn.id)
        resp = self.client.get(
            reverse(views.get_player_contract, args=[pawn.id]),
        )
        self.assertEqual(resp.status_code, 200)
