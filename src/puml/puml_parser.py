import os
import sys

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(root_path)

from model.state import State
from model.transition import Transition
from model.event import Event
from model.guard import Guard
from model.action import Action

from src.puml.puml_constants import *
from src.logger_config import logger

ARROWSTICK_TYPE = {"-", "l", "r", "u", "d"}

def parse_plantuml(puml_file): 
    states: dict[str, State] = {}
    transitions: set[Transition] = set()
    superstate_stack: list[str] = []
    region_stack: list[int] = [1]

    instate_actions: dict[str, dict[str, list[str] | set[str]]] = {}
    with open(puml_file, 'r') as file:
        
        for line in file:
            if line := line.strip():                
                if line.startswith(END_PUML):
                    logger.debug("End of PlantUML file Found")
                    break
                
                elif line.startswith(START_PUML):
                    logger.debug("Start of PlantUML file Found")
                    continue
                
                if line.isspace():
                    continue
                
                elif line.startswith("'"):
                    continue

                elif line == "--":
                    region_stack[-1] += 1
                    states[superstate_stack[-1]].region_count = str(int(states[superstate_stack[-1]].region_count) + 1)
                    continue

                elif line.startswith('}'):
                    superstate_stack.pop()
                    region_stack.pop()
                    continue

                elif line.startswith('state '):
                    state_name = line.split()[1].lower() if line.split()[1][-1] != ":" else line.split()[1][:-1].lower()

                    # "state" can be a state name
                    if state_name[0] == "-":
                        logger.warning('state name "state" found')
                        transitions.add(__parse_transition(line, states, superstate_stack, region_stack))
                        continue

                    states[state_name] = __create_state(line, state_name, states, instate_actions, superstate_stack, region_stack)
                
                elif (state_name := line[:line.find(":")].strip().lower()) in states and ">" not in line:
                    entry_actions, do_actions, exit_actions, internal_transitions_set = __parse_state_behavior(line, state_name.lower())
                    if state_name in states:
                        states[state_name].on_entry_actions = entry_actions
                        states[state_name].do_actions = do_actions
                        states[state_name].on_exit_actions = exit_actions
                        states[state_name].internal_transitions = internal_transitions_set
                    else:
                        instate_actions[state_name] = {"on_entry": entry_actions, "do_action": do_actions, "on_exit": exit_actions, "internal_transitions": internal_transitions_set}

                    logger.debug(f'State Behavior of "{state_name}" created')

                else:
                    new_transition = __parse_transition(line, states, superstate_stack, region_stack)
                    if new_transition:
                        if len(superstate_stack) != 0:
                            states[superstate_stack[-1]].transitions.add(new_transition)
                            transitions.add(new_transition)  
                        else:
                            transitions.add(new_transition)         
    return states, transitions

def __parse_state_behavior(line: str, state_name: str):
    on_entry_index = line.find(NoteType.ON_ENTRY.value)
    do_action_index = line.find(NoteType.DO_ACTION.value)
    on_exit_index = line.find(NoteType.ON_EXIT.value)

    # ON ENTRY
    on_entry_string = line[on_entry_index:]
    start = on_entry_string.find(":")
    end = on_entry_string.find("\\n")

    _, _, entry_actions = __parse_ega("/" + on_entry_string[start + 1:end].strip())

    # DO ACTION
    do_action_string = line[do_action_index:]
    start = do_action_string.find(":")
    end = do_action_string.find("\\n")

    _, _, do_actions = __parse_ega("/" + do_action_string[start + 1:end].strip())

    # ON EXIT
    on_exit_string = line[on_exit_index:]
    start = on_exit_string.find(":")
    end = on_exit_string.find("\\n")

    _, _, exit_actions = __parse_ega("/" + on_exit_string[start + 1:end])

    # INTERNAL TRANSITIONS
    internal_transitions_index = line.find(NoteType.INTERNAL_TRANSITION.value)
    internal_transitions_set = set()
    if internal_transitions_index != -1:
        internal_transitions = line[internal_transitions_index:].split("\\n")
        
        for internal_transition in internal_transitions:
            if internal_transition.startswith(NoteType.INTERNAL_TRANSITION.value):
                internal_transitions_set.add(Transition(state_name, state_name, *__parse_ega(internal_transition)))
    
    return entry_actions, do_actions, exit_actions, internal_transitions_set

def __create_state(line: str, state_name: str, states: dict[str, State], instate_actions: dict[str, dict], superstate_stack: list[str], region_stack: list[int]) -> State:
    new_state = State(state_name.lower())
    if state_name in instate_actions:
        state_behavior = instate_actions[state_name]
        new_state.on_entry_actions = state_behavior["on_entry"]
        new_state.do_actions = state_behavior["do_action"]
        new_state.on_exit_actions = state_behavior["on_exit"]
        new_state.internal_transitions = state_behavior["internal_transitions"]

        instate_actions.pop(state_name)
    
    new_state.region = str(region_stack[-1])
    __connect_superstate(new_state, superstate_stack, states)
    
    left_stereotype = line.find("<<")
    right_stereotype = line.find(">>")
    stereotype = line[left_stereotype + 2:right_stereotype]
    if stereotype == CHOICE_STEREOTYPE:
        new_state.choice = True

    if stereotype == JUNCTION_STEREOTYPE:
        new_state.junction = True

    if stereotype == ENTRY_STEREOTYPE:
        new_state.entry = True
        
    if stereotype == EXIT_STEREOTYPE:
        new_state.exit = True

    if line.split()[-1] == "{":
        superstate_stack.append(state_name)
        region_stack.append(1)
    
    entry_actions, do_actions, exit_actions, internal_transitions_set = __parse_state_behavior(line, state_name.lower())
    new_state.on_entry_actions = entry_actions
    new_state.do_actions = do_actions
    new_state.on_exit_actions = exit_actions
    new_state.internal_transitions = internal_transitions_set

    logger.debug(f'"{state_name}" created')
    return new_state

def __connect_superstate(state: State, superstate_stack: list[str], states: dict[str:State]) -> None:
    if len(superstate_stack) >= 1:
        state.superstate = superstate_stack[-1]
        states[superstate_stack[-1]].substates.add(state.name)

        
def __parse_transition(transition: str, states: dict[str:State], superstate_stack: list[str], region_stack: list[int]) -> Transition:
    events, guards, actions = [], [] ,[]
    dash_index = transition.find("-")
    greater_index = transition.find(">")

    if dash_index == -1 or greater_index == -1:
        logger.error(f'"{transition}" is not valid PlantUML')
        return None
    
    for i in range(dash_index + 1, greater_index):
        if transition[i] not in ARROWSTICK_TYPE:
            logger.error(f'"{transition}" is not valid PlantUML')
            return None
        
    colon_index = transition.find(":")
    src = transition[:dash_index].strip().lower()

    # This makes sure an arrow is not inputed accidentally
    if src == "":
        logger.error(f'"{transition}" is not valid PlantUML')
        return None
        
    if colon_index == -1:
        dest = transition[greater_index + 1:].strip().lower()
    else:
        dest = transition[greater_index + 1: colon_index].strip().lower()

        ega = transition[colon_index + 1:]
        events, guards, actions = __parse_ega(ega)

    if src not in states and src != INITIAL_STATE:
        new_state = State(src)
        states[src] = new_state
        logger.debug(f'"{src}" created by transition')

    if dest not in states and dest != FINAL_STATE:
        new_state = State(dest)
        states[dest] = new_state
        logger.debug(f'"{dest}" created by transition')

    if src == INITIAL_STATE:
        states[dest].is_initial = True
        return None
    
    elif dest == FINAL_STATE:
        if len(superstate_stack) == 0:
            dest = "final"
        elif region_stack[-1] > 1:
            dest = superstate_stack[-1] + "_final" + str(region_stack[-1])
        else:
            dest = superstate_stack[-1] + "_final"

        if dest not in states:
            new_state = State(dest)
            new_state.is_final = True
            states[dest] = new_state
            logger.debug(f'"{dest}" created by transition')

    __connect_superstate(states[src], superstate_stack, states)
    __connect_superstate(states[dest], superstate_stack, states)
    
    new_transition = Transition(src, dest, events=events, guards=guards, actions=actions)
    logger.debug(f'"{new_transition.source}" to "{new_transition.destination}" created')
    return new_transition
    
def __parse_ega(ega: str) -> tuple[Event, Guard, Action]:
    slash = ega.find("/")
    l_bracket = ega.find("[")
    r_bracket = ega.find("]")

    if l_bracket != -1:
        event = ega[:l_bracket].strip()

    elif slash != -1:
        event = ega[:slash].strip()
    
    else:
        event = ega.strip()

    guard = ega[l_bracket + 1: r_bracket].strip() if l_bracket != -1 and r_bracket != -1 else ""
    action = ega[slash + 1:].strip() if slash != -1 else ""

    events_str = event.split(";") if event else []
    guards_str = guard.split(";") if guard else []
    actions_str = action.split(";") if action else []

    events = []
    for event_str in events_str:
        if event_str.split()[0] not in EVENT_TYPES:
            events.append(Event("call", event_str.strip()))

    guards = [Guard(condition.strip()) for condition in guards_str]

    actions = []
    for action_str in actions_str:
        actions.append(Action("log", action_str.strip()))

    return events, guards, actions