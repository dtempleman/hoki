import random
from enum import Enum, auto
from typing import List, Union

from hoki.game_state import GameState
from hoki.pawn import position


class player_action(Enum):
    SHOOT = auto()
    PASS = auto()
    SKATE = auto()
    NOTHING = auto()
    HIT = auto()


class PlayerManager:
    def __init__(self, players_by_id, ice_map) -> None:
        self.players = players_by_id
        self.ice_map = ice_map

    def get_players_opponant_by_position(
        self, game_state: GameState, player_id: str, positions: List[int] = []
    ):
        players = list(self.players.keys())
        team_player_ids = game_state.players_by_team[
            game_state.team_by_player[player_id]
        ]
        players = list(set(players) - set(team_player_ids))
        if positions is not None and len(positions) > 0:
            players = [
                pid for pid in players if self.players[pid].position in positions
            ]
        return players

    def get_players_teammate_by_position(
        self, game_state: GameState, player_id: str, positions: List[int] = []
    ):
        players = list(self.players.keys())
        if player_id is not None:
            players = [
                p
                for p in game_state.players_by_team[
                    game_state.team_by_player[player_id]
                ]
            ]
            players.remove(player_id)
        if positions is not None and len(positions) > 0:
            players = [
                pid for pid in players if self.players[pid].position in positions
            ]
        return players

    def get_all_players_by_positions(self, positions: List = []):
        players = list(self.players.keys())
        if positions is not None and len(positions) > 0:
            players = [
                pid for pid in players if self.players[pid].position in positions
            ]
        return players

    def face_off(self, game_state: GameState):
        # calculate winner a faceoff between the 2 centres
        players = self.get_all_players_by_positions([position.CENTRE])
        idx = random.randint(0, 1)
        return players[idx], players[(idx + 1) % 2]

    def get_loose_puck(self, game_state: GameState):
        # for each player in puck zone calculate who gets the puck
        pass

    def player_choose_action(
        self, player_id: int, game_state: GameState
    ) -> player_action:
        options = [
            player_action.SKATE,
            player_action.NOTHING,
            player_action.SHOOT,
            player_action.PASS,
        ]

        if player_id == game_state.puck_player:
            option = random.randint(0, len(options) - 1)
        elif self.players[player_id].position == position.GOALIE:
            return player_action.NOTHING
        else:
            option = random.randint(0, len(options) - 3)
        return options[option]

    def player_choose_reaction_tip(
        self, player_id: int, game_state: GameState
    ) -> float:
        # return chance
        return 1.0

    def player_choose_reaction_block(
        self, player_id: int, game_state: GameState
    ) -> float:
        # return chance
        return 1.0

    def player_choose_action_skate(
        self, player_id: int, game_state: GameState
    ) -> Union[float, int]:
        # return chance and zone id
        return 1.0, game_state.zone_by_player[player_id]

    def player_choose_action_hit(
        self, player_id: int, game_state: GameState
    ) -> Union[float, int]:
        # return chance and player id of receiver
        return 1.0, 0

    def player_choose_action_shoot(
        self, player_id: int, game_state: GameState
    ) -> float:
        # return chance
        return 1.0

    def player_choose_action_pass(
        self, player_id: int, game_state: GameState
    ) -> Union[float, int]:
        # return chance and player id of receiver
        players = self.get_players_teammate_by_position(game_state, player_id)
        return 1.0, players[random.randint(0, len(players) - 1)]

    def player_action_shoot(
        self,
        shooter_id: int,
        game_state: GameState,
    ) -> Union[bool, int, int]:
        # print(f"player {shooter_id} shoots!")

        # Calculate the results of a shot.
        goalie_id = self.get_players_opponant_by_position(
            game_state, shooter_id, [position.GOALIE]
        )[0]

        shot_path = self.ice_map.shot_paths[game_state.zone_by_player[shooter_id]][
            game_state.zone_by_player[goalie_id]
        ]
        goalie_zone = shot_path[-1]
        shooter_team = game_state.team_by_player[shooter_id]

        # TODO: calculate if initial shot is on target
        ontarget = True
        if not ontarget:
            return False, -1, 10

        # TODO: calculate initial save difficulty based on shooter stats,
        # path length, and number of opponants in the way
        save_difficulty = self.players[shooter_id].stats.shooting
        # print(f"initlal diff: {save_difficulty}")
        # print(shot_path)
        blocked = False
        for zone in shot_path:
            for player_id in game_state.player_by_zone[zone]:
                if player_id == shooter_id:
                    continue
                player = self.players[player_id]
                if player.position == position.GOALIE:
                    continue
                if game_state.team_by_player[player_id] == shooter_team:
                    if self.player_choose_reaction_tip(player, game_state):
                        # print(f"player {player_id} attepts to tip it!")
                        # TODO: determin if tip is successfull
                        if random.uniform(0, 1) < 0.25:
                            # print(f"player {player_id} tips it!")
                            save_difficulty += 0.15
                            # print(f"diff = {save_difficulty}")
                else:
                    if (
                        self.player_choose_reaction_block(player, game_state)
                        and not blocked
                    ):
                        blocked = True
                        # print(f"player {player_id} attepts to block it!")
                        # TODO: determin is block is successfull
                        if random.uniform(0, 1) < 0.25:
                            # print(f"player {player_id} blocks it!")
                            return (
                                False,
                                player_id,
                                game_state.zone_by_player[player_id],
                            )
                        # print(f"player {player_id} screens the goalie!")
                        save_difficulty += 0.5
                        # print(f"diff = {save_difficulty}")

        # TODO: calculate if the goalie is able to make the save
        if save_difficulty < self.players[goalie_id].stats.save:
            # print(f"player {goalie_id} saves it!")
            return False, goalie_id, goalie_zone
        # print("GOAL!")
        return True, None, goalie_zone

    def player_action_pass(
        self, passer_id: int, game_state: GameState
    ) -> Union[int, int]:
        _, receiver_id = self.player_choose_action_pass(passer_id, game_state)
        shooter_team = game_state.team_by_player[passer_id]

        pass_path = self.ice_map.shot_paths[game_state.zone_by_player[passer_id]][
            game_state.zone_by_player[receiver_id]
        ]

        # print(f"player: {passer_id} passes to {receiver_id}!")
        for zone_id in pass_path:
            for player_id in game_state.player_by_zone[zone_id]:
                player = self.players[player_id]
                if game_state.team_by_player[player_id] != shooter_team:
                    if self.player_choose_reaction_block(player, game_state):
                        if random.uniform(0, 1) < 0.25:
                            # print(f"player {player_id} intercepts the pass!")
                            return player_id, game_state.zone_by_player[player_id]

        return receiver_id, game_state.zone_by_player[receiver_id]

    def player_action_skate(self, player_id: int, game_state: GameState) -> int:
        # return the zone id to move the player to
        possible_zones = self.ice_map.zones[game_state.zone_by_player[player_id]][
            "connections"
        ]
        return possible_zones[random.randint(0, len(possible_zones) - 1)]

    def player_action_hit(self, player_id: int, game_state: GameState) -> float:
        # calculate if the hit makes contanct and return the force
        return 1.0

    def player_reaction_tip(
        self, player_id: int, difficulty: float, game_state: GameState
    ) -> Union[float, int]:
        # return updated shot difficulty and zone id of the puck
        return 1.0, game_state.zone_by_player[player_id]

    def player_reaction_block(
        self, player_id: int, difficulty: float, game_state: GameState
    ) -> Union[float, int]:
        # return updated shot difficulty and zone id of the puck
        return 1.0, game_state.zone_by_player[player_id]

    def player_reaction_save(
        self, player_id: int, difficulty: float, game_state: GameState
    ) -> Union[bool, int]:
        # return bool if save, and zone id if rebound
        return True, game_state.zone_by_player[player_id]

    def player_reaction_intercept(
        self, player_id: int, difficulty: float, game_state: GameState
    ) -> bool:
        # return if the player intercepts the pass
        return True
