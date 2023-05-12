from dataclasses import dataclass, field
from typing import List

import pandas as pd


@dataclass
class GameState:
    """
    A dataclass containg the game state data
    """

    # the player id of the puck
    puck_player: int
    # the zone id of the puck
    puck_zone: int

    # a dict of lists of player ids keyed by team id
    players_by_team: dict
    # a dict of team ids keyed by player id
    team_by_player: dict

    # a dict of lists of player ids keyed by zone id
    player_by_zone: dict
    # a dict of zone ids keyed by player id
    zone_by_player: dict

    # the current score and stats
    boxscore: pd.DataFrame
    # the current time remaining in period in seconds
    time: int
    # the current period
    period: int
    # if the game is currently in overtime
    overtime: bool = False

    game_log: List[str] = field(default_factory=lambda: [])
