import random

import pytest

from hoki.game import GameManager
from hoki.models.body import Body
from hoki.models.pawn import Pawn, generate_pawn_name
from hoki.models.player import Player, dominant_hands, position
from hoki.models.savestate import SaveState
from hoki.models.statblock import generate_inital_stats
from hoki.models.team import Team, generate_team_name


@pytest.fixture()
def create_teams(create_team):
    def func(n_teams=1):
        return [create_team() for _ in range(n_teams)]

    return func


@pytest.fixture()
def create_team():
    def func(**kwargs):
        return Team(name=generate_team_name())

    return func


@pytest.fixture()
def create_player():
    def func(**kwargs):
        values = dict(
            name=generate_pawn_name(),
            position=position.CENTRE,
            id=0,
            shoots=dominant_hands.LEFT,
            stats=generate_inital_stats(),
            jersey_num=random.randint(0, 99),
            body=Body(),
        )
        values.update(kwargs)
        return Player(
            name=values["name"],
            position=values["position"],
            id=values["id"],
            shoots=values["shoots"],
            stats=values["stats"],
            jersey_num=values["jersey_num"],
            body=values["body"],
        )

    return func


@pytest.fixture()
def create_players(create_player):
    def func(n_players=1):
        return [create_player() for _ in range(n_players)]

    return func


@pytest.fixture()
def fill_teams_with_pawns():
    def func(teams):
        positions = [
            position.GOALIE,
            position.DEFENCE_L,
            position.DEFENCE_R,
            position.WING_L,
            position.WING_R,
            position.CENTRE,
        ]

        players = []
        i = 0
        for t in teams:
            for p in positions:
                players.append(
                    Player(
                        name=generate_pawn_name(),
                        position=p,
                        id=str(i),
                        shoots=dominant_hands.LEFT
                        if random.randint(0, 1) == 0
                        else dominant_hands.RIGHT,
                        stats=generate_inital_stats(),
                        jersey_num=random.randint(0, 99),
                        body=Body(),
                    )
                )
                t.players.append(players[-1].id)
                i += 1
        return players

    return func


@pytest.fixture()
def create_game(create_teams, fill_teams_with_pawns):
    def func():
        teams = create_teams(2)
        players = fill_teams_with_pawns(teams)
        game = GameManager(teams[0], teams[1], pawns=players)
        return game, teams, players

    return func
