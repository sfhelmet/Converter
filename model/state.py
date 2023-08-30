class State:
    def __init__(self, name) -> None:
        self.name = name
        self.is_final = None
        self.is_initial = None
        self.entries = set()
        self.exits = set()
        self.superstate = None
        self.substates = set()
        self.transitions = set()
        self.choice = False