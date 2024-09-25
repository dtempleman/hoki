from dataclasses import dataclass
from typing import List

from hoki.models.player import Player
from hoki.models.savable import Savable
from hoki.models.team import Team


@dataclass
class SaveState(Savable):
    players: List[Player]
    teams: List[Team]
