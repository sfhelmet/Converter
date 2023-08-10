from fact import State, Transition
import re
def generate_substates(states):
    pass

def generate_plantuml(states: dict[str: State], transitions: set[Transition]):
    plantuml_code = "@startuml\n\n"
    for state in states:
        if states[state].entries or states[state].exits or states[state].substates:
            plantuml_code += f"state {states[state].name} {{\n"
            for sub in states[state].substates:
                plantuml_code += f"\tstate {sub}\n"
            for entry in states[state].entries:
                plantuml_code += f"\tstate {entry} <<entryPoint>>\n"
            for exit in states[state].exits:
                plantuml_code += f"\tstate {exit} <<exitPoint>>\n"
            plantuml_code += "}\n"

        elif states[state].superstate:
            continue

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
                pattern = r'event\((\w+),\s*(?:b)?["\']?([^"\']+)?["\']?\)'
                matches = re.findall(pattern, transition.event)
                print(matches)
                type, event = matches[0]
                if type == "call":
                    plantuml_code += f" {event}"
                else:
                    plantuml_code += f" {type} {event}"

            if transition.guard:
                plantuml_code += f" [{transition.guard}]"

            if transition.action:
                # There's always a b in front of function name
                pattern = r'action\((\w+), b\s*["\']?((?:[^"\']+)|(?:"(?:\\.|[^"\\])*")|(?:\'(?:\\.|[^\'\\])*\'))["\']?\)'
                matches = re.findall(pattern, transition.action)
                type, action = matches[0] # try catch maybe?
                if type == "exec":
                    plantuml_code += f" / {action[:-3]}"
                else:
                    plantuml_code += f" /{transition.action}"

        plantuml_code += "\n"
        arrow_type = " ---> "
    plantuml_code += "\n@enduml\n"
    return plantuml_code

def write_plantuml_code_to_file(plantuml_code, output_file):
    with open(output_file, 'w') as file:
        file.write(plantuml_code)