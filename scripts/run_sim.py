import argparse
import os
import random
import xml.etree.ElementTree as ET
from datetime import datetime
from multiprocessing import Pool
from pathlib import Path

import pandas as pd

from hoki.body import Body
from hoki.league import League
from hoki.pawn import Pawn, dominant_hands, generate_player_name, position
from hoki.save_manager import save_state_to_xml, xml_to_save_state
from hoki.statblock import STAT_NAMES, generate_inital_stats, get_df_row
from hoki.team import Team, generate_team_name

DATA_DIR = "data"
DATA_FILE = "data.xml"

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


def generate_teams(n_teams=2):
    with Pool() as pool:
        teams = pool.map(
            generate_team, [(generate_team_name()) for _ in range(n_teams)]
        )
    return teams


def generate_player(pos, id):
    return Pawn(
        name=generate_player_name(),
        position=pos,
        id=f"p{id}",
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


def generate_players(teams):
    all_players = []
    with Pool() as pool:
        team_players = pool.map(
            generate_team_players, [(i * len(POSITIONS)) for i in range(len(teams))]
        )
    for i, players in enumerate(team_players):
        teams[i].players = [p.id for p in players]
        all_players += players
    return all_players


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
    parser = argparse.ArgumentParser(
        description="Run a league season simulation with n teams."
    )
    parser.add_argument(
        "--n-teams",
        "-t",
        help="The number of team in the simulation",
        type=int,
        default=32,
    )
    parser.add_argument(
        "--force-gen",
        "-f",
        help="Force the sim to generate a new dataset of teams",
        action="store_true",
        default=False,
    )
    args = parser.parse_args()

    start = datetime.now()
    data_file = Path(DATA_DIR, DATA_FILE)
    if data_file.is_file() and not args.force_gen:
        print("Loading existing dataset...")
        annotation_tree = ET.parse(data_file)
        root = annotation_tree.getroot()
        players, teams = xml_to_save_state(root)

    else:
        data_gen_start = datetime.now()
        print("Generating new dataset...")
        teams = generate_teams(n_teams=args.n_teams)
        players = generate_players(teams)
        root = save_state_to_xml(teams=teams, pawns=players)
        ET.ElementTree(root).write(data_file)
        print(f"Generated data for {len(teams)} teams and {len(players)} players.")
        print(f"Generated in {datetime.now() - data_gen_start}")
    print("Complete.")

    players_df = generate_players_df(players)

    league = League(teams=teams[: args.n_teams], players=players)

    league_start = datetime.now()
    league.run_season()
    league_time = datetime.now() - league_start

    league.player_stats.to_csv(f"data/season_{league.year}_player_stats.csv")
    league.team_stats.to_csv(f"data/season_{league.year}_team_stats.csv")

    print_standings(league)
    print_stats(league)

    games = league.seasons[0].schedule

    print(f"\nTotal games: {len(games)}")
    print(f"Total teams: {len(teams)}")
    print(f"Completed in: {league_time}")
    print(f"Avg. per game: {league_time/len(games)}")
    print(datetime.now() - start)
