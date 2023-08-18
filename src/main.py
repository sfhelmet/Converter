from query import *
from model.fact import State, Transition
from generate import generate_plantuml, write_plantuml_code_to_file

file_load("./db/decl.pl")

states = {}
states_list = state("Name")

for state in states_list:
    states[state["Name"]] = (State(state["Name"]))

transitions = set()
transitions_list = transition("X", "Y", "E", "G", "A")

for transition in transitions_list:
    transitions.add(Transition(transition["X"], transition["Y"], transition["E"], transition["G"], transition["A"]))

final_states = final("X")
for final_state in final_states:
    states[final_state["X"]].is_final = True

initial_states = initial("X")
for initial_state in initial_states:
    states[initial_state["X"]].is_initial = True
    transitions.add(Transition("__INIT", initial_state["X"]))

superstate_pairs = superstate("Superstate", "Substate")
for pair in superstate_pairs:
    sup = pair["Superstate"]
    sub = pair["Substate"]
    states[sup].substates.add(sub)
    states[sub] = State(sub)
    states[sub].superstate = sup

entries = entry_pseudostate("Entry", "Substate")
for entry in entries:
    sub = entry["Substate"]
    entry_state = entry["Entry"]

    states[states[sub].superstate].entries.add(entry_state)
    transitions.add(Transition(entry_state, sub))
    
exits = exit_pseudostate("Exit", "Superstate")
for exit in exits:
    sup = exit["Superstate"]
    exit_state = exit["Exit"]

    states[sup].exits.add(exit_state)

uml_code = generate_plantuml(states, transitions)
write_plantuml_code_to_file(uml_code, "./PUML/plantUML.puml")










