from typing import List, Union

import pytest

from hoki.game_state import GameState
from hoki.ice_map import IceMap
from hoki.pawn import Pawn, position
from hoki.player_manager import PlayerManager


@pytest.fixture()
def player_manager(create_players):
    players = create_players(10)
    ice_map = IceMap()
    players_by_id = {p.id: p for p in players}
    return PlayerManager(players_by_id, ice_map), players_by_id


def test_player_manager(player_manager):
    manager, _ = player_manager


@pytest.mark.parametrize(
    "position",
    [
        pytest.param(position.GOALIE, id="Goalie"),
        pytest.param(position.WING_L, id="Wing L"),
        pytest.param(position.WING_R, id="Wing R"),
        pytest.param(position.DEFENCE_L, id="Defence L"),
        pytest.param(position.DEFENCE_R, id="Defence R"),
        pytest.param(position.CENTRE, id="Centre"),
    ],
)
def test_get_players_opponant_by_position(
    player_manager: Union[PlayerManager, List], position
):
    manager, players = player_manager


@pytest.mark.parametrize(
    "position",
    [
        pytest.param(position.GOALIE, id="Goalie"),
        pytest.param(position.WING_L, id="Wing L"),
        pytest.param(position.WING_R, id="Wing R"),
        pytest.param(position.DEFENCE_L, id="Defence L"),
        pytest.param(position.DEFENCE_R, id="Defence R"),
        pytest.param(position.CENTRE, id="Centre"),
    ],
)
def test_get_players_teammate_by_position(player_manager, position):
    manager, _ = player_manager


@pytest.mark.parametrize(
    "position",
    [
        pytest.param(position.GOALIE, id="Goalie"),
        pytest.param(position.WING_L, id="Wing L"),
        pytest.param(position.WING_R, id="Wing R"),
        pytest.param(position.DEFENCE_L, id="Defence L"),
        pytest.param(position.DEFENCE_R, id="Defence R"),
        pytest.param(position.CENTRE, id="Centre"),
    ],
)
def test_get_all_players_by_positions(
    player_manager: PlayerManager, position: position
):
    manager, _ = player_manager
    manager.get_all_players_by_positions([position])


def test_face_off(player_manager):
    manager, _ = player_manager


def test_get_loose_puck(player_manager):
    manager, _ = player_manager


def test_player_choose_action(player_manager):
    manager, _ = player_manager


# player choose


def test_player_choose_reaction_tip(player_manager):
    manager, _ = player_manager


def test_player_choose_reaction_block(player_manager):
    manager, _ = player_manager


def test_player_choose_action_skate(player_manager):
    manager, _ = player_manager


def test_player_choose_action_hit(player_manager):
    manager, _ = player_manager


def test_player_choose_action_shoot(player_manager):
    manager, _ = player_manager


def test_player_choose_action_pass(player_manager):
    manager, _ = player_manager


# player actions


def test_player_action_skate(player_manager):
    manager, _ = player_manager


def test_player_action_hit(player_manager):
    manager, _ = player_manager


def test_player_action_shoot(player_manager):
    manager, _ = player_manager


def test_player_action_pass(player_manager):
    manager, _ = player_manager


# player reactions


def test_player_reaction_tip(player_manager):
    manager, _ = player_manager


def test_player_reaction_block(player_manager):
    manager, _ = player_manager
