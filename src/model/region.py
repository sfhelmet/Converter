class Region:
    def __init__(self, name) -> None:
        self.name: str = name
        self.superstate = None
        self.substates = set()
        self.transitions = set()

    def __repr__(self) -> str:
        return f"Region({self.name})"