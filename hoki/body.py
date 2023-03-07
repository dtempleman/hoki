from dataclasses import dataclass
from enum import Enum, auto


class dominant_hands(Enum):
    """Enumerate a Bodys dominant hands."""

    RIGHT = auto()
    LEFT = auto()


@dataclass
class BodyPart:
    """
    A dataclass to hold the durrability of a single body part.

    Attributes:
        name (str): The name of the body part
        current (float): The current durrability of the body part. Default = 1.0
        maximum (float): The maximum durrability of the body part. Default = 1.0
            The current cannot be an hight thant the maximum
    """

    name: str
    current: float = 1.0  # current health of body part
    maximum: float = 1.0  # the maximum health the part can be


@dataclass
class Body:
    """
    A dataclass containing a set of BodyParts.

    Attributes:
        head (BodyPart): The BodyPart represenging the bodies head.
        torso (BodyPart): The BodyPart represenging the bodies torso.
        arm_l (BodyPart): The BodyPart represenging the bodies left arm.
        arm_r (BodyPart): The BodyPart represenging the bodies right arm.
        leg_l (BodyPart): The BodyPart represenging the bodies left leg.
        leg_r (BodyPart): The BodyPart represenging the bodies right leg.
    """

    head: BodyPart = BodyPart(name="head")
    torso: BodyPart = BodyPart(name="torso")
    arm_r: BodyPart = BodyPart(name="arm_r")
    arm_l: BodyPart = BodyPart(name="arm_l")
    leg_r: BodyPart = BodyPart(name="leg_r")
    leg_l: BodyPart = BodyPart(name="leg_l")


def damage_bodypart(body_part: BodyPart, force: float) -> None:
    """
    Apply a force to a body part and degrade its durrability.

    Args:
        body_part (BodyPart): the body part to apply force upon
        force (float): the ammount of force applied
    """
    if force > body_part.current:
        body_part.current = 0
    else:
        body_part.current -= force
