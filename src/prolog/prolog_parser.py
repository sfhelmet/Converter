import os
import sys

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(root_path)

from model.state import State
from model.transition import Transition
from model.event import Event
from model.guard import Guard
from model.action import Action
from prolog.query import *
from prolog.prolog_constants import NIL, BYTES_TYPE_AS_STRING, UTF8_CONSTANT
from parse import get_params

def parse_prolog():
    states = {}
    states_list = get_state("Name")

    for state in states_list:
        states[state["Name"]] = (State(state["Name"]))

    transitions = set()
    transitions_list = get_transition("X", "Y", "E", "G", "A")

    superstate_pairs = get_superstate("Superstate", "Substate")
    for pair in superstate_pairs:
        sup = pair["Superstate"]
        sub = pair["Substate"]
        states[sup].substates.add(sub)
        states[sub] = State(sub)
        states[sub].superstate = sup

    for transition in transitions_list:
        src = transition["X"]
        dest = transition["Y"]
        event = parse_event(transition["E"])
        guard = parse_guard(transition["G"])
        action = parse_action(transition["A"])
        
        new_transitions = Transition(src, dest, event, guard, action)
        src_superstate = get_superstate("Sup", src)
        dest_superstate = get_superstate("Sup", dest)
        print("src", src_superstate, src)
        print("dest", dest_superstate, dest)

        if len(src_superstate) == 0 and len(dest_superstate) == 0:
            transitions.add(new_transitions)

        elif len(src_superstate) == 0:
            states[states[dest].superstate].transitions.add(new_transitions)
        else:
            states[states[src].superstate].transitions.add(new_transitions)    

    final_states = get_final("X")
    for final_state in final_states:
        states[final_state["X"]].is_final = True

    initial_states = get_initial("X")
    for initial_state in initial_states:
        states[initial_state["X"]].is_initial = True
        transitions.add(Transition("__INIT", initial_state["X"]))

    entries = get_entry_pseudostate("Entry", "Substate")
    for entry in entries:
        sub = entry["Substate"]
        entry_state = entry["Entry"]

        states[states[sub].superstate].entries.add(entry_state)
        transitions.add(Transition(entry_state, sub))
        
    exits = get_exit_pseudostate("Exit", "Superstate")
    for exit in exits:
        sup = exit["Superstate"]
        exit_state = exit["Exit"]

        states[sup].exits.add(exit_state)

    return states, transitions

def parse_event(transition_event) -> list[Event]:
    if transition_event == NIL:
            event = []

    else:
        event_params = get_params(transition_event)
        event_type = event_params[0].strip()
        event_parameter = bytes_to_string(event_params[1])
        event = [Event(event_type, event_parameter)]
    
    return event

def parse_guard(transition_guard) -> list[Guard]:
    if transition_guard == NIL:
        guards_list = []

    else:
        guards_str = bytes_to_string(transition_guard).strip()
        guards = guards_str.split(";")
        guards_list = []
        for guard in guards:
            guard_condition = guard.strip()
            guards_list.append(Guard(guard_condition))
            
    return guards_list

def parse_action(transition_action) -> list[Action]:
    if transition_action == NIL:
        actions_list = []

    else:
        actions_params = get_params(transition_action)
        action_type = actions_params[0].strip()
        action_parameter = bytes_to_string(actions_params[1])
        actions = action_parameter.split(";")
        actions_list = []
        for action in actions:
            actions_list.append(Action(action_type, action.strip()))

    return actions_list

def bytes_to_string(string):
  if str(type(string)) == BYTES_TYPE_AS_STRING:
      return string.decode(UTF8_CONSTANT)
  if string.startswith("b'") or string.startswith('b"'):
    return str(string)[2:-1]
  return string