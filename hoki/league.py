from typing import List
import pandas as pd

from hoki.team import Team


class Season:
    def __init__(self, teams: List[Team]) -> None:
        self.schedule = self.build_schedule()

    def build_schedule(self) -> pd.Dataframe:
        pass


class League:
    def __init__(self, teams: List[Team], year: int) -> None:
        self.teams = teams
        self.year = year

        # dataframe that contains team stats, this will be updated after every game
        self.standings = None

        # a list of games to be played in a season
        self.seasons = []
        self.add_season_schedule()

    def add_season_schedule(self):
        # generate and add a schedule to self.seasons
        self.seasons.append(Season(self.teams))

    def run_season(self, season):
        # run a given season schedule
        pass

    def run_next_game(self):
        pass
