class State:
    def __init__(self, name) -> None:
        self.name = name
        self.is_final = False
        self.is_initial = False
        self.entries = set()
        self.exits = set()
        self.superstate = None
        self.substates = set()

class Transition:
    def __init__(self, source, destination, event=None, guard=None, action=None) -> None:
        self.source = source
        self.destination = destination
        self.event = event if event != "nil" else None
        self.guard = guard if guard != "nil" else None
        self.action = action if action != "nil" else None