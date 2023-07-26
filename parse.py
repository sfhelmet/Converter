import re

def parse_prolog_file(prolog_file):
    states = set()
    transitions = []

    with open(prolog_file, 'r') as file:
        final_state = ""
        for line in file:
            line = line.strip()
            if line.startswith('initial('):
                state = line.replace('initial(', '').replace(').', '')
                states.add(state)
                transitions.append(('[*]', state, "nil", "nil", "nil"))
            elif line.startswith('final('):
                state = line.replace('final(', '').replace(').', '')
                final_state = state
                states.remove(state)
            elif line.startswith('state('):
                state = line.replace('state(', '').replace(').', '')
                if state != final_state:
                    states.add(state)
            elif line.startswith('transition('):
                _, content = line.split('(', 1)
                params_text, _ = content.split('.', 1)
                params_text = params_text[:-1]

                params = re.findall(r'[\w]+(?:\([^)]*\))?', params_text)
                source, destination, event, guard, action = params
                if destination == final_state:
                    destination = '[*]'
                transitions.append((source, destination, event, guard, action))

    return states, transitions

def generate_plantuml(states, transitions):
    plantuml_code = "@startuml\n"
    for state in states:
        plantuml_code += f"state {state}\n"

    plantuml_code += "\n"

    for source, destination, event, _, _ in transitions:
        if source == '[*]' or destination == '[*]':
            arrow_type = " --> "
        if event != "nil":
            plantuml_code += f"{source} {arrow_type} {destination} : {event}\n"
        else:
            plantuml_code += f"{source} {arrow_type} {destination}\n"

        arrow_type = " -> "
    plantuml_code += "@enduml\n"
    return plantuml_code

def write_plantuml_code_to_file(plantuml_code, output_file):
    with open(output_file, 'w') as file:
        file.write(plantuml_code)