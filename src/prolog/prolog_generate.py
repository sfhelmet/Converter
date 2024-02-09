import os
import sys

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(root_path)

from model.state import State
from model.transition import Transition
from model.action import Action
from prolog.prolog_constants import *

def generate_prolog(states: dict[str:State], transitions: set[Transition]) -> str:
    prolog_code = ""
    initial_states = []
    final_states = []
    super_states = []
    choice = []
    entry_pseudostates = []
    exit_pseudostates = []
    on_entry_actions_list = []
    do_actions_list = []
    on_exit_actions_list = []
    internal_transitions_list = []
    for state_name in states:
        state = states[state_name]
        if state.superstate or state.entry or state.exit:
            if state.superstate:
                super_states.append(state.name)
            if state.entry:
                entry_pseudostates.append(state.name)
            if state.exit:
                exit_pseudostates.append(state.name)
        else:
            prolog_code += f"{STATE_PREFIX}({state.name}).\n"

        if state.is_initial:
            initial_states.append(state.name)
        if state.is_final:
            final_states.append(state.name)
        if state.choice:
            choice.append(state.name)
        if state.on_entry_actions:
            on_entry_actions_list.append(state.name)
        if state.do_actions:
            do_actions_list.append(state.name)
        if state.on_exit_actions:
            on_exit_actions_list.append(state.name)
        if state.internal_transitions:
            internal_transitions_list.append(state.name)
        
    for initial_state in initial_states:
        prolog_code += f"{INITIAL_PREFIX}({initial_state}).\n"
    
    for final_state in final_states:
        prolog_code += f"{FINAL_PREFIX}({final_state}).\n"
    
    for alias in final_states:
        prolog_code += f"{ALIAS_PREFIX}({alias}, '').\n"

    for state in super_states:
        if not states[state].entry and not states[state].exit:
            prolog_code += f"{SUPERSTATE_PREFIX}({states[state].superstate}, {state}).\n"

    for state in choice:
        prolog_code += f"{CHOICE_STATE_PREFIX}({state}). % choice state\n"

    for entry_pseudostate in entry_pseudostates:
        for transition in transitions:
            if transition.source == entry_pseudostate:
                prolog_code += f"{ENTRY_PSEUDOSTATE_PREFIX}({entry_pseudostate}, {transition.destination}).\n"
                break
        
    for exit_pseudostate in exit_pseudostates:
        prolog_code += f"{EXIT_PSEUDOSTATE_PREFIX}({exit_pseudostate}, {states[exit_pseudostate].superstate}).\n"

    for on_entry_action_state in on_entry_actions_list:
        for action in states[on_entry_action_state].on_entry_actions:
            if action.parameter:
                prolog_code += f"{ON_ENTRY_ACTION_PREFIX}({on_entry_action_state}, {create_action_string(action)}).\n"

    for do_action_state in do_actions_list:
        for proc in states[do_action_state].do_actions:
            prolog_code += f"{DO_ACTION_PREFIX}({do_action_state}, {create_proc_string(proc)}).\n"

    for on_exit_action_state in on_exit_actions_list:
        for action in states[on_exit_action_state].on_exit_actions:
            if action.parameter:
                prolog_code += f"{ON_EXIT_ACTION_PREFIX}({on_exit_action_state}, {create_action_string(action)}).\n"

    for internal_transition_state in internal_transitions_list:
        for transition in states[internal_transition_state].internal_transitions:
            src, _, event_str, guard_str, action_str = create_transition_ega(transition)
            prolog_code += f"{INTERNAL_TRANSITION_PREFIX}({src}, {event_str}, {guard_str}, {action_str}).\n"
                
    prolog_code += "\n"

    for transition in transitions:
        src, dest, event_str, guard_str, action_str = create_transition_ega(transition)
        prolog_code += f"{TRANSITION_PREFIX}({src}, {dest}, {event_str}, {guard_str}, {action_str}).\n"
    return prolog_code
def create_transition_ega(transition: Transition) -> str:
        src = transition.source
        dest = transition.destination

        event_type = transition.events[0].type if len(transition.events) != 0 else NIL
        event_parameter = transition.events[0].parameter if len(transition.events) != 0 else NIL
        event_str = f'{EVENT_PREFIX}({event_type}, "{event_parameter}")' if len(transition.events) != 0 else NIL

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

        action_str = f'{ACTION_PREFIX}({transition.actions[0].type}, "{actions_parameter_str}")' if len(transition.actions) != 0 else NIL

        return src, dest, event_str, guard_str, action_str

def create_action_string(action: Action) -> str:
    return f'{ACTION_PREFIX}({action.type}, "{action.parameter}")'

def create_proc_string(proc: str) ->str:
    return f'{PROCEDURE_PREFIX}("{proc}")'