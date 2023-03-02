from dataclasses import dataclass, fields
from typing import List
import random


STAT_NAMES = [
    "positioning",
    "accuracy",
    "strength",
    "iq",
    "health",
    "stability",
    "speed",
    "aggresivness",
]


@dataclass
class StatBlock:
    positioning: float = 0
    accuracy: float = 0
    strength: float = 0
    iq: float = 0

    # currently not being used
    health: float = 0  # used for recovering from injuries
    stability: float = 0  # used for withstanding checks and hits
    speed: float = 0  # used to see how far to move in a game tick
    aggresivness: float = 0  # used to determin if the player will hit

    shooting_hand: int = 0  # 0 = Right, 1 = Left


def get_df_row(stats: StatBlock) -> List:
    return [getattr(stats, field.name) for field in fields(stats)]


def generate_inital_stats():
    return StatBlock(
        positioning=round(random.uniform(0, 1), 2),
        accuracy=round(random.uniform(0, 1), 2),
        strength=round(random.uniform(0, 1), 2),
        iq=round(random.uniform(0, 1), 2),
        health=round(random.uniform(0, 1), 2),
        stability=round(random.uniform(0, 1), 2),
        speed=round(random.uniform(0, 1), 2),
        aggresivness=round(random.uniform(0, 1), 2),
        shooting_hand=random.randint(0, 1),
    )
