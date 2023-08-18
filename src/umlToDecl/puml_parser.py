import os
import sys

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(root_path)

from model.state import State
from model.transition import Transition

def create_state(name, states):
    if name not in states:
        states[name] = State(name)

    return states[name]

def parse_plantuml_file(puml_file):
    states = {}
    transitions = set()

    with open(puml_file, 'r') as file:
        for line in file:
            if line.strip():
                line = line.strip()

                event, guard, action = None, None, None
                if line.startswith('@'):
                    continue

                elif line.startswith('state '):
                    state_name = line.split()[1]

                    # "state" can be a state name
                    if state_name[0] == "-":
                        continue

                    new_state = State(state_name)
                    states[state_name] = (new_state)

                else:
                    dash_index = line.find("-")
                    greater_index = line.find(">")
                    colon_index = line.find(":")
                    src = line[:dash_index].strip()
                    if colon_index == -1:
                        dest = line[greater_index + 1:].strip()
                    else:
                        dest = line[greater_index + 1: colon_index].strip()

                        ega = line[colon_index + 1:]
                        event, guard, action = parse_ega(ega)

                    if src == "[*]":
                        states[dest].is_initial = True
                        continue

                    if dest == "[*]":
                        dest = "final"
                        if dest not in states:
                            new_state = State("final")
                            new_state.is_final = True
                            states[dest] = new_state

                    new_transition = Transition(src, dest, event=event, guard=guard, action=action)
                    transitions.add(new_transition)
            
    return states, transitions


def parse_ega(ega: str):
    slash = ega.find("/")
    l_bracket = ega.find("[")
    r_bracket = ega.find("]")

    if l_bracket != -1:
        event = ega[:l_bracket].strip()

    elif slash != -1:
        event = ega[:slash].strip()
    
    else:
        event = ega.strip()

    guard = ega[l_bracket + 1: r_bracket].strip() if l_bracket != -1 and r_bracket != -1 else None
    action = ega[slash:].strip() if slash != -1 else None

    return event, guard, action