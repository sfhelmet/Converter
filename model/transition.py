class Action:
    def __init__(self, type, parameter) -> None:
        self.type = type
        self.parameter = parameter

    def __str__(self) -> str:
        return self.parameter
    
    def __hash__(self) -> int:
        return hash(f"{self.type} {self.parameter}")
    
    def __repr__(self) -> str:
        return f"Action({self.type}, {self.parameter})"
    
class Event:
    def __init__(self, type, parameter) -> None:
        self.type = type
        self.parameter = parameter
        self.key: str = ""

    def __str__(self) -> str:
        return self.parameter
    
    def __hash__(self) -> int:
        return hash(self.type + self.parameter)

    def __repr__(self) -> str:
        return f"Event({self.type}, {self.parameter})"
    
class Guard:
    def __init__(self, condition) -> None:
        self.condition = condition

    def __str__(self) -> str:
        return self.condition
    
    def __hash__(self) -> int:
        return hash(self.condition)
    
    def __repr__(self) -> str:
        return f"Guard({self.condition})"
 
class Proc:
    def __init__(self, procedure) -> None:
        self.procedure = procedure

    def __str__(self) -> str:
        return self.procedure
    
class EgaDict:
  def __init__(self, event_dict: set[str, Event] = {}, guard_dict: set[str, Guard] = {}, action_dict: set[str, Action] = {}) -> None:
    self.event_dict: set[str, Event] = event_dict
    self.guard_dict: set[str, Guard] = guard_dict
    self.action_dict: set[str, Action] = action_dict

  def __repr__(self) -> str:
    return f"{self.event_dict}\n{self.guard_dict}\n{self.action_dict}"
  
  def get_dicts(self):
    return self.event_dict, self.guard_dict, self.action_dict

class Transition:
    def __init__(self, source, destination, events: list[Event]=[], guards: list[Guard]=[], actions: list[Action]=[]) -> None:
        self.source = source
        self.destination = destination
        self.events = events
        self.guards = guards
        self.actions = actions

    def __str__(self) -> str:
        return f"{self.source} -> {self.destination} : {self.events} : {self.guards} : {self.actions}"