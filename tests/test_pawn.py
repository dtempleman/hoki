import pytest

from hoki.models.body import Body
from hoki.models.pawn import Pawn, generate_pawn_name
from hoki.models.player import dominant_hands, position
from hoki.models.statblock import generate_inital_stats


@pytest.mark.parametrize(
    "player_position",
    [
        pytest.param(position.CENTRE, id="CENTER"),
        pytest.param(position.WING_L, id="WING_L"),
        pytest.param(position.WING_R, id="WING_R"),
        pytest.param(position.DEFENCE_L, id="DEFENCE_L"),
        pytest.param(position.DEFENCE_R, id="DEFENCE_R"),
        pytest.param(position.GOALIE, id="GOALIE"),
    ],
)
def test_pawn(player_position):
    for hand in [dominant_hands.RIGHT, dominant_hands.LEFT]:
        pawn = Pawn(
            name="test",
            id=0,
            stats=generate_inital_stats(),
        )

        assert str(pawn) == "test"


def test_generate_pawn_name():
    name1 = generate_pawn_name()
    name2 = generate_pawn_name()
    assert name1 != name2
