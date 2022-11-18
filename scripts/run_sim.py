import random
import pandas as pd

from hoki.pawn import (
    Pawn,
    dominant_hands,
    position,
    generate_player_name,
)
from hoki import faker
from hoki.statblock import generate_inital_stats, get_df_row, STAT_NAMES
from hoki.team import Team, Jersey, generate_team_name
from hoki.game import GameManager
from hoki.body import Body


if __name__ == "__main__":
    positions = [
        position.GOALIE,
        position.DEFENCE_L,
        position.DEFENCE_R,
        position.WING_L,
        position.WING_R,
        position.CENTRE,
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
                Pawn(
                    name=generate_player_name(),
                    position=p,
                    id=i,
                    shoots=dominant_hands.LEFT
                    if random.randint(0, 1) == 0
                    else dominant_hands.RIGHT,
                    stats=generate_inital_stats(),
                    jersey_num=random.randint(0, 99),
                    body=Body(),
                )
            )
            players[i] = (
                [
                    t.name,
                    t.players[-1].name,
                    t.players[-1].position.name,
                ]
                + get_df_row(t.players[-1].stats)
                + [t.players[-1].get_player_rating()]
            )
            i += 1

    players = pd.DataFrame.from_dict(
        data=players,
        orient="index",
        columns=[
            "team",
            "name",
            "pos",
        ] + STAT_NAMES + [
            "rating"
        ],
    )

    game = GameManager(
        home_team=teams[0],
        away_team=teams[1],
    )

    game.run_game()
    print()
    print(players)
