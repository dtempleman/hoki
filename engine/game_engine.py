from dataclasses import dataclass
from enum import Enum, auto
import random
import time
import pandas as pd

from player import Player, Team, generate_player_name, stick_hand, generate_inital_stats, position


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
        self.stats = pd.DataFrame.from_dict(data, orient='index', columns=["team", "player-id", "player"] + stats_names)

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
        score = dict()
        for team in self.stats["team"].unique():
            score[team] = self.stats[self.stats["team"] == team]['goals'].sum()
        return score

    def __str__(self) -> str:
        return str(self.get_score())


class Game:
    def __init__(self, home_team, away_team) -> None:

        self.timer = 30
        self.pass_stack = []

        self.home_team = home_team
        self.away_team = away_team

        self.players_by_id = {}
        self.teams_by_id = {}

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

        self.lineups = pd.DataFrame.from_dict(data, orient='index', columns=["home", "team", "player-id", "player", "position", "on-ice"])

        self.puck = Puck(zone=zone.OUT_OF_PLAY)
        self.boxscore = BoxScore(self.home_team, self.away_team)

    def get_player_team(self, player):
        return self.lineups.loc[self.lineups["player-id"] == player.id].team.unique()[0]

    def get_team_players(self, team):
        return self.lineups.loc[self.lineups["team"] == team.name]

    def get_opponent_team(self, player):
        return self.lineups.loc[self.lineups["team"] != self.get_player_team(player)].team.unique()[0]

    def get_home_team(self):
        return self.lineups.loc[self.lineups["home"] == True]
    
    def get_away_team(self):
        return self.lineups.loc[self.lineups["home"] == False]

    def get_random_player(self, team=None):
        if team:
            player = self.get_team_players(team).sample()
        else:
            player = self.lineups.sample()
        return self.players_by_id[player["player-id"].values[0]]

    def player_shoot(self, player):
        chance = random.uniform(0, 1)
        if chance < player.stats.accuracy:
            self.boxscore.add_shot(player, goal=True)
            self.puck.zone = zone.OUT_OF_PLAY
            self.puck.player = None
            action = "scored!"
        else:
            self.boxscore.add_shot(player)
            self.puck.player = self.get_random_player(
                team=self.teams_by_id[self.get_opponent_team(player)]
            )
            action = f"missed, now {self.puck.player.name} has the puck."
        print(f"{self.timer}: {player.name} {action}")

    def player_pass(self, player_a, player_b):
        chance = random.uniform(0, 1)
        if chance < (player_a.stats.accuracy + player_b.stats.positioning / 2):
            self.puck.player = player_b
        else:
            self.puck.player = self.get_random_player()
        print(f"{self.timer}: {player_a.name} passed to {self.puck.player.name}")

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
        print(f"{self.timer}: faceoff won by {self.puck.player.name}")

    def do_something(self, player):

        team = self.teams_by_id[self.get_player_team(player)]

        option = random.randint(0, 1)
        if option == 0:
            self.player_shoot(player)
        elif option == 1:
            player_b = team.players[random.randint(0, len(team.players) - 1)]
            self.player_pass(player, player_b)

    def run(self):
        while self.timer > 0:
            if self.puck.zone == zone.OUT_OF_PLAY:
                self.face_off(self.home_team.players[-1], self.away_team.players[-1])
            else:
                self.do_something(self.puck.player)
            
            self.timer -= 1
            time.sleep(0.5)

    def print_score(self):
        print(self.boxscore.get_score())


if __name__ == "__main__":
    positions = [
        position.GOALIE,
        position.DEFENCE,
        position.DEFENCE,
        position.FORWARD,
        position.FORWARD,
        position.FORWARD,
    ]

    teams = [
        Team(name="Red"),
        Team(name="Blue")
    ]
    i = 0
    for t in teams:
        for p in positions:
            t.players.append(
                Player(
                    name=generate_player_name(),
                    position=p,
                    id=i,
                    shoots=stick_hand.LEFT if random.randint(0, 1) == 0 else stick_hand.RIGHT,
                    stats=generate_inital_stats(),
                )
            )
            i += 1

    game = Game(
        home_team=teams[0],
        away_team=teams[1],
    )

    game.run()

    for team in teams:
        for player in team.players:
            print(player)

    game.print_score()
    print(game.boxscore.stats)
