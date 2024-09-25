import random
from dataclasses import dataclass, field
from typing import List

from hoki.models.pawn import Pawn

# the starting plase when determining a players statistics
INITAIL_CANDIDATES = [0, 50, 100]


@dataclass
class Scout(Pawn):
    initial_distribution: List[int] = field(default_factory=lambda: [])
    efficiency: float


class Scout2:
    def __init__(self) -> None:
        self.rating = random.randint(0, 100)

        self.initial_distribution = self._calculate_inital_distribution()
        self.efficiency = self._calculate_efficiency()

        self.report = {}

    def update_scouting_report(self, player):
        # update the scouting report for a given payer

        if player.id not in self.report:
            self.init_report(player)

        player_report = self.report[player.id]

        for statistic in player.statistics:
            starting_value = player_report[statistic.name]["value"]
            scouting_diff = statistic.value - starting_value
            scouting_progress = round(scouting_diff * self.efficiency)
            result_value = starting_value + scouting_progress
            confidence = 100 - scouting_progress

            player_report[statistic.name] = {
                "value": result_value,
                "confidence": confidence,
            }

        self.report[player.id] = player_report

    def init_report(self, player):
        # create an initail scouting report for a player
        # all stats will begin at one of the INITIAL_CANDIDATES values
        report = {}

        for statistic in player.statistics:
            sorted_list = sorted(
                INITAIL_CANDIDATES, key=lambda x: abs(statistic.value - x)
            )
            report[statistic.name] = {
                "value": random.choice(sorted_list, self.initial_distribution, 1),
                "confidence": 0,
            }
        self.report[player.id] = report

    def _calculate_inital_distribution(self):
        distributions = {
            25: [0.0, 0.3, 0.7],
            50: [0.1, 0.4, 0.5],
            75: [0.4, 0.5, 0.1],
            100: [0.7, 0.3, 0.0],
        }
        for d in distributions:
            if d <= self.rating:
                return distributions[d]

    def _calculate_efficiency(self):
        efficiencies = {
            25: 0.05,
            50: 0.1,
            75: 0.25,
            100: 0.5,
        }
        for e in efficiencies:
            if e <= self.rating:
                return efficiencies[e]

    def _level_up(self):
        self.initial_distribution = self._calculate_inital_distribution()
        self.efficiency = self._calculate_efficiency()
