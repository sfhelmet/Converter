import os
import sys

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(root_path)

from model.state import State
from model.transition import Transition
from model.event import Event
from model.guard import Guard
from model.action import Action
from model.proc import Proc
from prolog.query import *
from prolog.prolog_constants import NIL, BYTES_TYPE_AS_STRING, UTF8_CONSTANT
from src.util.parse import get_params

from src.logger_config import logger

def parse_prolog():
    
    logger.debug("Reading Prolog File")
    states = {}
    states_list = get_state("Name")

    for state in states_list:
        states[state["Name"]] = (State(state["Name"]))

    transitions = set()
    transitions_list = get_transition("X", "Y", "E", "G", "A")

    region_list = get_region("Sup", "Region")
    region_count = {}
    regions = set()

    for region_object in region_list:
        sup = region_object["Sup"]
        region = region_object["Region"]

        region_count[sup] = region_count.get(sup, 0) + 1
        regions.add(region)

    superstate_pairs = get_substate("Superstate", "Substate")
    for pair in superstate_pairs:
        sup = pair["Superstate"]
        sub = pair["Substate"]

        states[sub] = State(sub)
        if sup in regions:
            states[sub].region = sup
        else:
            states[sup].substates.add(sub)
            states[sub].superstate = sup

    for region_name in region_count:
        states[region_name].region_count = region_count[region_name]

    for transition in transitions_list:
        src = transition["X"]
        dest = transition["Y"]
        event = parse_event(transition["E"])
        guard = parse_guard(transition["G"])
        action = parse_action(transition["A"])
        
        if src not in states or dest not in states:
            continue
        
        new_transitions = Transition(src, dest, event, guard, action)
        src_superstate = states[src].superstate
        dest_superstate = states[dest].superstate

        if not src_superstate and not dest_superstate:
            transitions.add(new_transitions)

        elif not src_superstate:
            states[states[dest].superstate].transitions.add(new_transitions)
        else:
            states[states[src].superstate].transitions.add(new_transitions)    

    final_states = get_final("X")
    for final_state in final_states:
        states[final_state["X"]].is_final = True

    initial_states = get_initial("X")
    i = 1
    for initial_state in initial_states:
        states[initial_state["X"]].is_initial = True
        superstate = get_substate("Sup", initial_state["X"])
        if len(superstate) == 0:
            transitions.add(Transition(f"__INIT{i}", initial_state["X"]))
        else:
            states[superstate[0]['Sup']].transitions.add(Transition(f"__INIT{i}_{superstate[0]['Sup']}", initial_state["X"]))
        i += 1

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

    on_exit_actions = get_onexit_action("State", "Action")
    
    for on_exit_action in on_exit_actions:
        state = on_exit_action["State"]
        action = on_exit_action["Action"]
        action_type = get_params(action)[0]
        param = bytes_to_string(get_params(action)[1])
        # states[state].on_exit_actions.append(Action(type, param))
        add_item(states, state, "on_exit_actions", Action(action_type, param))

    on_entry_actions = get_onentry_action("State", "Action")
    for on_entry_action in on_entry_actions:
        state = on_entry_action["State"]
        action = on_entry_action["Action"]
        action_type = get_params(action)[0]
        param = bytes_to_string(get_params(action)[1])
        # states[state].on_entry_actions.append(Action(type, param))
        add_item(states, state, "on_entry_actions", Action(action_type, param))
        
    do_actions = get_do_action("State", "Proc")
    for do_action in do_actions:
        state = do_action["State"]
        procedure = do_action["Proc"]
        # states[state].do_actions.append(Proc(bytes_to_string(get_params(procedure)[0])))
        add_item(states, state, "do_actions", Proc(bytes_to_string(get_params(procedure)[0])))

    internal_trasitions = get_internal_transition("State", "Event", "Guard", "Action")
    for internal_transition in internal_trasitions:
        state = internal_transition["State"]
        event = parse_event(internal_transition["Event"])
        guard = parse_guard(internal_transition["Guard"])
        action = parse_action(internal_transition["Action"])
        
        transition = Transition(state, state, event, guard, action)
        # states[state].internal_transitions.add(transition)
        add_item(states, state, "internal_transitions", transition)

    logger.debug("End of Reading Prolog File")
    return states, transitions  

def add_item(states, state, name, what):
    if state not in states:
        logger.warning(f"State {state} does not exists, ignoring {name}: {what}")
    else:
        getattr(states[state], name).add(what)

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
    actions_list = []

    if transition_action == NIL:
        return actions_list

    if type(transition_action) is list:
        for action in transition_action:
            actions_params = get_params(action)
            action_type = actions_params[0].strip()
            action_parameter = bytes_to_string(actions_params[1])
            actions_list.append(Action(action_type, action_parameter))
                    
    else:
        actions_params = get_params(transition_action)
        action_type = actions_params[0].strip()
        action_parameter = bytes_to_string(actions_params[1])
        actions_list.append(Action(action_type, action_parameter))

    return actions_list

def create_action(action_string):
    actions_params = get_params(action_string)
    action_type = actions_params[0].strip()
    action_parameter = bytes_to_string(actions_params[1])
    return Action(action_type, action_parameter)

def bytes_to_string(string):
  if str(type(string)) == BYTES_TYPE_AS_STRING:
      return string.decode(UTF8_CONSTANT)
  if string.startswith("b'") or string.startswith('b"'):
    return str(string)[2:-1]
  return string