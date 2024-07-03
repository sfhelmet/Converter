from .states import StateInterface
from .transition import Transition
from typing import Dict, Set

class FiniteStateMachine():
    def __init__(self) -> None:
        states: Dict[StateInterface] = {}
        transitions: Set[Transition] = {}

    