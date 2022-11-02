from dataclasses import dataclass
from enum import Enum, auto
import random
import time
import pandas as pd

from hoki.player import Player


class zone(Enum):
    OFFENCE = auto()
    DEFENCE = auto()
    NEWTRAL = auto()
    OUT_OF_PLAY = auto()


@dataclass
class Puck:
    zone: zone = zone.OUT_OF_PLAY
    player: Player = None


class GameEvents:
    def __init__(self, home, away) -> None:
        pass

    def add_event(self):
        pass

    def print_event(self):
        pass


class BoxScore:
    def __init__(self, home, away) -> None:
        idx = 0
        data = {}
        stats_names = ["goals", "shots", "faceoffs", "faceoffs-won"]
        for team in [home, away]:
            for player in team.players:
                data[idx] = [
                    team.name,
                    player.id,
                    player.name,
                ]
                for _ in stats_names:
                    data[idx].append(0)
                idx += 1
        self.stats = pd.DataFrame.from_dict(
            data, orient="index", columns=["team", "player-id", "player"] + stats_names
        )

    def increment_stat(self, player, stat):
        self.stats.loc[self.stats["player-id"] == player.id, stat] += 1

    def add_shot(self, player, goal=False):
        self.increment_stat(player, "shots")
        if goal:
            self.increment_stat(player, "goals")

    def add_faceoff(self, player, won=False):
        self.increment_stat(player, "faceoffs")
        if won:
            self.increment_stat(player, "faceoffs-won")

    def get_score(self):
        teams = self.stats["team"].unique()
        scores = {
            "team": teams,
            "goals": [
                self.stats[self.stats["team"] == team]["goals"].sum() for team in teams
            ],
            "shots": [
                self.stats[self.stats["team"] == team]["shots"].sum() for team in teams
            ],
        }
        return pd.DataFrame(data=scores)

    def is_tied(self):
        return len(self.get_score()["goals"].unique()) == 1

    def __str__(self) -> str:
        return str(self.get_score())


class Game:
    def __init__(self, home_team, away_team) -> None:

        self.timer = 30
        self.num_periods = 3
        self.current_period = 1
        self.posession_stack = []

        self.home_team = home_team
        self.away_team = away_team

        # TODO: both player_by_id and team_by_id are set in the _generate_lineups() function.
        # it is not clear that this is happening
        self.players_by_id = {}
        self.teams_by_id = {}
        self.lineups = self._generate_lineups()

        self.puck = Puck(zone=zone.OUT_OF_PLAY)
        self.boxscore = BoxScore(self.home_team, self.away_team)

    def get_player_team(self, player):
        return self.lineups.loc[self.lineups["player-id"] == player.id].team.unique()[0]

    def get_team_players(self, team):
        return self.lineups.loc[self.lineups["team"] == team.name]

    def get_opponent_team(self, player):
        return self.lineups.loc[
            self.lineups["team"] != self.get_player_team(player)
        ].team.unique()[0]

    def get_home_team(self):
        return self.lineups.loc[self.lineups["home"] is True]

    def get_away_team(self):
        return self.lineups.loc[self.lineups["home"] is False]

    def get_random_player(self, team=None):
        if team:
            player = self.get_team_players(team).sample()
        else:
            player = self.lineups.sample()
        return self.players_by_id[player["player-id"].values[0]]

    def _generate_lineups(self):
        idx = 0
        data = {}
        for home, team in enumerate([self.away_team, self.home_team]):
            self.teams_by_id[team.name] = team
            for player in team.players:
                self.players_by_id[player.id] = player
                data[idx] = [
                    home == 1,
                    team.name,
                    player.id,
                    player.name,
                    player.position,
                    True,
                ]
                idx += 1
        return pd.DataFrame.from_dict(
            data,
            orient="index",
            columns=["home", "team", "player-id", "player", "position", "on-ice"],
        )

    def player_shoot(self, player, timer):
        chance = random.uniform(0, 1)
        goal = False
        if chance < player.stats.accuracy:
            self.boxscore.add_shot(player, goal=True)
            self.puck.zone = zone.OUT_OF_PLAY
            self.puck.player = None
            action = "scored!"
            goal = True
        else:
            self.boxscore.add_shot(player)
            self.puck.player = self.get_random_player(
                team=self.teams_by_id[self.get_opponent_team(player)]
            )
            action = f"missed, now {self.puck.player.name} has the puck."
        print(f"{self.current_period}:{timer}: {player.name} {action}")
        return goal

    def player_pass(self, player_a, player_b, timer):
        chance = random.uniform(0, 1)
        if chance < (player_a.stats.accuracy + player_b.stats.positioning) / 2:
            self.puck.player = player_b
        else:
            self.puck.player = self.get_random_player()
        print(
            f"{self.current_period}:{timer}: {player_a.name} passed to {self.puck.player.name}"
        )

    def face_off(self, player_a, player_b, timer):
        diff = player_a.stats.strength - player_b.stats.strength
        chance = random.uniform(0, 1)
        if chance < 0.5 + diff:
            self.puck.player = player_a
        else:
            self.puck.player = player_b
        self.puck.zone = zone.NEWTRAL
        self.boxscore.add_faceoff(player_a, won=player_a is self.puck.player)
        self.boxscore.add_faceoff(player_b, won=player_b is self.puck.player)
        print(f"{self.current_period}:{timer}: faceoff won by {self.puck.player.name}")

    def do_something(self, player, timer):
        team = self.teams_by_id[self.get_player_team(player)]
        option = random.randint(0, 1)
        if option == 0:
            return self.player_shoot(player, timer)
        elif option == 1:
            player_b = team.players[random.randint(0, len(team.players) - 1)]
            self.player_pass(player, player_b, timer)

    def run_period(self, length, sleep=1, overtime=False):
        while length > 0:
            if self.puck.zone == zone.OUT_OF_PLAY:
                self.face_off(
                    self.home_team.players[-1], self.away_team.players[-1], length
                )
            else:
                goal = self.do_something(self.puck.player, length)
                if goal and overtime:
                    return
            length -= 1
            time.sleep(sleep)

    def run(self):
        for _ in range(self.num_periods):
            self.run_period(self.timer, 0.25)
            self.current_period += 1
        overtimes = 1
        while self.boxscore.is_tied():
            print()
            self.print_score()
            print(f"Game is tied. running overtime period {overtimes}")
            self.run_period(self.timer, 0.25, overtime=True)

    def print_score(self):
        print(self.boxscore.get_score())
