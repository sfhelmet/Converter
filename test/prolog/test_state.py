import pytest
from src.prolog.prolog_parser import parse_prolog
from src.model.states import Pseudostate, PseudostateType

from src.prolog.query import get_state, get_initial, get_final, get_substate

STATES_PATH = "test/resources/state_test.pl"

@pytest.fixture(scope='module')
def parsed_prolog():
    states, transitions, ega_dict = parse_prolog(STATES_PATH)
    return states, transitions, ega_dict

@pytest.mark.unit
def test_parse_state(parsed_prolog):
    expected_states = [state["X"] for state in get_state("X")]

    states, _, _ = parsed_prolog
    
    states = [
        state for state, state_obj in states.items()
        if not state_obj.superstate
        ]
    assert len(states) == len(expected_states)

    for state in expected_states:
        assert state in states

def test_parse_initial_state(parsed_prolog):
    expected_initial_states = [state["X"] for state in get_initial("X")]

    states, _, _ = parsed_prolog

    initial_states = [
        state_name for state_name, state_obj in states.items()
        if isinstance(state_obj, Pseudostate) and state_obj.type == PseudostateType.INITIAL
    ]

    assert initial_states == expected_initial_states
    
def test_parse_final_state(parsed_prolog):
    expected_final_states = [state["X"] for state in get_final("X")]
    
    states, _, _ = parsed_prolog

    final_states = [
        state_name for state_name, state_obj in states.items()
        if isinstance(state_obj, Pseudostate) and state_obj.type == PseudostateType.FINAL
    ]

    assert final_states == expected_final_states

def test_parse_substate(parsed_prolog):
    expected_substates = set([state["Sub"] for state in get_substate("Sup", "Sub")])
    expected_superstates = set([state["Sup"] for state in get_substate("Sup", "Sub")])

    states, _, _ = parsed_prolog






