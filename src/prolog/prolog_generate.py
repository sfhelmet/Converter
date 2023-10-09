import os
import sys

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(root_path)

from model.state import State
from model.transition import Transition
from prolog.prolog_constants import NIL

def generate_prolog(states: dict[str:State], transitions: set[Transition]) -> str:
    prolog_code = ""
    initial_states = []
    final_states = []
    super_states = []
    choice = []
    entry_pseudostates = []
    exit_pseudostates = []
    for state_name in states:
        state = states[state_name]
        if state.is_initial:
            initial_states.append(state.name)
        if state.is_final:
            final_states.append(state.name)
        if state.superstate:
            super_states.append(state.name)
        if state.choice:
            choice.append(state.name)
        if state.entry:
            entry_pseudostates.append(state.name)
        if state.exit:
            exit_pseudostates.append(state.name)
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

    for state in choice:
        prolog_code += f"state({state}). % choice state\n"

    # for entry_pseudostate in entry_pseudostates:
    #     prolog_code += f"entry_pseudostate({entry_pseudostate}, ).\n"
        
    for exit_pseudostate in exit_pseudostates:
        prolog_code += f"exit_pseudostate({exit_pseudostate}, {states[exit_pseudostate].superstate}).\n"

    prolog_code += "\n"

    for transition in transitions:
        src = transition.source
        dest = transition.destination

        event_type = transition.events[0].type if len(transition.events) != 0 else NIL
        event_parameter = transition.events[0].parameter if len(transition.events) != 0 else NIL
        event_str = f'event({event_type}, "{event_parameter}")' if len(transition.events) != 0 else NIL

        if len(transition.guards) == 0:
            guard_str = NIL
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

        action_str = f'action({transition.actions[0].type}, "{actions_parameter_str}")' if len(transition.actions) != 0 else NIL

        prolog_code += f"transition({src}, {dest}, {event_str}, {guard_str}, {action_str}).\n" 

    return prolog_code
