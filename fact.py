class State:
    def __init__(self, name) -> None:
        self.name = name

class Transition:
    def __init__(self, source, destination, event=None, guard=None, action=None) -> None:
        self.source = source
        self.destination = destination
        self.event = event
        self.guard = guard
        self.action = action