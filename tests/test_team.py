from hoki.team import Team, generate_team_name


def test_team(create_player):
    team = Team(
        name="test"
    )
    assert str(team) == "test:\n"
    assert team.name == "test"
    assert team.players == []

    pawn = create_player()
    team.players.append(pawn)
    assert str(team) == f"test:\n{pawn}\n"
    assert team.name == "test"
    assert team.players == [pawn]


def test_generate_team_name():
    name1 = generate_team_name()
    name2 = generate_team_name()
    assert name1 != name2
