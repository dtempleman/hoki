# # import xml.etree.ElementTree as ET
# # from abc import ABC, abstractmethod
# # from dataclasses import dataclass, fields
# # from enum import Enum

# from hoki.models.body import Body, BodyPart
# from hoki.models.player import Player
# from hoki.models.savable import Savable
# from hoki.models.statblock import StatBlock
from hoki.save_manager import save_state_to_xml, xml_to_save_state


def test_save_and_load_savestate(create_teams, fill_teams_with_pawns):
    teams = create_teams()
    pawns = fill_teams_with_pawns(teams)

    root = save_state_to_xml(
        teams,
        pawns,
    )

    new_pawns, new_teams = xml_to_save_state(root)

    assert len(teams) == len(new_teams)
    assert len(pawns) == len(new_pawns)

    for i, t in enumerate(teams):
        assert t == new_teams[i]
    for i, p in enumerate(pawns):
        assert p.id == new_pawns[i].id
        assert p.position == new_pawns[i].position
        assert p.shoots == new_pawns[i].shoots
