import os
import sys

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(root_path)

from model.state import State
from model.transition import Transition
from model.event import Event
from model.guard import Guard
from model.action import Action
from enum import Enum

class EventType(Enum):
    CALL = "call"
    SIGNAL = "signal"
    TIME = "time"
    CHANGE = "change"

    INACTIVITY = "inactivity"
    UPDATE = "update"
    COMPLETION = "completion"

class ActionType(Enum):
    LOG = "log"

EVENT_TYPES = {EventType.CALL, EventType.SIGNAL, EventType.TIME, EventType.CHANGE, EventType.INACTIVITY, EventType.UPDATE, EventType.COMPLETION} 

def parse_plantuml(puml_file):
    states = {}
    transitions = set()
    superstate_stack = []
    with open(puml_file, 'r') as file:
        
        for line in file:
            if line.strip():
                line = line.strip()

                if line.startswith('@') or line.isspace():
                    continue
                
                elif line.startswith('}'):
                    superstate_stack.pop()
                    continue

                elif line.startswith('state '):
                    state_name = line.split()[1]

                    # "state" can be a state name
                    if state_name[0] == "-":
                        transitions.add(parse_transition(line, states, transitions, superstate_stack))
                        continue

                    new_state = State(state_name)
                    connect_superstate(new_state, superstate_stack, states)

                    if line.split()[-1] == "{":
                        superstate_stack.append(state_name)
                    states[state_name] = (new_state)

                else:
                    new_transition = parse_transition(line, states, transitions, superstate_stack)
                    if new_transition:
                        transitions.add(new_transition)
    return states, transitions

def connect_superstate(state: State, superstate_stack: list[str], states: dict[str:State]):
    if len(superstate_stack) >= 1:
        state.superstate = superstate_stack[-1]
        states[superstate_stack[-1]].substates.add(state.name)

        
def parse_transition(transition: str, states: dict[str:State], transitions: set[Transition], superstate_stack) -> Transition:
    events, guards, actions = [], [] ,[]
    dash_index = transition.find("-")
    greater_index = transition.find(">")
    colon_index = transition.find(":")
    src = transition[:dash_index].strip()
    if colon_index == -1:
        dest = transition[greater_index + 1:].strip()
    else:
        dest = transition[greater_index + 1: colon_index].strip()

        ega = transition[colon_index + 1:]
        events, guards, actions = parse_ega(ega)

    if src not in states and src != "[*]":
        new_state = State(src)
        states[src] = new_state

    if dest not in states and dest != "[*]":
        new_state = State(dest)
        states[dest] = new_state

    if src == "[*]":
        states[dest].is_initial = True
        return None
    
    elif dest == "[*]":
        dest = "final"
        if dest not in states:
            new_state = State("final")
            new_state.is_final = True
            states[dest] = new_state

    connect_superstate(states[src], superstate_stack, states)
    connect_superstate(states[dest], superstate_stack, states)
    
    new_transition = Transition(src, dest, events=events, guards=guards, actions=actions)
    return new_transition
    
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

    guard = ega[l_bracket + 1: r_bracket].strip() if l_bracket != -1 and r_bracket != -1 else ""
    action = ega[slash + 1:].strip() if slash != -1 else ""

    events_str = event.split(";") if event else []
    guards_str = guard.split(";") if guard else []
    actions_str = action.split(";") if action else []

    events = []
    for event_str in events_str:
        if event_str.split()[0] not in EVENT_TYPES:
            events.append(Event("call", event_str))

    guards = [Guard(condition) for condition in guards_str]

    actions = []
    for action_str in actions_str:
        actions.append(Action("log", action_str))

    return events, guards, actions