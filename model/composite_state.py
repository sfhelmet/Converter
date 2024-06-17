from typing import Optional, Set
from model.region import Region
from model.state import State
from model.transition import Transition


class CompositeState(State):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.entry_pseudostate: Optional[str] = None
        self.exit_pseudostate: Optional[str] = None
        self.substates: Set[State] = set()
        self.transitions: Set[Transition] = set()
        self.regions: Set[Region] = set()

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

    def add_substate(self, substate: State) -> None:
        self.substates.add(substate)

    def __repr__(self) -> str:
        return f"CompositeState({self.name}, substates={self.substates})"