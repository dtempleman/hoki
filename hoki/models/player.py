from dataclasses import dataclass
from enum import Enum, auto

from hoki.models.body import Body, dominant_hands
from hoki.models.pawn import Pawn
from hoki.models.statblock import get_df_row


class position(Enum):
    """Enumerate the player positions."""

    GOALIE = auto()
    CENTRE = auto()
    WING_L = auto()
    WING_R = auto()
    DEFENCE_L = auto()
    DEFENCE_R = auto()


@dataclass
class Player(Pawn):
    position: position
    shoots: dominant_hands  # should be removed and replaced with the body.dominant hand
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
