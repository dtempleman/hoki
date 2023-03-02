from hoki.league import League, Season


def test_league_run_season(create_game, fill_teams_with_pawns):
    game, teams, players = create_game()
    league = League(teams=teams, players=players)
    assert league.year == 0

    game.state.period = 3
    game.state.time = 0
    game.increment_state()
    game.run()
    league._apply_game_stats(game)
    league.run_season()
    assert league.year == 1


def test_seasion(create_teams):
    for n_teams in range(100):
        teams = create_teams(n_teams)
        seasion = Season(teams)
        assert len(seasion.schedule) == (n_teams * (n_teams - 1)) / 2
