from model.state_interface import StateInterface

class State(StateInterface):
    def __init__(self, name: str) -> None:
        self._name: str = name
        self._superstate = None
        self.region = None
        self.entries = set()
        self.exits = set()
        self.substates = set()
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
