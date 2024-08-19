from states import StateInterface
from transition import EgaDict, Transition
from typing import Dict, Set, Callable, Tuple
from prolog_parser import parse_prolog

class FiniteStateMachine():
    def __init__(self) -> None:
        states: Dict[str, StateInterface] = {}
        transitions: Set[Transition] = {}
        ega_dict: EgaDict

    def read_prolog(self, path: str):
        self.states, self.transitions, self.ega_dict = parse_prolog(path)
        return self.states, self.transitions, self.ega_dict