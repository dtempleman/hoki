from hoki.body import Body, BodyPart, damage_bodypart


def test_body():
    body = Body()
    assert body.arm_l.name == "arm_l"
    assert body.arm_r.name == "arm_r"
    assert body.leg_l.name == "leg_l"
    assert body.leg_r.name == "leg_r"
    assert body.head.name == "head"
    assert body.torso.name == "torso"


def test_damage_body_part():
    body_part = BodyPart(name="test")
    assert body_part.current == 1
    assert body_part.maximum == 1
    damage_bodypart(body_part, 0.5)
    assert body_part.current == 0.5
    damage_bodypart(body_part, 0.5)
    assert body_part.current == 0.0
    damage_bodypart(body_part, 0.5)
    assert body_part.current == 0.0