import os
import sys

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(root_path)

from model.state import State
from model.transition import Transition

from puml_parser import parse_plantuml_file



def generate_prolog(states: dict[str:State], transition: set[Transition]) -> None:
    prolog_code = ""
    initial_states = []
    final_states = []
    for state_name in states:
        state = states[state_name]
        if state.is_initial:
            initial_states.append(state.name)
        if state.is_final:
            final_states.append(state.name)
        prolog_code += "state(" + state.name + ").\n"
        
    for initial_state in initial_states:
        prolog_code += "initial(" + initial_state + ").\n"
    
    for final_state in final_states:
        prolog_code += "final(" + final_state + ").\n"
    
    for alias in final_states:
        prolog_code += "alias(" + alias + ", '').\n"

    return prolog_code


def write_prolog_code_to_file(prolog_code: str, output_file: str) -> None:
    with open(output_file, 'w') as file:
        file.write(prolog_code)


states, transitions = parse_plantuml_file("./PUML/input.puml")
prolog_code = generate_prolog(states, transitions)
write_prolog_code_to_file(prolog_code=prolog_code, output_file="./db/output.pl")