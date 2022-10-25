import random

from hoki.player import (
    Player,
    generate_player_name,
    stick_hand,
    generate_inital_stats,
    position,
)
from hoki.team import Team, generate_team_name
from hoki.game_engine import Game


if __name__ == "__main__":
    positions = [
        position.GOALIE,
        position.DEFENCE,
        position.DEFENCE,
        position.FORWARD,
        position.FORWARD,
        position.FORWARD,
    ]

    teams = [Team(name=generate_team_name()), Team(name=generate_team_name())]
    i = 0
    for t in teams:
        for p in positions:
            t.players.append(
                Player(
                    name=generate_player_name(),
                    position=p,
                    id=i,
                    shoots=stick_hand.LEFT
                    if random.randint(0, 1) == 0
                    else stick_hand.RIGHT,
                    stats=generate_inital_stats(),
                    jersey=random.randint(0, 99),
                )
            )
            i += 1

    game = Game(
        home_team=teams[0],
        away_team=teams[1],
    )

    game.run()
    game.print_score()

    for team in teams:
        for player in team.players:
            print(player)

    game.print_score()
    print(game.boxscore.stats)
