from abc import abstractmethod
from enum import Enum
from typing import Optional

from model.state_interface import StateInterface


class PseudostateType(Enum):
    INITIAL = "Initial"
    FINAL = "Final"
    ENTRY = "Entry"
    EXIT = "Exit"
    CHOICE = "Choice"
    JUNCTION = "Junction"

class Pseudostate(StateInterface):
    def __init__(self, name, type_, superstate=None):
        if not isinstance(type_, PseudostateType):
            raise ValueError(f"Invalid type: {type_}. Valid types are: {list(PseudostateType)}")
        self._name: str = name
        self._type: PseudostateType = type_
        self._superstate: Optional[str] = superstate

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def superstate(self) -> Optional[str]:
        return self._superstate

    @superstate.setter
    def superstate(self, value):
        self._superstate = value
    
    @property
    def type(self) -> PseudostateType:
        return self._type

    @type.setter
    def type(self, value):
        if not isinstance(value, PseudostateType):
            raise ValueError(f"Invalid type: {value}. Valid types are: {list(PseudostateType)}")
        self._type = value

    def __repr__(self) -> str:
        return f"{self.type.value}({self.name})"
