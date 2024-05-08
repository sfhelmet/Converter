class State:
    def __init__(self, name) -> None:
        self.name: str = name
        self.is_final: bool = False
        self.is_initial: bool = False
        self.entries = set()
        self.exits = set()
        self.superstate = None
        self.substates = set()
        self.transitions = set()
        self.choice: bool = False
        self.junction: bool = False
        self.exit: bool = False
        self.entry: bool = False
        self.on_exit_actions = []
        self.on_entry_actions = []
        self.do_actions = []
        self.internal_transitions = set()
        self.region: str = "1"
        self.region_count: int = 1
