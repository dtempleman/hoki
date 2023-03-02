from dataclasses import dataclass, field
from typing import List
from enum import Enum, auto
import random
import time
import pandas as pd

from hoki.pawn import Pawn


SLEEP = 0  # seconds between game ticks
STATS_NAMES = ["goals", "assists", "shots", "faceoffs", "faceoffs-won"]


class zone(Enum):
    OFFENCE = auto()
    DEFENCE = auto()
    NEWTRAL = auto()
    OUT_OF_PLAY = auto()


@dataclass
class Puck:
    zone: zone = zone.OUT_OF_PLAY
    player: Pawn = None


class BoxScore:
    def __init__(self, home, away, players_by_id) -> None:
        idx = 0
        data = {}
        for team in [home, away]:
            for player_id in team.players:
                data[idx] = [
                    team.name,
                    players_by_id[player_id].id,
                    players_by_id[player_id].name,
                ]
                for _ in STATS_NAMES:
                    data[idx].append(0)
                idx += 1
        self.stats = pd.DataFrame.from_dict(
            data, orient="index", columns=["team", "player-id", "player"] + STATS_NAMES
        )

    def increment_stat(self, player, stat):
        self.stats.loc[self.stats["player-id"] == player.id, stat] += 1

    def add_assist(self, player):
        self.increment_stat(player, "assists")

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

    def get_score_dict(self):
        return self.get_score().to_dict()

    def get_stats(self):
        return self.stats

    def get_stats_dict(self):
        return self.stats.to_dict()

    def __str__(self) -> str:
        return str(self.get_score())


@dataclass
class GameState:
    boxscore: pd.DataFrame
    players_positions: dict  # contains player position data
    time: int  # the current game time
    period: int  # the current period
    puck: dict
    paused: bool = True
    overtime: bool = False
    game_log: List[str] = field(default_factory=lambda: [])


class PossessionStack:
    def __init__(self):
        self.stack = []

    def add_player(self, player):
        # if the most recent player on the stack is on ther other team, reset stack
        # add a player to the stack if they are not already at the top
        if player:
            current_player = self.stack[-1].name if len(self.stack) > 0 else None
            if current_player is None or current_player != player.name:
                self.stack.append(player)

    def get_assist(self):
        # return the player who assisted the goal, if no player return None
        return self.stack[-2] if self.size() > 1 else None

    def reset(self):
        self.stack = []

    def size(self):
        return len(self.stack)

    def print_stack(self):
        for player in self.stack:
            print(player.name)


class GameManager:
    def __init__(self, home_team, away_team, pawns) -> None:
        self.teams_by_id = {
            home_team.name: home_team,
            away_team.name: away_team,
        }
        self.players_by_id = {player.id: player for player in pawns}

        self.home_team = home_team
        self.away_team = away_team
        self.boxscore = BoxScore(self.home_team, self.away_team, self.players_by_id)

        self.puck = Puck(zone=zone.OUT_OF_PLAY)
        self.timer = 30
        self.game_tick = 1
        self.num_periods = 3
        self.current_period = 1
        self.completed = False
        self.posession_stack = PossessionStack()
        self.lineups = self._generate_lineups()

        self.state = GameState(
            boxscore=self.boxscore,
            players_positions=self.lineups,
            time=self.timer,
            period=1,
            puck={"zone": self.puck.zone, "player": self.puck.player},
        )

    def get_player_team(self, player):
        return self.lineups.loc[self.lineups["player-id"] == player.id].team.unique()[0]

    def get_team_players(self, team):
        return self.lineups.loc[self.lineups["team"] == team.name]

    def get_opponent_team(self, player):
        return self.lineups.loc[
            self.lineups["team"] != self.get_player_team(player)
        ].team.unique()[0]

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
            for player_id in team.players:
                data[idx] = [
                    home == 1,
                    team.name,
                    self.players_by_id[player_id].id,
                    self.players_by_id[player_id].name,
                    self.players_by_id[player_id].position,
                    True,
                ]
                idx += 1
        return pd.DataFrame.from_dict(
            data,
            orient="index",
            columns=["home", "team", "player-id", "player", "position", "on-ice"],
        )

    def log_event(self, text):
        self.state.game_log.append(f"{self.state.period}:{self.state.time}: {text}")

    def reset_puck(self):
        self.puck.zone = zone.OUT_OF_PLAY
        self.puck.player = None

    def score_goal(self, player):
        self.reset_puck()
        pass

    def player_shoot(self, player):
        chance = random.uniform(0, 1)
        if chance < player.stats.accuracy:
            assister = self.posession_stack.get_assist()
            if assister and self.get_player_team(assister) == self.get_player_team(
                player
            ):
                self.boxscore.add_assist(assister)
            self.score_goal(player)
            self.boxscore.add_shot(player, goal=True)
        else:
            self.boxscore.add_shot(player)
            self.puck.player = self.get_random_player(
                team=self.teams_by_id[self.get_opponent_team(player)]
            )

    def player_pass(self, player_a, player_b):
        chance = random.uniform(0, 1)
        if chance < (player_a.stats.accuracy + player_b.stats.positioning) / 2:
            self.puck.player = player_b
        else:
            self.puck.player = self.get_random_player()

    def face_off(self, player_a, player_b):
        diff = player_a.stats.strength - player_b.stats.strength
        chance = random.uniform(0, 1)
        if chance < 0.5 + diff:
            self.puck.player = player_a
        else:
            self.puck.player = player_b
        self.puck.zone = zone.NEWTRAL
        self.boxscore.add_faceoff(player_a, won=player_a is self.puck.player)
        self.boxscore.add_faceoff(player_b, won=player_b is self.puck.player)

    def do_something(self, player):
        # TODO:
        team = self.teams_by_id[self.get_player_team(player)]
        option = random.randint(0, 1)
        if option == 0:
            return self.player_shoot(player)
        elif option == 1:
            player_id = team.players[random.randint(0, len(team.players) - 1)]
            player_b = self.players_by_id[player_id]
            self.player_pass(player, player_b)

    def is_tied(self) -> bool:
        """return True if the game is currently tied else Flase"""
        return self.boxscore.is_tied()

    def run(self):
        while not self.completed:
            self.completed = self.increment_state()

    def increment_state(self) -> bool:
        """
        increment the game by 1 game_tick and return True if the game is over.
        """
        self.run_state()
        if self.state.time > 0:
            if self.state.overtime and not self.is_tied():
                return True
            self.state.time -= self.game_tick
        elif self.state.period < self.num_periods:
            self.state.period += 1
            self.state.time = self.timer
        elif self.is_tied():
            self.state.period += 1
            self.state.time = self.timer
            self.state.overtime = True
        else:
            return True

    def run_state(self):
        if self.puck.zone == zone.OUT_OF_PLAY:
            self.face_off(
                self.players_by_id[self.home_team.players[-1]],
                self.players_by_id[self.away_team.players[-1]],
            )
        else:
            self.do_something(self.puck.player)
        self.posession_stack.add_player(self.puck.player)
        # self.posession_stack.print_stack()
        time.sleep(SLEEP)
