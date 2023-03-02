from dataclasses import dataclass
from enum import Enum, auto


class dominant_hands(Enum):
    RIGHT = auto()
    LEFT = auto()


@dataclass
class BodyPart:
    name: str
    current: float = 1.0  # current health of body part
    maximum: float = 1.0  # the maximum health the part can be


@dataclass
class Body:
    head: BodyPart = BodyPart(name="head")
    torso: BodyPart = BodyPart(name="torso")
    arm_r: BodyPart = BodyPart(name="arm_r")
    arm_l: BodyPart = BodyPart(name="arm_l")
    leg_r: BodyPart = BodyPart(name="leg_r")
    leg_l: BodyPart = BodyPart(name="leg_l")


def damage_bodypart(body_part, force):
    if force > body_part.current:
        body_part.current = 0
    else:
        body_part.current -= force
