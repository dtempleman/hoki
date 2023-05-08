import xml.etree.ElementTree as ET
from typing import List

from hoki.body import Body, BodyPart
from hoki.pawn import Pawn, dominant_hands, position
from hoki.statblock import StatBlock
from hoki.team import Team


def team_to_xml(team: Team) -> ET.Element:
    """
    Convert a Team object to an Element.

    Args:
        team (Team): The team to convert.
    Returns:
        an element tree representation of the team.
    """
    element = ET.Element("team", name=team.name)
    for player_id in team.players:
        pid = ET.SubElement(element, "player-id")
        pid.text = str(player_id)
    return element


def xml_to_team(element: ET.Element) -> Team:
    """
    Convert an ET.Element to a Team object.

    Args:
        element (ET.Element): the element to convert.
    Returns:
        a Team object containing the data from the Element.
    """
    return Team(name=element.attrib["name"], players=[p.text for p in element])


def teams_list_to_xml(teams: List[Team]) -> ET.Element:
    """
    Convert a list of Team objects to an Element.

    Args:
        teams (List[Team]): The teams to convert.
    Returns:
        an element tree representation of the teams.
    """
    element = ET.Element("teams")
    for team in teams:
        element.append(team_to_xml(team))
    return element


def xml_to_teams_list(elements: ET.Element) -> List[Team]:
    """
    Convert an ET.Element to a list of Team objects.

    Args:
        element (ET.Element): the element to convert.
    Returns:
        a list of Team objects containing the data from the Element.
    """
    return [xml_to_team(team) for team in elements]


def statblock_to_xml(statblock: StatBlock) -> ET.Element:
    """
    Convert a StatBlock object to an Element.

    Args:
        statblock (StatBlock): The statblock to convert.
    Returns:
        an element tree representation of the StatBlock.
    """
    element = ET.Element("statblock")
    pos = ET.SubElement(element, "stat", dict(name="positioning"))
    pos.text = str(statblock.positioning)
    pos = ET.SubElement(element, "stat", dict(name="iq"))
    pos.text = str(statblock.iq)
    pos = ET.SubElement(element, "stat", dict(name="shooting"))
    pos.text = str(statblock.shooting)
    pos = ET.SubElement(element, "stat", dict(name="passing"))
    pos.text = str(statblock.passing)
    pos = ET.SubElement(element, "stat", dict(name="save"))
    pos.text = str(statblock.save)
    pos = ET.SubElement(element, "stat", dict(name="skate"))
    pos.text = str(statblock.skate)
    pos = ET.SubElement(element, "stat", dict(name="checking"))
    pos.text = str(statblock.checking)
    pos = ET.SubElement(element, "stat", dict(name="stable"))
    pos.text = str(statblock.stable)
    return element


def xml_to_statblock(element: ET.Element) -> StatBlock:
    """
    Convert an ET.Element to a StatBlock object.

    Args:
        element (ET.Element): the element to convert.
    Returns:
        a StatBlok object containing the data from the Element.
    """
    stats = {stat.attrib["name"]: float(stat.text) for stat in element.findall("stat")}
    return StatBlock(
        positioning=stats["positioning"],
        iq=stats["iq"],
        shooting=stats["shooting"],
        passing=stats["passing"],
        save=stats["save"],
        skate=stats["skate"],
        checking=stats["checking"],
        stable=stats["stable"],
        shooting_hand=1.0,
    )


def bodypart_to_xml(bodypart: BodyPart) -> ET.Element:
    """
    Convert a BodyPart object to an ET.Element.

    Args:
        bodypart (BodyPart): The bodypart to convert.
    Returns:
        an element tree representation of the BodyPart.
    """
    element = ET.Element("bodypart", name=bodypart.name)
    state = ET.SubElement(element, "state", name="current")
    state.text = str(bodypart.current)
    max = ET.SubElement(element, "state", name="maximum")
    max.text = str(bodypart.maximum)
    return element


def xml_to_bodypart(element: ET.Element) -> Body:
    """
    Convert an ET.Element to a BodyPart object.

    Args:
        element (ET.Element): the element to convert.
    Returns:
        a BodyPart object containing the data from the Element.
    """
    state = {
        state.attrib["name"]: float(state.text) for state in element.findall("state")
    }
    return BodyPart(
        name=element.attrib["name"],
        current=state["current"],
        maximum=state["maximum"],
    )


def body_to_xml(body: Body) -> ET.Element:
    """
    Convert a Body object to an ET.Element.

    Args:
        body (Body): The body to convert.
    Returns:
        an element tree representation of the Body.
    """
    element = ET.Element("body")
    element.append(bodypart_to_xml(body.head))
    element.append(bodypart_to_xml(body.torso))
    element.append(bodypart_to_xml(body.arm_r))
    element.append(bodypart_to_xml(body.arm_l))
    element.append(bodypart_to_xml(body.leg_r))
    element.append(bodypart_to_xml(body.leg_l))
    return element


def xml_to_body(element: ET.Element) -> Body:
    """
    Convert an ET.Element to a Body object.

    Args:
        element (ET.Element): the element to convert.
    Returns:
        a Body object containing the data from the Element.
    """
    bodyparts = {
        part.attrib["name"]: xml_to_bodypart(part)
        for part in element.findall("bodypart")
    }
    return Body(
        head=bodyparts["head"],
        torso=bodyparts["torso"],
        arm_r=bodyparts["arm_r"],
        arm_l=bodyparts["arm_l"],
        leg_r=bodyparts["leg_r"],
        leg_l=bodyparts["leg_l"],
    )


def pawn_to_xml(pawn: Pawn) -> ET.Element:
    """
    Convert a Pawn object to an ET.Element.

    Args:
        pawn (Pawn): The pawn to convert.
    Returns:
        an element tree representation of the Pawn.
    """
    element = ET.Element(
        "pawn",
        id=str(pawn.id),
        name=pawn.name,
        jersey_num=str(pawn.jersey_num),
        shoots=pawn.shoots.name,
        position=pawn.position.name,
    )
    element.append(statblock_to_xml(pawn.stats))
    element.append(body_to_xml(pawn.body))
    return element


def xml_to_pawn(element: ET.Element) -> Pawn:
    """
    Convert an ET.Element to a Pawn object.

    Args:
        element (ET.Element): the element to convert.
    Returns:
        a Pawn object containing the data from the Element.
    """
    return Pawn(
        id=element.attrib["id"],
        name=element.attrib["name"],
        jersey_num=element.attrib["jersey_num"],
        position=position[element.attrib["position"]],
        shoots=dominant_hands[element.attrib["shoots"]],
        stats=xml_to_statblock(element.find("statblock")),
        body=xml_to_body(element.find("body")),
    )


def pawns_list_to_xml(pawns: List[Pawn]) -> ET.Element:
    """
    Convert a list of Pawn objects to an ET.Element.

    Args:
        pawns (List[Pawn]): The pawns to convert.
    Returns:
        an element tree representation of the Pawns.
    """
    element = ET.Element("pawns")
    for pawn in pawns:
        element.append(pawn_to_xml(pawn))
    return element


def xml_to_pawns_list(elements: ET.Element) -> List[Pawn]:
    """
    Convert an ET.Element to a list of Pawn objects.

    Args:
        element (ET.Element): the element to convert.
    Returns:
        a list of Pawn objects containing the data from the Element.
    """
    return [xml_to_pawn(pawn) for pawn in elements]


def save_state_to_xml(teams: List[Team], pawns: List[Pawn]) -> ET.Element:
    """
    Convert a list of Teams and a list of Pawns to an ET.Element

    Args:
        teams (List[Team]): The teams to convert.
        pawns (List[Pawn]): The pawns to convert.
    Returns:
        an element tree representation of the Teams and Pawns.
    """
    root = ET.Element("data")
    pawns = pawns_list_to_xml(pawns)
    teams = teams_list_to_xml(teams)
    root.append(pawns)
    root.append(teams)
    return root


def xml_to_save_state(element: ET.Element):
    """
    Convert an ET.Element to a list of Pawn objects and a list of Team objects.

    Args:
        element (ET.Element): the element to convert.
    Returns:
        a list of Pawn objects and a list of Team object containing the data from the Element.
    """
    pawns = xml_to_pawns_list(element.find("pawns"))
    teams = xml_to_teams_list(element.find("teams"))
    return pawns, teams
