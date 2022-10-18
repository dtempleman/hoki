from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List


class position(Enum):
    GOALIE = auto()
    FORWARD = auto()
    DEFENCE = auto()


@dataclass
class Player:
    id: int
    name: str
    position: position

    def __str__(self):
        return f"{self.name}: {self.position.name}"

@dataclass
class Team:
    name: str
    players: List[Player] = field(default_factory=lambda: [])

    def __str__(self):
        string = f"{self.name}:\n"
        for p in self.players:
            string += f"{p}\n"
        return string