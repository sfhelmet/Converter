class State:
    def __init__(self, name) -> None:
        self.name = name
        self.is_final = False
        self.is_initial = False
        self.entries = set()
        self.exits = set()
        self.superstate = None
        self.substates = set()