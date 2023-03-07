from dataclasses import dataclass, field
from typing import List

from hoki import faker


@dataclass
class Team:
    """
    A dataclass to hold the data from a single team.

    Attributes:
        name (str): the name of the team.
        players (List[Pawn]): a list of all player in the team.
    """

    name: str
    players: List[int] = field(default_factory=lambda: [])

    def __str__(self):
        """return a string representation of the team. 'team name:\nplayer name\n...'"""
        string = f"{self.name}:\n"
        for p in self.players:
            string += f"{p}\n"
        return string


def generate_team_name():
    """Return a random team name. '<random city> <random word>s'"""
    return faker.city() + " " + faker.word() + "s"
