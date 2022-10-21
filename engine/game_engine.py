from dataclasses import dataclass
from enum import Enum, auto
import random
import time
import pandas as pd

from models import Player


class zone(Enum):
    OFFENCE = auto()
    DEFENCE = auto()
    NEWTRAL = auto()
    OUT_OF_PLAY = auto()


@dataclass
class Puck:
    zone: zone = zone.OUT_OF_PLAY
    player: Player = None


class BoxScore:
    def __init__(self, home, away) -> None:
        idx = 0
        data = {}
        stats_names = ["goals"]
        for team in [home, away]:
            for player in team.players:
                data[idx] = [
                    team.name,
                    player.id,
                ]
                for _ in stats_names:
                    data[idx].append(0)
                idx += 1
        self.stats = pd.DataFrame.from_dict(data, orient='index', columns=["team", "player"] + stats_names)

    def add_goal(self, player):
        self.stats.loc[self.stats['player'] == player.id, 'goals'] += 1

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

        self.team_by_player = dict()
        self.on_ice_players = dict()
        for t in [self.home_team, self.away_team]:
            for p in t.players:
                self.team_by_player[p.id] = t
                self.on_ice_players[p.id] = p

        self.puck = Puck(zone=zone.OUT_OF_PLAY)
        self.boxscore = BoxScore(self.home_team, self.away_team)

    def player_shoot(self, player):
        chance = random.randint(0, 1)

        if chance == 0:
            self.boxscore.add_goal(player)
            self.puck.zone = zone.OUT_OF_PLAY
            self.puck.player = None
            action = "scored!"
        elif chance == 1:
            idx = random.randint(0, len(self.on_ice_players) - 1)
            self.puck.player = self.on_ice_players[idx]
            action = f"missed, now {self.puck.player} has the puck."
        print(f"{self.timer}: {player} {action}")

    def player_pass(self, player, target_player):
        chance = random.randint(0, 1)
        if chance == 0:
            self.puck.player = target_player
        elif chance == 1:
            self.puck.player = self.on_ice_players[random.randint(0, len(self.on_ice_players) - 1 )]
        print(f"{self.timer}: {player} passed to {self.puck.player}")

    def face_off(self, player_a, player_b):
        self.puck.player = [player_a, player_b][random.randint(0, 1)]
        self.puck.zone = zone.NEWTRAL
        print(f"{self.timer}: faceoff won by {self.puck.player}")

    def do_something(self, player):

        team = self.team_by_player[player.id]

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

    from models import Team, Player, position

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
                    name=f"player {i}",
                    position=p,
                    id=i
                )
            )
            i += 1

    game = Game(
        home_team=teams[0],
        away_team=teams[1]
    )

    game.run()
    game.print_score()
