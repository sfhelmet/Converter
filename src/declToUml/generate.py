import os
import sys

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(root_path)

from model.state import State
from model.transition import Transition
import re
from parse import get_params, strip_binary

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
            dest = f"[*]"
        elif transition.source == "__INIT":
            src = f"[*]"
        plantuml_code += f"{src} {arrow_type} {dest}"  

        if transition.event or transition.guard or transition.action:
            plantuml_code += " :"
            if transition.event:
                plantuml_code += generate_event(transition)

            if transition.guard:
                plantuml_code += f" [{strip_binary(transition.guard)}]"

            if transition.action:
                plantuml_code += generate_action(transition)
                
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
            substate_code += f"{indent_str}\tstate {entry} <<entryPoint>>\n"
        for exit in state.exits:
            substate_code += f"{indent_str}\tstate {exit} <<exitPoint>>\n"
        
        for child in state.substates:
            substate_code += generate_substates(states[child], states, indent + 1)

        substate_code += indent_str + "}"

    substate_code += "\n"
    return substate_code

def generate_event(transition: Transition) -> str:
    # pattern = r'event\((\w+),\s*(?:b)?["\']?([^"\']+)?["\']?\)'
    # matches = re.findall(pattern, transition.event)
    type, event = get_params(transition.event)
    if type == "call":
        return f" {event}"
    else:
        return f" {type} {event}"

def generate_action(transition: Transition) -> str:
    # There's always a b in front of function name
    # pattern = r'action\((\w+), b\s*["\']?((?:[^"\']+)|(?:"(?:\\.|[^"\\])*")|(?:\'(?:\\.|[^\'\\])*\'))["\']?\)'
    # matches = re.findall(pattern, transition.action)
    type, action = get_params(transition.action)
    if type == "exec":
        return f" / {action}"
    elif type == "log":
        return f" / log {action}"
    else:
        return f" /{transition.action}"


def write_plantuml_code_to_file(plantuml_code: str, output_file: str) -> None:
    with open(output_file, 'w') as file:
        file.write(plantuml_code)