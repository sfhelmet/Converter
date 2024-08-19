import os
import sys

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(root_path)

from states import State
from transition import Transition, EgaDict
from constants import *

def generate_mermaid(states: dict[str: State], transitions: set[Transition], ega_dict, legend: bool = False) -> str:
    event_dict, guard_dict, action_dict = ega_dict.get_dicts()
    plantuml_code = f"{STATE_DIAGRAM_HEADER}\n\n"
    # Generate States
    for state in states:
        if states[state].superstate:
            continue
        
        elif states[state].entries or states[state].exits or states[state].substates:
            plantuml_code += generate_substates(states[state], states, legend)

        else:
            plantuml_code += f"{STATE_STRING} {states[state].name}" if not states[state].is_final else ""
            if states[state].choice:
                plantuml_code += f" <<{CHOICE_STEREOTYPE}>>"

            elif states[state].junction:
                plantuml_code += f" <<{JUNCTION_STEREOTYPE}>>"
            
            elif internal_transitions := states[state].internal_transitions:
                plantuml_code += ":"
                for internal_transition in internal_transitions:
                    
                    plantuml_code += f" {NoteType.INTERNAL_TRANSITION.value}: {generate_ega(internal_transition, legend)}\\n"

            plantuml_code += "\n"


    # Generate Transitions
    for transition in transitions:
        plantuml_code += generate_transitions(transition, states, legend)
        plantuml_code += "\n"

    if legend:
        plantuml_code += f'{LEGEND} "Event Legend\\n'
        for event in event_dict:
            plantuml_code += f'{event_dict[event]} : {event.type} {event.parameter}\\n'

        plantuml_code += f'" as event_legend\n'

        plantuml_code += f'{LEGEND} "Guard Legend\\n'
        for guard in guard_dict:
            plantuml_code += f'{guard_dict[guard]} : {guard.condition}\\n'

        plantuml_code += f'" as guard_legend\n'

        plantuml_code += f'{LEGEND} "Action Legend\\n'
        for action in action_dict:
            plantuml_code += f'{action_dict[action]} : {action.type} {action.parameter}\\n'

        plantuml_code += f'" as action_legend\n'

    return plantuml_code

def generate_transitions(transition, states, legend: bool):
    plantuml_code = ""
    dest = transition.destination
    src = transition.source
    if states.get(dest, State('dummy')).is_final:
        dest = FINAL_STATE
    elif transition.source.startswith("__INIT"):
        src = INITIAL_STATE
    plantuml_code += f"{src} {ARROW_TYPE} {dest}"  

    plantuml_code += f" : {generate_ega(transition, legend)}"
        
    return plantuml_code
                

def generate_substates(state: State, states: dict[str:State], legend: bool, indent =  0) -> str:
    TAB = "\t"
    indent_str = TAB * indent
    substate_code = ""
    on_entry_actions = state.on_entry_actions
    do_actions = state.do_actions
    on_exit_actions = state.on_exit_actions
    internal_transitions = state.internal_transitions
    if on_exit_actions or on_entry_actions or do_actions or internal_transitions:
        substate_code += f'{indent_str}{state.name}: '

        if on_entry_actions:
            substate_code += f'{NoteType.ON_ENTRY.value}: {on_entry_actions[0].type} {on_entry_actions[0].parameter}'
            for i in range(1, len(on_entry_actions)):
                substate_code += f'; {on_entry_actions[i].type} {on_entry_actions[i].parameter}'
            substate_code += '\\n'

        if do_actions:
            substate_code += f'{NoteType.DO_ACTION.value}: {do_actions[0].procedure}'
            for i in range(1, len(do_actions)):
                substate_code += f'; {do_actions[i].procedure}'
            substate_code += '\\n'

        if on_exit_actions:
            substate_code += f'{NoteType.ON_EXIT.value}: {on_exit_actions[0].type} {on_exit_actions[0].parameter}'
            for i in range(1, len(on_exit_actions)):
                substate_code += f'; {on_exit_actions[i].type} {on_exit_actions[i].parameter}'
            substate_code += '\\n'

        if internal_transitions := state.internal_transitions:
            for internal_transition in internal_transitions:
                substate_code += f"{NoteType.INTERNAL_TRANSITION.value}: {generate_ega(internal_transition, legend)}\\n"

        substate_code += '\n'
    if not state.is_final:
        substate_code += f"{indent_str}{STATE_STRING} {state.name}"      
    if state.choice == True:
        substate_code += f"<<{CHOICE_STEREOTYPE}>>"

    elif state.junction == True:
        substate_code += f"<<{JUNCTION_STEREOTYPE}>>"
    
    if state.entries or state.exits or state.substates or state.region_count > 1:
        substate_code += " {\n"

        if state.region_count <= 1:
            for entry in state.entries:
                substate_code += f"{indent_str}{TAB}{STATE_STRING} {entry} <<{ENTRY_STEREOTYPE}>>\n"
            for exit in state.exits:
                substate_code += f"{indent_str}{TAB}{STATE_STRING} {exit} <<{EXIT_STEREOTYPE}>>\n"
        for i, region in enumerate(state.substates):
            for child in state.substates[region]:
                substate_code += generate_substates(states[child], states, legend, indent + 1)
            if i != len(state.substates) - 1:
                substate_code += f"{indent_str}{TAB}{REGION_SEPERATOR_VERTICAL}\n"

        for transition in state.transitions:
            substate_code += indent_str + TAB + generate_transitions(transition, states, legend) + "\n"

        substate_code += indent_str + "}\n"

    substate_code += "\n"
    return substate_code

def generate_ega(transition, legend) -> str:
    subcode = ""
    subcode += generate_events(transition.events, legend)

    if transition.guards:
        subcode += f" [{generate_guards(transition.guards, legend)}]"

    if transition.actions:
        subcode += generate_action(transition.actions, legend)

    return subcode

def generate_events(events, legend) -> str:
    if len(events) == 0:
        return EPSILON
    event_str = ""
    for i in range(len(events)):
        event = events[i]

        if i != 0:
            event_str += " ;"

        if legend:
            event_str += event.key
        # Mermaid does not allow colons (:) in string
        elif event.type == "call":
            event_str += f" {event.parameter.replace(':', '-')}"
        else:
            event_str += f" {event.type} {event.parameter.replace(':', '-')}"

    return event_str

def generate_guards(guards, legend) -> str:
    guard_str = ""
    for i in range(len(guards)):
        guard = guards[i]

        if i != 0:
            guard_str += "; "
        
        if legend:
            guard_str += guard.key
        else:
            guard_str += f"{guard.condition}"

    return guard_str

def generate_action(actions, legend) -> str:
    action_str = " /"
    for i in range(len(actions)):
        action = actions[i]
        if i != 0:
            action_str += "; "
        
        if legend:
            action_str += action.key
        else:
            action_str += f"{action.type} {action.parameter.replace(';', ',')}"
    return action_str