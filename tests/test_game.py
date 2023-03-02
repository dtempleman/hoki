import pytest

from hoki.game import GameManager, PossessionStack


@pytest.mark.parametrize(
    'n_players, expected_player_index',
    [
        pytest.param(0, None, id='0'),
        pytest.param(1, None, id='1'),
        pytest.param(2, 0, id='2'),
        pytest.param(3, 1, id='>2'),
    ]
)
def test_possession_stack(create_players, n_players, expected_player_index):
    stack = PossessionStack()
    players = create_players(n_players)
    for player in players:
        stack.add_player(player)
    expected_player = players[expected_player_index] if expected_player_index is not None else None
    assert stack.get_assist() == expected_player
    stack.reset()
    assert stack.size() == 0


def test_run_game(create_teams, fill_teams_with_pawns):
    teams = create_teams(2)
    players = fill_teams_with_pawns(teams)
    game = GameManager(teams[0], teams[1], pawns=players)
    game.run()
    assert game.completed
