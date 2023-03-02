import random
import pandas as pd
from pathlib import Path
import xml.etree.ElementTree as ET
import os

from hoki.pawn import (
    Pawn,
    dominant_hands,
    position,
    generate_player_name,
)
from hoki.statblock import generate_inital_stats, get_df_row, STAT_NAMES
from hoki.team import Team, generate_team_name
from hoki.body import Body
from hoki.save_manager import save_state_to_xml, xml_to_save_state
from hoki.league import League


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
            t.players.append(players[-1].id)
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
            "team",
            "name",
            "pos",
        ]
        + STAT_NAMES
        + ["rating"],
    ).set_index(["name"])


def display_state(game):
    os.system("clear")
    print(game.state.boxscore.get_score())
    print()
    print(game.state.boxscore.stats)
    print()
    for log in game.state.game_log[-10:]:
        print(log)


def print_score(game):
    print(game.boxscore.get_score())


def print_game_summary(game):
    game.print_score()
    print()
    print(game.state.boxscore.get_stats())


def print_standings(league):
    df = league.team_stats
    df["points"] = df["wins"] * 2 + df["overtime-losses"]
    print(df.sort_values(by=["points"], ascending=False))


def print_stats(league):
    df = league.player_stats
    df["points"] = df["goals"] + df["assists"]
    print(df.sort_values(by=["points"], ascending=False))


if __name__ == "__main__":
    data_file = Path(DATA_DIR, DATA_FILE)
    if data_file.is_file():
        print("Loading existing dataset")
        annotation_tree = ET.parse(data_file)
        root = annotation_tree.getroot()
        players, teams = xml_to_save_state(root)

    else:
        print("Generating new dataset")
        teams = generate_teams(n_teams=12)
        players = generate_players(teams)
        root = save_state_to_xml(teams=teams, pawns=players)
        ET.ElementTree(root).write(data_file)

    players_df = generate_players_df(players)
    print(players_df)

    league = League(teams=teams, players=players)
    league.run_season()
    league.player_stats.to_csv(f"data/season_{league.year}_player_stats.csv")
    league.team_stats.to_csv(f"data/season_{league.year}_team_stats.csv")

    print_standings(league)
    print_stats(league)
