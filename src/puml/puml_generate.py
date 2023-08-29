import os
import sys

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(root_path)

from model.state import State
from model.transition import Transition
from puml.puml_constants import SPECIAL_STATE, ENTRY_STEROTYPE, EXIT_STEROTYPE

def generate_plantuml(states: dict[str: State], transitions: set[Transition]):
    plantuml_code = "@startuml\n\n"
    for state in states:
        if states[state].superstate:
            continue

        elif states[state].entries or states[state].exits or states[state].substates:
            plantuml_code += generate_substates(states[state], states)

        else:
            plantuml_code += f"state {states[state].name}\n" if not states[state].is_final else ""

    plantuml_code += "\n"

    arrow_type = " ---> "
    for transition in transitions:
        dest = transition.destination
        src = transition.source
        if states.get(transition.destination, State('dummy')).is_final:
            dest = SPECIAL_STATE
        elif transition.source == "__INIT":
            src = SPECIAL_STATE
        plantuml_code += f"{src} {arrow_type} {dest}"  

        if transition.events or transition.guards or transition.actions:
            plantuml_code += " :"
            if transition.events:
                plantuml_code += generate_events(transition.events)

            if transition.guards:
                plantuml_code += f" [{generate_guards(transition.guards)}]"

            if transition.actions:
                plantuml_code += generate_action(transition.actions)
                
        plantuml_code += "\n"
        arrow_type = " ---> "
    plantuml_code += "\n@enduml\n"
    return plantuml_code

def generate_substates(state: State, states: dict[str:State], indent =  0) -> str:
    indent_str = "\t" * indent
    substate_code = f"{indent_str}state {state.name}"

    if state.entries or state.exits or state.substates:
        substate_code += " {\n"
        for entry in state.entries:
            substate_code += f"{indent_str}\tstate {entry} {ENTRY_STEROTYPE}\n"
        for exit in state.exits:
            substate_code += f"{indent_str}\tstate {exit} {EXIT_STEROTYPE}\n"
        
        for child in state.substates:
            substate_code += generate_substates(states[child], states, indent + 1)

        substate_code += indent_str + "}"

    substate_code += "\n"
    return substate_code

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