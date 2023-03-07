from dataclasses import dataclass
from enum import Enum, auto

from hoki import faker
from hoki.statblock import StatBlock, get_df_row
from hoki.body import Body, dominant_hands


class position(Enum):
    """Enumerate the player positions."""

    GOALIE = auto()
    CENTRE = auto()
    WING_L = auto()
    WING_R = auto()
    DEFENCE_L = auto()
    DEFENCE_R = auto()


@dataclass
class Pawn:
    """
    A dataclass to represent the a Pawn. Pawns are the representation of a person.

    Attributes:
        id (str): The pawn's id
        name (str): The pawn's name
        position (position): The pawn's position.
        shoots (dominant_hands): The pawn's dominant hand.
        stats (StatBlock): The pawn's stats.
        jersey_num (int): The pawn's jersey number.
        body (Body): The pawn's body.
    """

    id: int
    name: str
    position: position
    shoots: dominant_hands  # should be removed and replaced with the body.dominant hand
    stats: StatBlock
    jersey_num: int
    body: Body

    def __str__(self):
        """Return a string representation of the Pawn 'name: posotion #jersey number'"""
        return f"{self.name}: {self.position.name} #{self.jersey_num}"

    def get_player_rating(self):
        """Calculate and return the pawns rating. Calculated as the average of every stats."""
        x = 0.0
        for v in get_df_row(self.stats):
            x += v
        return round(x / len(get_df_row(self.stats)), 2)


def generate_player_name():
    """return a random name."""
    return faker.name()
