import random
import pandas as pd

from hoki.player import (
    Player,
    stick_hand,
    position,
    generate_player_name,
    generate_inital_stats,
)
from hoki.team import Team, Jersey, generate_team_name
from hoki.game_engine import Game
from hoki import faker


if __name__ == "__main__":
    positions = [
        position.GOALIE,
        position.DEFENCE,
        position.DEFENCE,
        position.FORWARD,
        position.FORWARD,
        position.FORWARD,
    ]

    prim_1 = faker.color()
    sec_1 = faker.color()
    trim_1 = faker.color()
    prim_2 = faker.color()
    sec_2 = faker.color()
    trim_2 = faker.color()

    teams = [
        Team(
            name=generate_team_name(),
            home_jersey=Jersey(
                primary_colour=prim_1,
                secondary_colour=sec_1,
                trim_colour=trim_1,
            ),
            away_jersey=Jersey(
                primary_colour=sec_1,
                secondary_colour=prim_1,
                trim_colour=trim_1,
            ),
        ),
        Team(
            name=generate_team_name(),
            home_jersey=Jersey(
                primary_colour=prim_2,
                secondary_colour=sec_2,
                trim_colour=trim_2,
            ),
            away_jersey=Jersey(
                primary_colour=sec_2,
                secondary_colour=prim_2,
                trim_colour=trim_2,
            ),
        ),
    ]

    players = {}
    i = 0
    for t in teams:
        for p in positions:
            t.players.append(
                Player(
                    name=generate_player_name(),
                    position=p,
                    id=i,
                    shoots=stick_hand.LEFT
                    if random.randint(0, 1) == 0
                    else stick_hand.RIGHT,
                    stats=generate_inital_stats(),
                    jersey_num=random.randint(0, 99),
                )
            )
            players[i] = [
                t.name,
                t.players[-1].name,
                t.players[-1].position,
            ] + t.players[-1].stats.df_row()
            i += 1

    players = pd.DataFrame.from_dict(
        data=players,
        orient="index",
        columns=["team", "name", "pos", "positioning", "accuracy", "strength", "iq"],
    )

    game = Game(
        home_team=teams[0],
        away_team=teams[1],
    )

    print(players)
    print()
    game.run()
    print()
    game.print_score()
    print()
    print(game.boxscore.stats)
