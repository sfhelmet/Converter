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