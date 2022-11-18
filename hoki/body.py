from dataclasses import dataclass
from enum import Enum, auto


class dominant_hands(Enum):
    RIGHT = auto()
    LEFT = auto()


@dataclass
class BodyPart:
    state: float = 1.0  # current health of body part
    maximum: float = 1.0  # the maximum health the part can be


@dataclass
class Body:
    head: BodyPart = BodyPart()
    torso: BodyPart = BodyPart()
    arm_r: BodyPart = BodyPart()
    arm_l: BodyPart = BodyPart()
    leg_r: BodyPart = BodyPart()
    leg_l: BodyPart = BodyPart()


def damage_bodypart(body_part, force):
    if force > body_part.state:
        body_part.state = 0
    else:
        body_part.state -= force