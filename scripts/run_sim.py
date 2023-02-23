import random
import pandas as pd
from pathlib import Path
import xml.etree.ElementTree as ET

from hoki.pawn import (
    Pawn,
    dominant_hands,
    position,
    generate_player_name,
)
from hoki.statblock import generate_inital_stats, get_df_row, STAT_NAMES
from hoki.team import Team, generate_team_name
from hoki.game import GameManager
from hoki.body import Body
from hoki.save_manager import save_state_to_xml, xml_to_save_state


DATA_DIR = "data"
DATA_FILE = "data.xml"


def generate_teams(n_teams=2):
    return [Team(name=generate_team_name()) for _ in range(n_teams)]


def generate_players(teams):
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
            t.players.append(
                players[-1].id
            )
            i += 1
    return players

def generate_players_df(players):
    data = {}
    i = 0
    for player in players:
        data[i] = (
            [
                player.name,
                player.position.name,
            ]
            + get_df_row(player.stats)
            + [player.get_player_rating()]
        )
        i += 1

    return pd.DataFrame.from_dict(
        data=data,
        orient="index",
        columns=[
            # "team",
            "name",
            "pos",
        ] + STAT_NAMES + [
            "rating"
        ],
    )


if __name__ == "__main__":

    data_file = Path(DATA_DIR, DATA_FILE)
    if data_file.is_file():
        print("Loading existing dataset")
        annotation_tree = ET.parse(data_file)
        root = annotation_tree.getroot()
        players, teams = xml_to_save_state(root)

    else:
        print("Generating new dataset")
        teams = generate_teams()
        players = generate_players(teams)
        root = save_state_to_xml(teams=teams, pawns=players)
        ET.ElementTree(root).write(data_file)

    players_df = generate_players_df(players)

    game = GameManager(
        home_team=teams[0],
        away_team=teams[1],
        pawns=players,
    )

    game.run_game()
    game.print_game_summary()
    print()
    print(players_df)
