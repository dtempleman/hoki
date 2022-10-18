from dataclasses import dataclass
from enum import Enum, auto
import random
from models import Player
import time


class zone(Enum):
    OFFENCE = auto()
    DEFENCE = auto()
    NEWTRAL = auto()
    OUT_OF_PLAY = auto()


@dataclass
class Puck:
    zone: zone = zone.OUT_OF_PLAY
    player: Player = None


def shoot(game, player):
    chance = random.randint(0, 1)

    if chance == 0:
        game.score[game.team_by_player[player.id].name]["goals"] += 1
        game.puck.zone = zone.OUT_OF_PLAY
        game.puck.player = None
        action = "scored!"
    elif chance == 1:
        idx = random.randint(0, len(game.on_ice_players) - 1)
        game.puck.player = game.on_ice_players[idx]
        action = f"missed, now {game.puck.player} has the puck."
    print(f"{game.timer}: {player} {action}")


def pass_to_player(game, player, target_player):
    chance = random.randint(0, 1)
    if chance == 0:
        game.puck.player = target_player
    elif chance == 1:
        game.puck.player = game.on_ice_players[random.randint(0, len(game.on_ice_players) - 1 )]
    print(f"{game.timer}: {player} passed to {game.puck.player}")


def face_off(game, player_a, player_b):
    game.puck.player = [player_a, player_b][random.randint(0, 1)]
    game.puck.zone = zone.NEWTRAL
    print(f"{game.timer}: faceoff won by {game.puck.player}")


def do_something(game, player):

    team = game.team_by_player[player.id]

    option = random.randint(0, 1)
    if option == 0:
        shoot(game, player)
    elif option == 1:
        player_b = team.players[random.randint(0, len(team.players) - 1)]
        pass_to_player(game, player, player_b)


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

        self.score = {
            self.home_team.name: dict(goals=0),
            self.away_team.name: dict(goals=0),
        }


    def run(self):
        while self.timer > 0:
            if self.puck.zone == zone.OUT_OF_PLAY:
                face_off(self, self.home_team.players[-1], self.away_team.players[-1])
            else:
                do_something(self, self.puck.player)
            
            self.timer -= 1
            time.sleep(1)

    def print_score(self):
        print(f"HOME: {self.home_team.name}: {self.score[self.home_team.name]['goals']}")
        print(f"AWAY: {self.away_team.name}: {self.score[self.away_team.name]['goals']}")

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

    # for team in teams:
    #     print(team)

    game = Game(
        home_team=teams[0],
        away_team=teams[1]
    )

    game.run()
    game.print_score()
