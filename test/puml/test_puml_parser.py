import pytest
from src.puml.puml_parser import parse_ega

@pytest.mark.unit
def test_parse_ega():
    ega = "event1 [guard1] / action1"
    events, guards, actions = parse_ega(ega)
    assert events[0].parameter == "event1"
    assert guards[0].condition == "guard1"
    assert actions[0].parameter == "action1"

@pytest.mark.unit
def test_parse_ega_list():
    ega = "event1; event2 [guard1; guard2] / action1; action2"
    events, guards, actions = parse_ega(ega)
    assert str(events[0]) == "event1"
    assert str(events[1]) == "event2"
    assert str(guards[0]) == "guard1"
    assert str(guards[1]) == "guard2"
    assert str(actions[0]) == "action1"
    assert str(actions[1]) == "action2"
