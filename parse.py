import re
from fact import *

def create_state(name, states):
    if name not in states:
        states[name] = State(name)

    return states[name]

def parse_prolog_file(prolog_file):
    states = {}
    transitions = []
    pending = {}

    with open(prolog_file, 'r') as file:
        final_state = ''
        for line in file:
            line = line.strip()

            if line.startswith('initial('):
                state = line.replace('initial(', '').replace(').', '')
                
                if state not in states:
                    states[state] = (State(state))
                transitions.append(('[*]', state, "nil", "nil", "nil"))

            elif line.startswith('final('):
                state = line.replace('final(', '').replace(').', '')
                final_state = state
                states[state].is_final = True

            elif line.startswith('state('):
                state = line.replace('state(', '').replace(').', '')
                if state != final_state:
                    states[state] = (State(state))

            elif line.startswith('entry_pseudostate('):
                _, content = line.split('(', 1)
                params, _ = content.split(').', 1)
                entry, state = params.split(',')
                entry = entry.strip()
                state = state.strip()
                
                if state not in states:
                    pending[state] = entry
                else:
                    state.superstate.entries.append(entry)

                transitions.append((entry, state, "nil", "nil", "nil"))

            elif line.startswith('exit_pseudostate('):
                _, content = line.split('(', 1)
                params, _ = content.split(').', 1)
                exit, state = params.split(',')
                exit = exit.strip()
                state = state.strip()
                states[state].exits.append(exit)

            elif line.startswith('transition('):
                _, content = line.split('(', 1)
                params_text, _ = content.split(').', 1)

                params = re.findall(r'[\w]+(?:\([^)]*\))?', params_text)
                source, destination, event, guard, action = params
                if destination == final_state:
                    destination = '[*]'
                transitions.append((source, destination, event, guard, action))

            elif line.startswith('superstate('):
                _, content = line.split('(', 1)
                params, _ = content.split(').', 1)
                sup, sub = params.split(',')
                sup = sup.strip()
                sub = sub.strip()

                create_state(sub, states)

                states[sup].substates.add(sub)
                states[sub].superstate = sup

                if sub in pending:
                    states[sup].entries.append(pending[sub])
                    pending.pop(sub)

    return states, transitions

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