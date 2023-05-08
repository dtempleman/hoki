import random
from dataclasses import dataclass, fields
from typing import List

# the names of the pawn statistics.
STAT_NAMES = [
    "positioning",
    "iq",
    "shooting",
    "passing",
    "save",
    "skate",
    "checking",
    "stable",
]


@dataclass
class StatBlock:
    """
    A dataclass containing all the pawn statistics.

    Attributes:
        positioning (float): The pawn's ability to get into the right position.
        accuracy (float): The pawn's shooting and passing accuracy.
        strength (float): The pawn's shooting power.
        iq (float): The pawn's ability to make the correct desision.
        health (float): used for recovering from injuries
        stability (float): used for withstanding checks and hits
        speed (float): used to see how far to move in a game tick
        aggresivness (float): used to determin if the player will hit
        shooting_hand (float): 0 = Right, 1 = Left
    """

    positioning: float = 0
    iq: float = 0
    shooting: float = 0
    passing: float = 0
    save: float = 0
    skate: float = 0
    checking: float = 0
    stable: float = 0

    shooting_hand: int = 0  # 0 = Right, 1 = Left


def get_df_row(stats: StatBlock) -> List:
    """Return a list representation of the stats. used when construction datafames."""
    return [getattr(stats, field.name) for field in fields(stats)]


def generate_inital_stats():
    """Generate a new Statblock with random values between 0 and 1 for each stat."""
    return StatBlock(
        positioning=round(random.uniform(0, 1), 2),
        iq=round(random.uniform(0, 1), 2),
        shooting=round(random.uniform(0, 1), 2),
        passing=round(random.uniform(0, 1), 2),
        save=round(random.uniform(0, 1), 2),
        skate=round(random.uniform(0, 1), 2),
        checking=round(random.uniform(0, 1), 2),
        stable=round(random.uniform(0, 1), 2),
        shooting_hand=random.randint(0, 1),
    )
