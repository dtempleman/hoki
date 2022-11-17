import random
import pandas as pd

from hoki.player import (
    Player,
    stick_hand,
    position,
    generate_player_name,
    generate_inital_stats,
)
from hoki.team import Team, Jersey, generate_team_name
from hoki.game_engine import Game
from hoki import faker
import json


if __name__ == "__main__":
    data = []

    positions = [
        position.GOALIE,
        position.DEFENCE_L,
        position.DEFENCE_R,
        position.WING_L,
        position.WING_R,
        position.CENTRE,
    ]

    teams = [
        {
            "pk": i + 1,
            "model": "team.Team",
            "fields": {
                "name": faker.word() + "s",
                "location": faker.city()
            }
        } for i in range(2)
    ]
    data += teams
    pk, spk = 1, 1
    for team in teams:
        team_nums = []
        for pos in positions:
            num = random.randint(0, 99)
            while num in team_nums:
                num += 1
            team_nums.append(num)
            data.append(
                {
                    "pk": pk,
                    "model": "team.Player",
                    "fields": {
                        "name": generate_player_name(),
                        "team": team["pk"],
                        "position": pos.name,
                        "jersey_num": num
                    }
                }
            )
            data.append(
                {
                    "pk": spk,
                    "model": "team.Stats",
                    "fields": {
                        "player": pk,
                        "positioning": round(random.uniform(0, 1), 2),
                        "accuracy": round(random.uniform(0, 1), 2),
                        "strength": round(random.uniform(0, 1), 2),
                        "iq": round(random.uniform(0, 1), 2),
                    }
                }
            )
            spk += 1
            pk += 1
    with open('team_data.json', 'w') as f:
        json.dump(data, f)
