from hoki.pawn import Pawn, dominant_hands, position, generate_player_name
from hoki.statblock import generate_inital_stats
from hoki.body import Body


import pytest


@pytest.mark.parametrize(
    'player_position',
    [
        pytest.param(position.CENTRE, id='CENTER'),
        pytest.param(position.WING_L, id='WING_L'),
        pytest.param(position.WING_R, id='WING_R'),
        pytest.param(position.DEFENCE_L, id='DEFENCE_L'),
        pytest.param(position.DEFENCE_R, id='DEFENCE_R'),
        pytest.param(position.GOALIE, id='GOALIE'),
    ]
)
def test_pawn(player_position):
    for hand in [dominant_hands.RIGHT, dominant_hands.LEFT]:
        pawn = Pawn(
            name="test",
            position=player_position,
            id=0,
            shoots=hand,
            stats=generate_inital_stats(),
            jersey_num=0,
            body=Body(),
        )

        assert pawn.get_player_rating() > 0
        assert str(pawn) == f"test: {player_position.name} #0"


def test_generate_player_name():
    name1 = generate_player_name()
    name2 = generate_player_name()
    assert name1 != name2
