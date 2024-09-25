import ast
import xml.etree.ElementTree as ET
from abc import ABC
from dataclasses import dataclass, fields
from enum import Enum
from typing import get_args, get_origin


@dataclass
class Savable(ABC):
    def __post_init__(self):
        for name, field_type in self.__annotations__.items():
            if field_type in [int, float, str]:
                if not isinstance(self.__dict__[name], field_type):
                    self.__dict__[name] = field_type(self.__dict__[name])

    def to_xml(self) -> ET.Element:
        """
        Convert the Savable object into Xml format
        """
        elements = []
        attributes = {}
        for field in fields(self):
            value = getattr(self, field.name)

            if isinstance(value, Savable):
                elements.append(value.to_xml())

            elif isinstance(value, Enum):
                attributes[field.name] = value.name

            elif isinstance(value, list) and isinstance(value[0], Savable):
                for v in value:
                    elements.append(v.to_xml())

            else:
                attributes[field.name] = str(value)

        element = ET.Element(self.__class__.__name__, attrib=attributes)
        for e in elements:
            element.append(e)
        return element

    @classmethod
    def from_xml(cls, element: ET.Element):
        """
        Create a Savable object from a Xml formatted Element Tree.

        Args:
            element (ET.Element): the element to create the Savable from
        """

        values = {}
        for field in fields(cls):
            if get_origin(field.type) == list:
                class_type = get_args(field.type)[0]
                if issubclass(class_type, Savable):
                    values[field.name] = [
                        class_type.from_xml(e)
                        for e in element.findall(class_type.__name__)
                    ]
                else:
                    values[field.name] = ast.literal_eval(element.attrib[field.name])

            elif issubclass(field.type, Savable):
                elements = element.findall(field.type.__name__)
                if len(elements) == 1:
                    values[field.name] = field.type.from_xml(elements[0])
                else:
                    field_element = [
                        e for e in elements if e.attrib["name"] == field.name
                    ][0]
                    values[field.name] = field.type.from_xml(field_element)

            elif issubclass(field.type, Enum):
                values[field.name] = field.type[element.attrib[field.name]]
            else:
                values[field.name] = element.attrib[field.name]
        return cls(**values)
