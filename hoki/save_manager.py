from typing import List

import xml.etree.ElementTree as ET

from hoki.team import Team
from hoki.pawn import Pawn, position, dominant_hands
from hoki.body import Body, BodyPart
from hoki.statblock import StatBlock


def team_to_xml(team: Team) -> ET.Element:
    element = ET.Element("team", name=team.name)
    for player_id in team.players:
        pid = ET.SubElement(element, "player-id")
        pid.text = str(player_id)
    return element


def xml_to_team(element: ET.Element) -> Team:
    return Team(name=element.attrib["name"], players=[p.text for p in element])


def teams_list_to_xml(teams: List[Team]) -> ET.Element:
    element = ET.Element("teams")
    for team in teams:
        element.append(team_to_xml(team))
    return element


def xml_to_teams_list(elements: ET.Element) -> List[Team]:
    return [xml_to_team(team) for team in elements]


def statblock_to_xml(statblock: StatBlock) -> ET.Element:
    element = ET.Element("statblock")
    pos = ET.SubElement(element, "stat", dict(name="positioning"))
    pos.text = str(statblock.positioning)
    acc = ET.SubElement(element, "stat", dict(name="accuracy"))
    acc.text = str(statblock.accuracy)
    acc = ET.SubElement(element, "stat", dict(name="strength"))
    acc.text = str(statblock.strength)
    acc = ET.SubElement(element, "stat", dict(name="iq"))
    acc.text = str(statblock.iq)
    return element


def xml_to_statblock(element: ET.Element) -> StatBlock:
    stats = {stat.attrib["name"]: float(stat.text) for stat in element.findall("stat")}
    return StatBlock(
        positioning=stats["positioning"],
        accuracy=stats["accuracy"],
        strength=stats["strength"],
        iq=stats["iq"],
        health=1.0,
        stability=1.0,
        speed=1.0,
        aggresivness=1.0,
        shooting_hand=1.0,
    )


def bodypart_to_xml(bodypart: BodyPart) -> ET.Element:
    element = ET.Element("bodypart", name=bodypart.name)
    state = ET.SubElement(element, "state", name="current")
    state.text = str(bodypart.current)
    max = ET.SubElement(element, "state", name="maximum")
    max.text = str(bodypart.maximum)
    return element


def xml_to_bodypart(element: ET.Element) -> Body:
    state = {
        state.attrib["name"]: float(state.text) for state in element.findall("state")
    }
    return BodyPart(
        name=element.attrib["name"],
        current=state["current"],
        maximum=state["maximum"],
    )


def body_to_xml(body: Body) -> ET.Element:
    element = ET.Element("body")
    element.append(bodypart_to_xml(body.head))
    element.append(bodypart_to_xml(body.torso))
    element.append(bodypart_to_xml(body.arm_r))
    element.append(bodypart_to_xml(body.arm_l))
    element.append(bodypart_to_xml(body.leg_r))
    element.append(bodypart_to_xml(body.leg_l))
    return element


def xml_to_body(element: ET.Element) -> Body:
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
    element = ET.Element("pawns")
    for pawn in pawns:
        element.append(pawn_to_xml(pawn))
    return element


def xml_to_pawns_list(elements: ET.Element) -> List[Pawn]:
    return [xml_to_pawn(pawn) for pawn in elements]


def save_state_to_xml(teams: List[Team], pawns: List[Pawn]) -> ET.Element:
    root = ET.Element("data")
    pawns = pawns_list_to_xml(pawns)
    teams = teams_list_to_xml(teams)
    root.append(pawns)
    root.append(teams)
    return root


def xml_to_save_state(element: ET.Element):
    pawns = xml_to_pawns_list(element.find("pawns"))
    teams = xml_to_teams_list(element.find("teams"))
    return pawns, teams
