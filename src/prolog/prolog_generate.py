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

        event_type = transition.events[0].type if len(transition.events) != 0 else "nil"
        event_parameter = transition.events[0].parameter if len(transition.events) != 0 else "nil"
        event_str = f'event({event_type}, "{event_parameter}")' if len(transition.events) != 0 else "nil"

        if len(transition.guards) == 0:
            guard_str = "nil"
        else:
            guard_str = '"'
            for i in range(len(transition.guards)):
                guard = transition.guards[i]
                if i != 0:
                    guard_str += "; "

                guard_str += guard.condition
            guard_str += '"'

        actions_parameter_str = ""
        for i in range(len(transition.actions)):
            action = transition.actions[i]
            if i != 0:
                actions_parameter_str += "; "
            actions_parameter_str += f'{action.parameter}'

        action_str = f'action({transition.actions[0].type}, "{actions_parameter_str}")' if len(transition.actions) != 0 else "nil"

        prolog_code += f"transition({src}, {dest}, {event_str}, {guard_str}, {action_str}).\n" 

    return prolog_code
