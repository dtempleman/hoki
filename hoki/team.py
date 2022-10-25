from dataclasses import dataclass, field
from typing import List

from hoki.player import Player
from hoki import faker


@dataclass
class Team:
    name: str
    players: List[Player] = field(default_factory=lambda: [])

    def __str__(self):
        string = f"{self.name}:\n"
        for p in self.players:
            string += f"{p}\n"
        return string


@dataclass
class Contract:
    player: Player
    team: Team
    starting_year: str
    length: int
    aav: float


def generate_team_name():
    return faker.city() + " " + faker.word() + "s"
