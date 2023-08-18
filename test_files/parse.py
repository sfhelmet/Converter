import re
from model.fact import *

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