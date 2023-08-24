import os
import sys

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(root_path)

from model.state import State
from model.transition import Transition

from enum import Enum


class Event(Enum):
    CALL = "call"
    SIGNAL = "signal"
    TIME = "time"
    CHANGE = "change"

    INACTIVITY = "inactivity"
    UPDATE = "update"
    COMPLETION = "completion"

def generate_prolog(states: dict[str:State], transitions: set[Transition]) -> str:
    prolog_code = ""
    initial_states = []
    final_states = []
    super_states = []
    for state_name in states:
        state = states[state_name]
        if state.is_initial:
            initial_states.append(state.name)
        if state.is_final:
            final_states.append(state.name)
        if state.superstate:
            super_states.append(state.name)
        else:
            prolog_code += "state(" + state.name + ").\n"

            
    for initial_state in initial_states:
        prolog_code += "initial(" + initial_state + ").\n"
    
    for final_state in final_states:
        prolog_code += "final(" + final_state + ").\n"
    
    for alias in final_states:
        prolog_code += "alias(" + alias + ", '').\n"

    for state in super_states:
        prolog_code += "superstate(" + states[state].superstate + ", " + state + ").\n"

    prolog_code += "\n"

    for transition in transitions:
        src = transition.source
        
        dest = transition.destination
        event = 'event(call, "' + transition.event + '")' if transition.event else "nil"
        guard = add_quote(transition.guard) if transition.guard else "nil"
        action = 'action(log, "' + transition.action + '")' if transition.action else "nil"

        prolog_code += "transition(" + src + ", " + dest + ", " + event + ", " + guard + ", " + action + ").\n" 

    return prolog_code


def write_prolog_code_to_file(prolog_code: str, output_file: str) -> None:
    with open(output_file, 'w') as file:
        file.write(prolog_code)

def add_quote(string: str) -> str:
    string.replace("'", "\'")
    string.replace('"', '\"')

    return '"' + string + '"'      

