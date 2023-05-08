import time
from typing import Dict, List

import pandas as pd

from hoki.game_state import GameState
from hoki.ice_map import IceMap
from hoki.pawn import Pawn
from hoki.player_manager import PlayerManager, player_action
from hoki.team import Team

# the number of seconds between game ticks
SLEEP = 0

# the different stats to be tracked durring a game
STATS_NAMES = ["goals", "assists", "shots", "faceoffs", "faceoffs-won"]


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

    def increment_stat(self, player: str, stat: str) -> None:
        """Increment the players given statistic by 1."""
        self.stats.loc[self.stats["player-id"] == player, stat] += 1

    def add_assist(self, player: str) -> None:
        """Increment the players assists by 1."""
        self.increment_stat(player, "assists")

    def add_shot(self, player: str, goal: bool = False) -> None:
        """Increment the players shots by one. If goal, increment its goals also."""
        self.increment_stat(player, "shots")
        if goal:
            self.increment_stat(player, "goals")

    def add_faceoff(self, player: str, won: bool = False) -> None:
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


class PossessionStack:
    """
    A class used to manage the history of players puck possession.

    Attributes:
        stack (List): a list of all players who have had puck possession, with the most recent player at the end.
    """

    def __init__(self) -> None:
        self.stack = []

    def add_player(self, player_id: int) -> None:
        """
        Add a player to the end of the stack if they are not currently the most recent player.
        """
        # TODO: if the most recent player on the stack is on ther other team, reset stack
        # add a player to the stack if they are not already at the top
        if player_id is not None:
            current_player = self.stack[-1] if len(self.stack) > 0 else None
            if current_player is None or current_player != player_id:
                self.stack.append(player_id)

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
        self.ice_map = IceMap()
        self.posession_stack = PossessionStack()

        self.teams_by_id = {
            home_team.name: home_team,
            away_team.name: away_team,
        }
        self.players_by_id = {player.id: player for player in pawns}
        self.player_manager = PlayerManager(self.players_by_id, self.ice_map)
        self.home_team = home_team
        self.away_team = away_team

        self.boxscore = BoxScore(self.home_team, self.away_team, self.players_by_id)

        self.timer = 30
        self.game_tick = 1
        self.num_periods = 3
        self.completed = False

        self.lineups = self._generate_lineups()

        players_by_team = {
            team: self.teams_by_id[team].players for team in self.teams_by_id
        }
        team_by_player = {
            pid: tid for tid in players_by_team for pid in players_by_team[tid]
        }
        zones_by_player = self.ice_map.get_initial_player_zones(self.lineups)
        player_by_zone = {z: [] for z in self.ice_map.zones}
        for p in zones_by_player:
            player_by_zone[zones_by_player[p]].append(p)

        self.state = GameState(
            puck_player=None,
            puck_zone=None,
            players_by_team=players_by_team,
            team_by_player=team_by_player,
            player_by_zone=player_by_zone,
            zone_by_player=zones_by_player,
            boxscore=self.boxscore,
            time=self.timer,
            period=1,
        )

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
        self.state.puck_player = None
        self.state.puck_zone = None

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
        if self.state.puck_zone is None:
            winner_id, loser_id = self.player_manager.face_off(self.state)
            self.boxscore.add_faceoff(winner_id, True)
            self.boxscore.add_faceoff(loser_id)
            self.state.puck_player = winner_id
            self.state.puck_zone = self.state.zone_by_player[winner_id]

        for player_id in self.players_by_id:
            action = self.player_manager.player_choose_action(player_id, self.state)

            if action == player_action.SHOOT:
                goal, puck_posessor, zone_id = self.player_manager.player_action_shoot(
                    player_id, self.state
                )
                self.boxscore.add_shot(player_id, goal)
                if goal:
                    assist_id = self.posession_stack.get_assist()
                    if (
                        assist_id is not None
                        and self.state.team_by_player[assist_id]
                        == self.state.team_by_player[player_id]
                    ):
                        self.boxscore.add_assist(assist_id)
                    self.reset_puck()
                else:
                    self.state.puck_player = puck_posessor
                    self.state.puck_zone = zone_id

            if action == player_action.PASS:
                receiver_id, zone_id = self.player_manager.player_action_pass(
                    player_id, self.state
                )
                self.state.puck_player = receiver_id
                self.state.puck_zone = zone_id

            if action == player_action.SKATE:
                zone_id = self.player_manager.player_action_skate(player_id, self.state)
                self.move_player(player_id, zone_id)

            if action == player_action.NOTHING:
                continue

            self.posession_stack.add_player(self.state.puck_player)
        time.sleep(SLEEP)

    def move_player(self, player_id, zone_id):
        old_zone_id = self.state.zone_by_player[player_id]

        self.state.player_by_zone[old_zone_id].remove(player_id)
        self.state.player_by_zone[zone_id].append(player_id)
        self.state.zone_by_player[player_id] = zone_id

        if self.state.puck_player == player_id:
            self.state.puck_zone = self.state.zone_by_player[player_id]
            return
