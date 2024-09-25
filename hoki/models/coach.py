from dataclasses import dataclass

from hoki.models.pawn import Pawn
from hoki.models.player import Player


@dataclass
class Coach(Pawn):
    method: str

    @classmethod
    def from_player(cls, player: Player):
        return cls(name=player.name, stats=player.stats, method=player.position.name)
