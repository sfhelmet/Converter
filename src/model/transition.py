from model.event import Event
from model.guard import Guard
from model.action import Action

class Transition:
    def __init__(self, source, destination, events: list[Event]=[], guards: list[Guard]=[], actions: list[Action]=[]) -> None:
        self.source = source
        self.destination = destination
        self.events = events
        self.guards = guards
        self.actions = actions

    def __str__(self) -> str:
        return f"{self.source} -> {self.destination} : {self.events} : {self.guards} : {self.actions}"