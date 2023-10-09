import pytest
from src.puml.puml_parser import parse_ega

@pytest.mark.unit
def test_parse_ega():
    ega = "event1 [guard1] / action1"
    events, guards, actions = parse_ega(ega)
    assert events[0].parameter == "event1"
    assert guards[0].condition == "guard1"
    assert actions[0].parameter == "action1"