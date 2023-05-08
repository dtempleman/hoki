import random

from hoki.body import Body
from hoki.game import GameManager
from hoki.pawn import Pawn, dominant_hands, generate_player_name, position
from hoki.statblock import generate_inital_stats
from hoki.team import Team, generate_team_name

POSITIONS = [
    position.GOALIE,
    position.DEFENCE_L,
    position.DEFENCE_R,
    position.WING_L,
    position.WING_R,
    position.CENTRE,
]


def generate_team(name):
    return Team(name=name)


def generate_player(pos, id):
    return Pawn(
        name=generate_player_name(),
        position=pos,
        id=id,
        shoots=dominant_hands.LEFT
        if random.randint(0, 1) == 0
        else dominant_hands.RIGHT,
        stats=generate_inital_stats(),
        jersey_num=random.randint(0, 99),
        body=Body(),
    )


def generate_team_players(offset):
    players = []
    for i, pos in enumerate(POSITIONS):
        players.append(
            Pawn(
                name=generate_player_name(),
                position=pos,
                id=f"p{i + offset}",
                shoots=dominant_hands.LEFT
                if random.randint(0, 1) == 0
                else dominant_hands.RIGHT,
                stats=generate_inital_stats(),
                jersey_num=random.randint(0, 99),
                body=Body(),
            )
        )
    return players


if __name__ == "__main__":
    teams = [generate_team(generate_team_name()), generate_team(generate_team_name())]
    players = []
    for offset, team in enumerate(teams):
        team_players = generate_team_players((offset * 6) + 1)
        team.players = [player.id for player in team_players]
        players += team_players

    game = GameManager(teams[0], teams[1], players)
    game.run()
    print(game.boxscore)
    print(game.boxscore.get_stats())
