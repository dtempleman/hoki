from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List
import random
import names


class position(Enum):
    GOALIE = auto()
    FORWARD = auto()
    DEFENCE = auto()


class stick_hand(Enum):
    RIGHT = auto()
    LEFT = auto()


@dataclass
class Stats:
    positioning: float = 0
    accuracy: float = 0
    strength: float = 0
    iq: float = 0

    def __str__(self) -> str:
        return f"[pos: {self.positioning}, acc: {self.accuracy}, str: {self.strength}, iq: {self.iq}]"


@dataclass
class Player:
    id: int
    name: str
    position: position
    shoots: stick_hand
    stats: Stats

    def __str__(self):
        return f"{self.name}: {self.position.name} | {self.stats}"


@dataclass
class Team:
    name: str
    players: List[Player] = field(default_factory=lambda: [])

    def __str__(self):
        string = f"{self.name}:\n"
        for p in self.players:
            string += f"{p}\n"
        return string


def generate_inital_stats():
    return Stats(
        positioning=round(random.uniform(0, 1), 2),
        accuracy=round(random.uniform(0, 1), 2),
        strength=round(random.uniform(0, 1), 2),
        iq=round(random.uniform(0, 1), 2),
    )


def generate_player_name():
    return names.get_full_name()