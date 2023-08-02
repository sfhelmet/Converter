from query import *
from fact import State, Transition

file_load("./db/decl.pl")

states = {}
states_list = state("X")

for state in states_list:
    states[state] = (State(state["X"]))

transitions = {}
transitions_list = transition("X", "Y", "E", "G", "A")

for transition in transitions_list:
    transitions.add(Transition(transition["X"], transition["Y"], transition["E"], transition["G"], transition["A"]))

initial_state = initial("X")
final_state = final("X")







