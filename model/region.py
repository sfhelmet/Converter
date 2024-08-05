from typing import Optional, Set
from model.state import State
from model.state_interface import StateInterface
from model.transition import Transition

class Region(StateInterface):
    def __init__(self, name) -> None:
        self._name: str = name
        self._superstate: Optional[str] = None
        self.substates: Set[State] = set()
        self.transitions: Set[Transition] = set()

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @property
    def superstate(self):
        return self._superstate

    @superstate.setter
    def superstate(self, value):
        self._superstate = value

    def __repr__(self) -> str:
        return f"Region({self.name})"