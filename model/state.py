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
        self.exit = False
        self.entry = False
        self.on_exit_actions = []
        self.on_entry_actions = []
        self.do_actions = []
        self.internal_transitions = set()
