import pytest

from hoki.game import STATS_NAMES, BoxScore, GameManager, PossessionStack


@pytest.mark.parametrize(
    "n_players, expected_player_index",
    [
        pytest.param(0, None, id="0"),
        pytest.param(1, None, id="1"),
        pytest.param(2, 0, id="2"),
        pytest.param(3, 1, id=">2"),
    ],
)
def test_possession_stack(create_players, n_players, expected_player_index):
    stack = PossessionStack()
    players = create_players(n_players)
    for player in players:
        stack.add_player(player)
    expected_player = (
        players[expected_player_index] if expected_player_index is not None else None
    )
    assert stack.get_assist() == expected_player
    stack.print_stack()
    stack.reset()
    assert stack.size() == 0


def test_run_game(create_teams, fill_teams_with_pawns):
    teams = create_teams(2)
    players = fill_teams_with_pawns(teams)
    game = GameManager(teams[0], teams[1], pawns=players)
    game.run()
    assert game.completed

    game.log_event("test")
    assert game.state.game_log == ["3:0: test"]


def test_run_game_overtime(create_teams, fill_teams_with_pawns):
    teams = create_teams(2)
    players = fill_teams_with_pawns(teams)
    game = GameManager(teams[0], teams[1], pawns=players)
    game.state.period = 3
    game.state.time = 0
    game.increment_state()
    assert game.state.overtime
    assert game.is_tied()
    game.run()
    assert game.completed


def test_boxscore(create_teams, fill_teams_with_pawns):
    teams = create_teams(2)
    players = fill_teams_with_pawns(teams)
    boxscore = BoxScore(
        teams[0],
        teams[1],
        players_by_id={p.id: p for p in players},
    )

    assert boxscore.is_tied()

    boxscore.add_assist(players[0].id)
    boxscore.add_shot(players[0].id)
    boxscore.add_shot(players[0].id, goal=True)
    boxscore.add_faceoff(players[0].id)
    boxscore.add_faceoff(players[0].id, won=True)

    for stat in STATS_NAMES:
        boxscore.increment_stat(players[0].id, stat)

    assert not boxscore.is_tied()

    score_df = boxscore.get_score()
    assert score_df["team"].loc[0] == teams[0].name
    assert score_df["goals"].loc[0] == 2
    assert score_df["shots"].loc[0] == 3
    assert score_df["team"].loc[1] == teams[1].name
    assert score_df["goals"].loc[1] == 0
    assert score_df["shots"].loc[1] == 0

    score = boxscore.get_score_dict()
    assert score["team"][0] == teams[0].name
    assert score["team"][1] == teams[1].name
    assert score["goals"][0] == 2
    assert score["goals"][1] == 0
    assert score["shots"][0] == 3
    assert score["shots"][1] == 0

    stats_df = boxscore.get_stats()
    assert stats_df["player-id"].loc[0] == players[0].id
    assert stats_df["goals"].loc[0] == 2
    assert stats_df["shots"].loc[0] == 3
    assert stats_df["assists"].loc[0] == 2
    assert stats_df["faceoffs"].loc[0] == 3
    assert stats_df["faceoffs-won"].loc[0] == 2

    for i in range(1, len(stats_df)):
        assert stats_df["player-id"].loc[i] == players[i].id
        assert stats_df["goals"].loc[i] == 0
        assert stats_df["shots"].loc[i] == 0
        assert stats_df["assists"].loc[i] == 0
        assert stats_df["faceoffs"].loc[i] == 0
        assert stats_df["faceoffs-won"].loc[i] == 0

    stats = boxscore.get_stats_dict()
    assert stats["player-id"][0] == players[0].id
    assert stats["goals"][0] == 2
    assert stats["shots"][0] == 3
    assert stats["assists"][0] == 2
    assert stats["faceoffs"][0] == 3
    assert stats["faceoffs-won"][0] == 2

    for i in range(1, len(stats)):
        assert stats["player-id"][i] == players[i].id
        assert stats["goals"][i] == 0
        assert stats["shots"][i] == 0
        assert stats["assists"][i] == 0
        assert stats["faceoffs"][i] == 0
        assert stats["faceoffs-won"][i] == 0

    assert str(boxscore) == str(score_df)
