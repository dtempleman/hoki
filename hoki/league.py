from typing import List
import itertools
import random
import pandas as pd

from hoki.team import Team
from hoki.pawn import Pawn
from hoki.game import GameManager, STATS_NAMES


class Season:
    def __init__(self, teams: List[Team]) -> None:
        self.teams = teams
        self.schedule = self.generate_schedule()

    def generate_schedule(self) -> List:
        # generate a scheduel where every team plays each other once
        games = list(itertools.combinations(self.teams, 2))
        random.shuffle(games)
        return games


class League:
    def __init__(self, teams: List[Team], players: List[Pawn]) -> None:
        self.year = 0
        self.teams = teams
        self.players = players

        # dataframes that contains team and player stats, this will be updated after every game
        player_stats_headers = ["games"] + STATS_NAMES
        team_stats_headers = ["wins", "losses", "overtime-losses"]
        self.team_stats = self._generate_inital_team_stats(team_stats_headers)
        self.player_stats = self._generate_inital_player_stats(player_stats_headers)

        # a list of seasons for a given league
        self.seasons = []
        self.add_season_schedule()

    def add_season_schedule(self):
        # generate and add a schedule to self.seasons
        self.seasons.append(Season(self.teams))

    def run_season(self):
        # run the current season schedule
        games = [
            GameManager(teams[0], teams[1], self.players)
            for teams in self.seasons[self.year].schedule
        ]
        for game in games:
            self.run_game(game)
        self.year += 1

    def run_game(self, game):
        game.run()
        self._apply_game_stats(game)

    def _apply_player_stats(self, game):
        game_stats = game.state.boxscore.get_stats().set_index(["player-id", "player"])
        game_stats["games"] = 1
        game_stats = game_stats.drop("team", axis=1)
        self.player_stats = game_stats.add(self.player_stats, fill_value=0)

    def _apply_team_stats(self, game):
        game_score = game.state.boxscore.get_score()
        game_score.sort_values(by=["goals"])
        game_score["wins"] = 0
        game_score["overtime-losses"] = 0
        game_score["losses"] = 0

        game_score.loc[0, "wins"] = 1
        if game.state.period > 3:
            game_score.loc[1, "overtime-losses"] = 1
        else:
            game_score.loc[1, "losses"] = 1

        game_score = game_score.drop(["goals", "shots"], axis=1)
        game_score.set_index("team", inplace=True)
        self.team_stats = game_score.add(self.team_stats, fill_value=0)

    def _apply_game_stats(self, game):
        self._apply_player_stats(game)
        self._apply_team_stats(game)

    def _generate_inital_player_stats(self, stats_headers):
        player_stats = pd.DataFrame(columns=["player-id", "player"] + stats_headers)
        for player in self.players:
            player_stats.loc[len(player_stats)] = [player.id, player.name] + [
                0 for _ in stats_headers
            ]
        return player_stats.set_index(["player-id", "player"])

    def _generate_inital_team_stats(self, stats_headers):
        team_stats = pd.DataFrame(columns=["team"] + stats_headers)
        for team in self.teams:
            team_stats.loc[len(team_stats)] = [team.name] + [0 for _ in stats_headers]
        return team_stats.set_index(["team"])

    def print_standings(self):
        df = self.team_stats
        df["points"] = df["wins"] * 2 + df["overtime-losses"]
        print(df.sort_values(by=["points"], ascending=False))

    def print_stats(self):
        df = self.player_stats
        df["points"] = df["goals"] + df["assists"]
        print(df.sort_values(by=["points"], ascending=False))
