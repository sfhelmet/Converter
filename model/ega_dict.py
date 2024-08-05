import os
import sys
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(root_path)

from .event import Event
from .guard import Guard
from .action import Action

class EgaDict:
  def __init__(self, event_dict: set[str, Event] = {}, guard_dict: set[str, Guard] = {}, action_dict: set[str, Action] = {}) -> None:
    self.event_dict: set[str, Event] = event_dict
    self.guard_dict: set[str, Guard] = guard_dict
    self.action_dict: set[str, Action] = action_dict

  def __repr__(self) -> str:
    return f"{self.event_dict}\n{self.guard_dict}\n{self.action_dict}"
  
  def get_dicts(self):
    return self.event_dict, self.guard_dict, self.action_dict
  