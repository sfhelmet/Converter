from fact import State

def generate_plantuml(states: list[State], transitions: list[tuple[str, str, str, str, str]]):
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
    for source, destination, event, _, _ in transitions:
        if source == '[*]' or destination == '[*]':
            arrow_type = " ---> "
        if event != "nil":
            plantuml_code += f"{source} {arrow_type} {destination} : {event}\n"
        else:
            plantuml_code += f"{source} {arrow_type} {destination}\n"

        arrow_type = " ---> "
    plantuml_code += "\n@enduml\n"
    return plantuml_code

def write_plantuml_code_to_file(plantuml_code, output_file):
    with open(output_file, 'w') as file:
        file.write(plantuml_code)