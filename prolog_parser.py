import os
import sys

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(root_path)

from query import file_load
from states import CompositeState, State, Pseudostate, PseudostateType, StateInterface, Region
from transition import Transition, Event, Guard, Action, Proc, EgaDict
from query import *
from constants import NIL, BYTES_TYPE_AS_STRING, UTF8_CONSTANT
from parse import get_params
from typing import Dict, Set

from logger_config import logger

event_counter = 1
guard_counter = 1
action_counter = 1
action_dict = {}
guard_dict = {}
event_dict = {}

def parse_prolog(path: str, legend: bool = False):
    file_load(path)
    global event_counter, event_dict, guard_counter, action_counter, guard_dict, action_dict
    logger.debug("Reading Prolog File")
    states: Dict[str, StateInterface] = {}
    states_list = [x["Name"] for x in get_state("Name")]
    choices_list = [x["Name"] for x in get_choice("Name")]
    junctions_list = [x["Name"] for x in get_junction("Name")]

    for state in states_list:
        states[state] = (State(state))

    for choice_name in choices_list:
        states[choice_name] = (Pseudostate(choice_name, PseudostateType.CHOICE))

    for junction_name in junctions_list: 
        states[junction_name] = (Pseudostate(junction_name, PseudostateType.JUNCTION))

    transitions: Dict[str, Transition] = {}
    transitions_list = get_transition("X", "Y", "E", "G", "A")

    region_list = get_region("Sup", "Region")
    regions: Dict[str, Region] = {}

    # for region_object in region_list:
    #     sup = region_object["Sup"]
    #     region = region_object["Region"]

    #     # regions[]

    superstate_pairs = get_substate("Superstate", "Substate")
    for pair in superstate_pairs:
        sup = pair["Superstate"]
        sub = pair["Substate"]
        if sub not in states:
            states[sub] = State(sub)
            states[sub].superstate = sup
        if sup in regions:
            states[sub].region = sup[-1]
            superstate_name = sup.split('_')[0]
            states[sub].superstate = superstate_name
            if superstate_name not in states:
                states[superstate_name] = State(superstate_name)
            states_set = states[superstate_name].substates.get(sup[-1], set([sub]))
            states_set.add(sub)
            states[superstate_name].substates[sup[-1]] = states_set
        else:
            if type(states[sup]) != CompositeState:
                states[sup] = CompositeState(state_instance=states[sup])
            states[sup].substates.add(sub)
            


    # for region_name in region_count:
    #     states[region_name].region_count = region_count[region_name]

    for transition in transitions_list:
        src = transition["X"]
        dest = transition["Y"]
        event = parse_event(transition["E"], legend)
        guard = parse_guard(transition["G"], legend)
        action = parse_action(transition["A"], legend)
        
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

    final_states = [x["X"] for x in get_final("X")]
    
    for final_state in final_states:
        new_final_state = Pseudostate(final_state, PseudostateType.FINAL)
        new_final_state.superstate = states[final_state].superstate
        states[final_state] = new_final_state

    initial_states = [x["X"] for x in get_initial("X")]
    for i, initial_state in enumerate(initial_states):
        
        new_initial_state = Pseudostate(initial_state, PseudostateType.INITIAL)
        new_initial_state.superstate = states[initial_state].superstate
        states[initial_state] = new_initial_state

        # State should only have 1 superstate
        superstates_list = [x["Sup"] for x in get_substate("Sup", initial_state)]
        superstate = None if not superstates_list else superstates_list[0]

        if not superstate:
            transitions[initial_state] = Transition(f"__INIT{i}", initial_state)
        else:
            states[superstate].transitions[initial_state] = Transition(f"__INIT{i}_{superstate}", initial_state)


    entries = get_entry_pseudostate("Entry", "Substate")
    for entry in entries:
        sub = entry["Substate"]
        if sub in regions:
            continue
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
        if type(action) is list:
            for a in action:
                action_type = get_params(action)[0]
                param = bytes_to_string(get_params(action)[1])
                add_item(states, state, "on_exit_actions", Action(action_type, param))
        else:
            action_type = get_params(action)[0]
            param = bytes_to_string(get_params(action)[1])
            # states[state].on_exit_actions.append(Action(type, param))
            add_item(states, state, "on_exit_actions", Action(action_type, param))

    on_entry_actions = get_onentry_action("State", "Action")
    for on_entry_action in on_entry_actions:
        state = on_entry_action["State"]
        action = on_entry_action["Action"]
        if type(action) is list:
            for a in action:
                action_type = get_params(a)[0]
                param = bytes_to_string(get_params(a)[1])
                add_item(states, state, "on_entry_actions", Action(action_type, param))
                    
        else:
            action_type = get_params(action)[0]
            param = bytes_to_string(get_params(action)[1])
            # states[state].on_entry_actions.append(Action(type, param))
            add_item(states, state, "on_entry_actions", Action(action_type, param))
        
    do_actions = get_do_action("State", "Proc")
    for do_action in do_actions:
        state = do_action["State"]
        procedure = do_action["Proc"]
        add_item(states, state, "do_actions", Proc(bytes_to_string(get_params(procedure)[0])))

    internal_trasitions = get_internal_transition("State", "Event", "Guard", "Action")
    for internal_transition in internal_trasitions:
        state = internal_transition["State"]
        event = parse_event(internal_transition["Event"], legend)
        guard = parse_guard(internal_transition["Guard"], legend)
        action = parse_action(internal_transition["Action"], legend)
        
        transition = Transition(state, state, event, guard, action)
        add_item(states, state, "internal_transitions", transition)

    logger.debug("End of Reading Prolog File")
    return states, transitions, EgaDict(event_dict, guard_dict, action_dict)

def add_item(states, state, name, what):
    if state not in states:
        logger.warning(f"State {state} does not exists, ignoring {name}: {what}")
    else:
        getattr(states[state], name).append(what)

def parse_event(transition_event: str, legend: bool) -> list[Event]:
    global event_counter, event_dict
    if transition_event == NIL:
        return []

    else:
        event_params = get_params(transition_event)
        event_type = event_params[0].strip()
        event_parameter = bytes_to_string(event_params[1])
        event = Event(event_type, event_parameter)
        if legend:
            if event not in event_dict:
                event_dict[event] = f"e{event_counter}"
                event.key = f"e{event_counter}"
                event_counter += 1
            else:
                event.key = event_dict[event]
    
    return [event]

def parse_guard(transition_guard, legend) -> list[Guard]:
    global guard_counter, guard_dict
    if transition_guard == NIL:
        guards_list = []
    
    else:
        guards_str = bytes_to_string(transition_guard).strip()
        guards = guards_str.split(";")
        guards_list = []
        for guard in guards:
            guard_condition = guard.strip()
            guard = Guard(guard_condition)
            if legend:
                if guard not in guard_dict:
                    guard_dict[guard] = f"g{guard_counter}"
                    guard.key = f"g{guard_counter}"
                    guard_counter += 1
                else:
                    guard.key = guard_dict[guard]
            guards_list.append(guard)
    return guards_list

def parse_action(transition_action, legend) -> list[Action]:
    global action_counter, action_dict
    actions_list = []

    if transition_action == NIL:
        return actions_list

    if type(transition_action) is list:
        for action_str in transition_action:
            actions_params = get_params(action_str)
            action_type = actions_params[0].strip()
            action_parameter = bytes_to_string(actions_params[1])
            action = Action(action_type, action_parameter)
            if legend:
                if action not in action_dict:
                    action_dict[action] = f"a{action_counter}"
                    action.key = f"a{action_counter}"
                    action_counter += 1
                else:
                    action.key = action_dict[action]
            actions_list.append(action)
                    
    else:
        actions_params = get_params(transition_action)
        action_type = actions_params[0].strip()
        action_parameter = bytes_to_string(actions_params[1])
        action = Action(action_type, action_parameter)
        if legend:
            if action not in action_dict:
                action_dict[action] = f"a{action_counter}"
                action.key = f"a{action_counter}"
                action_counter += 1
            else:
                action.key = action_dict[action]
        actions_list.append(action)

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