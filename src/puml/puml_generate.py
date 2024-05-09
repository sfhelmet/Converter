import os
import sys

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(root_path)

from model.state import State
from model.transition import Transition
from puml.puml_constants import *

def generate_plantuml(states: dict[str: State], transitions: set[Transition]):
    plantuml_code = f"{START_PUML}\n\n"
    # Generate States
    for state in states:
        if states[state].superstate:
            continue

        elif states[state].entries or states[state].exits or states[state].substates:
            plantuml_code += generate_substates(states[state], states)

        else:
            plantuml_code += f"state {states[state].name}" if not states[state].is_final else ""
            if states[state].choice:
                plantuml_code += f" <<{CHOICE_STEREOTYPE}>>"
            
            elif internal_transitions := states[state].internal_transitions:
                plantuml_code += ":"
                for internal_transition in internal_transitions:
                    
                    plantuml_code += f" {NoteType.INTERNAL_TRANSITION.value}: {generate_ega(internal_transition)}\\n"

            plantuml_code += "\n"


    # Generate Transitions
    for transition in transitions:
        plantuml_code += generate_transitions(transition, states)
        plantuml_code += "\n"
    plantuml_code += f"\n{END_PUML}\n"
    return plantuml_code

def generate_transitions(transition, states):
    plantuml_code = ""
    dest = transition.destination
    src = transition.source
    if states.get(transition.destination, State('dummy')).is_final:
        dest = FINAL_STATE
    elif transition.source.startswith("__INIT"):
        src = INITIAL_STATE
    plantuml_code += f"{src} {ARROW_TYPE} {dest}"  

    if transition.events or transition.guards or transition.actions:
        plantuml_code += f" : {generate_ega(transition)}"
        
    return plantuml_code
                

def generate_substates(state: State, states: dict[str:State], indent =  0) -> str:
    TAB = "\t"
    indent_str = TAB * indent
    substate_code = ""
    on_entry_actions = state.on_entry_actions
    do_actions = state.do_actions
    on_exit_actions = state.on_exit_actions
    internal_transitions = state.internal_transitions
    if on_exit_actions or on_entry_actions or do_actions or internal_transitions:
        substate_code += f'{indent_str}note "<<{STATE_BEHAVIOR}>>\\n'

        if on_entry_actions:
            substate_code += f'On Entry: {on_entry_actions[0].type} {on_entry_actions[0].parameter}'
            for i in range(1, len(on_entry_actions)):
                substate_code += f'; {on_entry_actions[i].type} {on_entry_actions[i].parameter}'
            substate_code += '\\n'

        if do_actions:
            substate_code += f'Do Action: {do_actions[0].procedure}'
            for i in range(1, len(do_actions)):
                substate_code += f'; {do_actions[i].procedure}'
            substate_code += '\\n'

        if on_exit_actions:
            substate_code += f'On Exit: {on_exit_actions[0].type} {on_exit_actions[0].parameter}'
            for i in range(1, len(on_exit_actions)):
                substate_code += f'; {on_exit_actions[i].type} {on_exit_actions[i].parameter}'
            substate_code += '\\n'

        if internal_transitions := state.internal_transitions:
            for internal_transition in internal_transitions:
                substate_code += f"{NoteType.INTERNAL_TRANSITION.value}: {generate_ega(internal_transition)}\\n"
        substate_code += f'" as N_{state.name} \n'
    
    if not state.is_final:
        substate_code += f"{indent_str}state {state.name}"      

    if state.choice == True:
        substate_code += f"<<{CHOICE_STEREOTYPE}>>"

    if state.entries or state.exits or state.substates:
        substate_code += " {\n"
        for entry in state.entries:
            substate_code += f"{indent_str}{TAB}state {entry} <<{ENTRY_STEREOTYPE}>>\n"
        for exit in state.exits:
            substate_code += f"{indent_str}{TAB}state {exit} <<{EXIT_STEREOTYPE}>>\n"
        
        for child in state.substates:
            substate_code += generate_substates(states[child], states, indent + 1)

        for transition in state.transitions:
            substate_code += indent_str + TAB + generate_transitions(transition, states) + "\n"

        substate_code += indent_str + "}\n"

    if on_exit_actions or do_actions or on_entry_actions or internal_transitions:
        substate_code += indent_str + "\n"
        substate_code += f"{indent_str}N_{state.name} --> {state.name}\n"

    substate_code += "\n"
    return substate_code

def generate_ega(transition):
    subcode = ""
    if transition.events:
        subcode += generate_events(transition.events)

    if transition.guards:
        subcode += f" [{generate_guards(transition.guards)}]"

    if transition.actions:
        subcode += generate_action(transition.actions)

    return subcode

def generate_events(events) -> str:
    event_str = ""
    for i in range(len(events)):
        event = events[i]

        if i != 0:
            event_str += " ;"

        if event.type == "call":
            event_str += f" {event.parameter}"
        else:
            event_str += f" {event.type} {event.parameter}"

    return event_str

def generate_guards(guards) -> str:
    guard_str = ""
    for i in range(len(guards)):
        guard = guards[i]

        if i != 0:
            guard_str += "; "
        guard_str += f"{guard.condition}"

    return guard_str

def generate_action(actions) -> str:
    action_str = " /"
    for i in range(len(actions)):
        action = actions[i]
        if i != 0:
            action_str += "; "

        action_str += f"{action.type} {action.parameter}"
    return action_str