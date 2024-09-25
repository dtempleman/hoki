import pytest

from hoki.models.savestate import SaveState


@pytest.fixture()
def create_savable(create_player, create_team, fill_teams_with_pawns, create_teams):
    def func(savable):
        if savable == "Player":
            return create_player()
        elif savable == "Team":
            team = create_team()
            fill_teams_with_pawns([team])
            return team
        elif savable == "SaveState":
            teams = create_teams()
            players = fill_teams_with_pawns(teams)
            return SaveState(teams=teams, players=players)

    return func


@pytest.mark.parametrize(
    "savable_class",
    [
        "Player",
        "Team",
        "SaveState",
    ],
)
def test_savable_to_and_from_xml(savable_class, create_savable):
    savable = create_savable(savable_class)
    root = savable.to_xml()
    new_savable = type(savable).from_xml(root)
    assert savable == new_savable
