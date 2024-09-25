from dataclasses import dataclass

from hoki import faker
from hoki.models.savable import Savable
from hoki.models.statblock import StatBlock


@dataclass
class Pawn(Savable):
    """
    A template dataclass to represent the a Pawn. Pawns are the base representation of a person.

    Attributes:
        id (str): The pawn's id
        name (str): The pawn's name
        stats (StatBlock): The pawn's stats.
    """

    id: str
    name: str
    stats: StatBlock

    def get_overall_rating(self):
        return self.stats.get_overall_rating()


def generate_pawn_name():
    """return a random name."""
    return faker.name()
