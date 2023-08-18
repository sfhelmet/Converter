class Transition:
    def __init__(self, source, destination, event=None, guard=None, action=None) -> None:
        self.source = source
        self.destination = destination
        self.event = event if event != "nil" else None
        self.guard = guard if guard != "nil" else None
        self.action = action if action != "nil" else None