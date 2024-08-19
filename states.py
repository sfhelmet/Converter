from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional, Set
from transition import Transition

class PseudostateType(Enum):
    INITIAL = "Initial"
    FINAL = "Final"
    ENTRY = "Entry"
    EXIT = "Exit"
    CHOICE = "Choice"
    JUNCTION = "Junction"

class StateInterface(ABC):
    @property
    @abstractmethod
    def name(self):
        """Get the name of the state."""
        pass

    @name.setter
    @abstractmethod
    def name(self, value):
        """Set the name of the state."""
        pass

    @property
    @abstractmethod
    def superstate(self):
        """Get the superstate of the state."""
        pass

    @superstate.setter
    @abstractmethod
    def superstate(self, value):
        """Set the superstate of the state."""
        pass

class State(StateInterface):
    def __init__(self, name: str) -> None:
        self._name: str = name
        self._superstate = None
        self.region = None
        self.entries = set()
        self.exits = set()
        self.on_exit_actions = []
        self.on_entry_actions = []
        self.do_actions = []
        self.internal_transitions = set()

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
        return f"State({self.name})"

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
    
class CompositeState(State):
    def __init__(self, name: str = None, state_instance: State = None) -> None:
        if state_instance:
            # Copy constructor logic
            super().__init__(state_instance.name)
            self.__dict__.update(state_instance.__dict__)
            self.entry_pseudostate: Optional[str] = None
        else:
            super().__init__(name)
            
        self.entry_pseudostate: Optional[str] = None
        self.exit_pseudostate: Optional[str] = None
        self.substates: Set[str] = set()
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