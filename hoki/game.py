from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum, auto
import random
import time
import pandas as pd

from hoki.pawn import Pawn
from hoki.team import Team


# the number of seconds between game ticks
SLEEP = 0

# the different stats to be tracked durring a game
STATS_NAMES = ["goals", "assists", "shots", "faceoffs", "faceoffs-won"]


class zone(Enum):
    """Enumerate the zones of play"""

    OFFENCE = auto()
    DEFENCE = auto()
    NEWTRAL = auto()
    OUT_OF_PLAY = auto()


@dataclass
class Puck:
    """
    A dataclass representing the puck and the current pawn that has possession.

    Attributes:
        zone (zone): The current zone the puck is in.
        player (Pawn): The Pawn that has possession. None if not Pawn has possession.
    """

    zone: zone = zone.OUT_OF_PLAY
    player: Pawn = None


class BoxScore:
    """
    A class to manage the a games score and stats.

    Attributes:
        stats (pd.DataFrame): A dataframe containing the stats for all the players.

    Args:
        home (Team): The team with home ice advantage.
        away (Team): The visiting team.
        players_by_id (dict[Pawn]): A dict of players keyed by their ids.
    """

    def __init__(self, home: Team, away: Team, players_by_id: Dict[int, Pawn]) -> None:
        idx = 0
        data = {}
        for team in [home, away]:
            for player_id in team.players:
                data[idx] = [
                    team.name,
                    players_by_id[player_id].id,
                    players_by_id[player_id].name,
                ]
                for _ in STATS_NAMES:
                    data[idx].append(0)
                idx += 1
        self.stats = pd.DataFrame.from_dict(
            data, orient="index", columns=["team", "player-id", "player"] + STATS_NAMES
        )

    def increment_stat(self, player: Pawn, stat: str) -> None:
        """Increment the players given statistic by 1."""
        self.stats.loc[self.stats["player-id"] == player.id, stat] += 1

    def add_assist(self, player: Pawn) -> None:
        """Increment the players assists by 1."""
        self.increment_stat(player, "assists")

    def add_shot(self, player: Pawn, goal: bool = False) -> None:
        """Increment the players shots by one. If goal, increment its goals also."""
        self.increment_stat(player, "shots")
        if goal:
            self.increment_stat(player, "goals")

    def add_faceoff(self, player: Pawn, won: bool = False) -> None:
        """Increment the players faceoffs. If won, increment its won-faceoffs also."""
        self.increment_stat(player, "faceoffs")
        if won:
            self.increment_stat(player, "faceoffs-won")

    def get_score(self) -> pd.DataFrame:
        """
        Return a DataFrame with the current games score.

        Returns:
            a pd.DataFrame of the teams, goals, and shots.
        """
        teams = self.stats["team"].unique()
        scores = {
            "team": teams,
            "goals": [
                self.stats[self.stats["team"] == team]["goals"].sum() for team in teams
            ],
            "shots": [
                self.stats[self.stats["team"] == team]["shots"].sum() for team in teams
            ],
        }
        return pd.DataFrame(data=scores)

    def is_tied(self) -> bool:
        """Return True if the game is tied else False."""
        return len(self.get_score()["goals"].unique()) == 1

    def get_score_dict(self) -> Dict:
        """Return a dict with the current games score."""
        return self.get_score().to_dict()

    def get_stats(self) -> pd.DataFrame:
        """Return the game stats."""
        return self.stats

    def get_stats_dict(self):
        """Get the game stats as a dict."""
        return self.stats.to_dict()

    def __str__(self) -> str:
        """Return the game score as a string."""
        return str(self.get_score())


@dataclass
class GameState:
    """
    A dataclass containg the game state data

    Attributes:
        boxscore (BoxScore): The current game score and player stats.
        players_positions (pd.DataFrame): A dataframe containing all players and their possitions.
        time (int): The current time in seconds until end of periond.
        period (int): The current period number.
        overtime (bool): True if the game is in overtime, else False. Default = False.
        game_log (List[str]): A list of event log string. Default = []
    """

    boxscore: pd.DataFrame
    players_positions: pd.DataFrame
    time: int
    period: int
    puck: dict
    overtime: bool = False
    game_log: List[str] = field(default_factory=lambda: [])


class PossessionStack:
    """
    A class used to manage the history of players puck possession.

    Attributes:
        stack (List): a list of all players who have had puck possession, with the most recent player at the end.
    """

    def __init__(self) -> None:
        self.stack = []

    def add_player(self, player: Pawn) -> None:
        """
        Add a player to the end of the stack if they are not currently the most recent player.
        """
        # TODO: if the most recent player on the stack is on ther other team, reset stack
        # add a player to the stack if they are not already at the top
        if player:
            current_player = self.stack[-1].name if len(self.stack) > 0 else None
            if current_player is None or current_player != player.name:
                self.stack.append(player)

    def get_assist(self) -> Pawn:
        """Return the player who assisted the goal, if no player return None"""
        return self.stack[-2] if self.size() > 1 else None

    def reset(self) -> None:
        """Reset the stack to an empty list"""
        self.stack = []

    def size(self) -> int:
        """Return the total length of the stack"""
        return len(self.stack)

    def print_stack(self) -> None:
        """Print all of the players in the stack"""
        for player in self.stack:
            print(player.name)


class GameManager:
    """
    A class that manages all the game actions.

    Attributes:
        teams_by_id (Dict[int, Team]): a dict of Team keyed by ids.
        players_by_id (Dict[int, Pawn]): a dict of Pawn keyed by ids.
        home_team (Team): The team with the home ice advantage.
        away_team (Team): The visiting team.
        boxscore (BoxScore): The current game score and player stats.
        puck (Puck): The puck state.
        timer (int): The number of second for each period. Default = 30.
        game_ticks (int): The number of seconds to dectement each game tick. Default = 1.
        num_periods (int): The total number of periods to play before overtime. Default = 3.
        completed (bool): True if the game is over, else False. Default = False.
        possession_stack (PossessionStack): The stack to manage the player possession.
        lineups (pd.DataFrame): A dataframe containing all players and their possitions.
        state (pd.DataFrame): The current game state.

    Args:
        home_team (Team): The Team to grant home ice advantage.
        away_team (Team): The visiting Team.
        pawns (List[Pawns]): A list of all Pawns in the game.
    """

    def __init__(self, home_team: Team, away_team: Team, pawns: List[Pawn]) -> None:
        self.teams_by_id = {
            home_team.name: home_team,
            away_team.name: away_team,
        }
        self.players_by_id = {player.id: player for player in pawns}

        self.home_team = home_team
        self.away_team = away_team
        self.boxscore = BoxScore(self.home_team, self.away_team, self.players_by_id)

        self.puck = Puck(zone=zone.OUT_OF_PLAY)
        self.timer = 30
        self.game_tick = 1
        self.num_periods = 3
        self.completed = False
        self.posession_stack = PossessionStack()
        self.lineups = self._generate_lineups()

        self.state = GameState(
            boxscore=self.boxscore,
            players_positions=self.lineups,
            time=self.timer,
            period=1,
            puck={"zone": self.puck.zone, "player": self.puck.player},
        )

    def get_player_team(self, player: Pawn) -> str:
        """Return the name of the team of the given player."""
        return self.lineups.loc[self.lineups["player-id"] == player.id].team.unique()[0]

    def get_team_players(self, team: Team) -> pd.DataFrame:
        """Return a dataframe containing all the data for all players in the team."""
        return self.lineups.loc[self.lineups["team"] == team.name]

    def get_opponent_team(self, player: Pawn) -> str:
        """Return the opposition team name of the given player."""
        return self.lineups.loc[
            self.lineups["team"] != self.get_player_team(player)
        ].team.unique()[0]

    def get_random_player(self, team: Optional[Team] = None) -> Pawn:
        """
        Return a random player on the ice. If team is not None get a random player from that team.
        Args:
            team (Optional[Team]): if not None, return a random player from that team.
        Returns:
            a random Pawn on the ice.
        """
        if team:
            player = self.get_team_players(team).sample()
        else:
            player = self.lineups.sample()
        return self.players_by_id[player["player-id"].values[0]]

    def _generate_lineups(self) -> pd.DataFrame:
        """
        Generate a pd.DataFrame containing all the teams players possition data.

        Returns:
            a DataFrame with player possition data.
        """
        idx = 0
        data = {}
        for home, team in enumerate([self.away_team, self.home_team]):
            for player_id in team.players:
                data[idx] = [
                    home == 1,
                    team.name,
                    self.players_by_id[player_id].id,
                    self.players_by_id[player_id].name,
                    self.players_by_id[player_id].position,
                    True,
                ]
                idx += 1
        return pd.DataFrame.from_dict(
            data,
            orient="index",
            columns=["home", "team", "player-id", "player", "position", "on-ice"],
        )

    def log_event(self, text: str) -> None:
        """Add the event text to the game_log."""
        self.state.game_log.append(f"{self.state.period}:{self.state.time}: {text}")

    def reset_puck(self):
        """Reset the puck, setting the zone to OUT_OF_PLAY and the player to None."""
        self.puck.zone = zone.OUT_OF_PLAY
        self.puck.player = None

    def player_shoot(self, player: Pawn) -> None:
        """
        Determin the result of a shot from the given Pawn.

        Args:
            player (Pawn): the shooting player.
        """
        chance = random.uniform(0, 1)
        if chance < player.stats.accuracy:
            assister = self.posession_stack.get_assist()
            if assister and self.get_player_team(assister) == self.get_player_team(
                player
            ):
                self.boxscore.add_assist(assister)
            self.reset_puck()
            self.boxscore.add_shot(player, goal=True)
        else:
            self.boxscore.add_shot(player)
            self.puck.player = self.get_random_player(
                team=self.teams_by_id[self.get_opponent_team(player)]
            )

    def player_pass(self, player_a: Pawn, player_b: Pawn) -> None:
        """
        Determin the result of a pass from the given Pawn to another, and change puck possession.

        Args:
            player_a (Pawn): the passing player.
            player_b (Pawn): the recieving player.
        """
        chance = random.uniform(0, 1)
        if chance < (player_a.stats.accuracy + player_b.stats.positioning) / 2:
            self.puck.player = player_b
        else:
            self.puck.player = self.get_random_player()

    def face_off(self, player_a: Pawn, player_b: Pawn) -> None:
        """
        Determin the result of a faceoff between two Pawns, log stats and set puck possession.

        Args:
            player_a (Pawn): the passing player.
            player_b (Pawn): the recieving player.
        """
        diff = player_a.stats.strength - player_b.stats.strength
        chance = random.uniform(0, 1)
        if chance < 0.5 + diff:
            self.puck.player = player_a
        else:
            self.puck.player = player_b
        self.puck.zone = zone.NEWTRAL
        self.boxscore.add_faceoff(player_a, won=player_a is self.puck.player)
        self.boxscore.add_faceoff(player_b, won=player_b is self.puck.player)

    def do_something(self, player: Pawn) -> None:
        """
        Determin what a Pawn attempts todo with the puck.

        Args:
            player (Pawn): the Pawn that is attempting to do something.
        """
        # TODO:
        team = self.teams_by_id[self.get_player_team(player)]
        option = random.randint(0, 1)
        if option == 0:
            return self.player_shoot(player)
        elif option == 1:
            player_id = team.players[random.randint(0, len(team.players) - 1)]
            player_b = self.players_by_id[player_id]
            self.player_pass(player, player_b)

    def is_tied(self) -> bool:
        """Return True if the game is currently tied else Flase"""
        return self.boxscore.is_tied()

    def run(self):
        """Run the game until it is completed."""
        while not self.completed:
            self.completed = self.increment_state()

    def increment_state(self) -> bool:
        """
        increment the game by 1 game_tick and return True if the game is over.
        """
        self.run_state()
        if self.state.time > 0:
            if self.state.overtime and not self.is_tied():
                return True
            self.state.time -= self.game_tick
        elif self.state.period < self.num_periods:
            self.state.period += 1
            self.state.time = self.timer
        elif self.is_tied():
            self.state.period += 1
            self.state.time = self.timer
            self.state.overtime = True
        else:
            return True

    def run_state(self) -> None:
        """
        Run the current game state and then sleep for SLEEP.
        """
        if self.puck.zone == zone.OUT_OF_PLAY:
            self.face_off(
                self.players_by_id[self.home_team.players[-1]],
                self.players_by_id[self.away_team.players[-1]],
            )
        else:
            self.do_something(self.puck.player)
        self.posession_stack.add_player(self.puck.player)
        # self.posession_stack.print_stack()
        time.sleep(SLEEP)
