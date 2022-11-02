from dataclasses import dataclass
from enum import Enum, auto
import random
from typing import List

from hoki import faker


class position(Enum):
    GOALIE = auto()
    CENTRE = auto()
    WING_L = auto()
    WING_R = auto()
    DEFENCE_L = auto()
    DEFENCE_R = auto()


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

    def df_row(self) -> List:
        return [self.positioning, self.accuracy, self.strength, self.iq]


@dataclass
class Player:
    id: int
    name: str
    position: position
    shoots: stick_hand
    stats: Stats
    jersey_num: int

    def __str__(self):
        return f"{self.name}: {self.position.name} #{self.jersey_num} | {self.stats}"

    def get_player_rating(self):
        x = 0.0
        for v in self.stats.df_row():
            x += v
        return round(x / len(self.stats.df_row()), 2)


def generate_inital_stats():
    return Stats(
        positioning=round(random.uniform(0, 1), 2),
        accuracy=round(random.uniform(0, 1), 2),
        strength=round(random.uniform(0, 1), 2),
        iq=round(random.uniform(0, 1), 2),
    )


def generate_player_name():
    return faker.name()
