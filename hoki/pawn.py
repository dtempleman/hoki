from dataclasses import dataclass
from enum import Enum, auto

from hoki import faker
from hoki.statblock import StatBlock, get_df_row
from hoki.body import Body


class position(Enum):
    GOALIE = auto()
    CENTRE = auto()
    WING_L = auto()
    WING_R = auto()
    DEFENCE_L = auto()
    DEFENCE_R = auto()


class dominant_hands(Enum):
    RIGHT = auto()
    LEFT = auto()


@dataclass
class Pawn:
    id: int
    name: str
    position: position
    shoots: dominant_hands
    stats: StatBlock
    jersey_num: int
    body: Body

    def __str__(self):
        return f"{self.name}: {self.position.name} #{self.jersey_num}"

    def get_player_rating(self):
        x = 0.0
        for v in get_df_row(self.stats):
            x += v
        return round(x / len(get_df_row(self.stats)), 2)


def generate_player_name():
    return faker.name()
