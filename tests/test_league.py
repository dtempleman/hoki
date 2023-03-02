from hoki.league import League, Season


def test_league_run_season(create_teams, fill_teams_with_pawns):
    n_teams = 2
    teams = create_teams(n_teams)
    players = fill_teams_with_pawns(teams)
    league = League(teams=teams, players=players)
    assert league.year == 0
    league.run_season()
    assert league.year == 1


def test_seasion(create_teams):
    for n_teams in range(100):
        teams = create_teams(n_teams)
        seasion = Season(teams)
        assert len(seasion.schedule) == (n_teams * (n_teams - 1)) / 2
