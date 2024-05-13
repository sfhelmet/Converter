class Action:
    def __init__(self, type, parameter) -> None:
        self.type = type
        self.parameter = parameter

    def __str__(self) -> str:
        return self.parameter
    
    def __hash__(self) -> int:
        return hash(f"{self.type} {self.parameter}")
    
    def __repr__(self) -> str:
        return f"Action({self.type}, {self.parameter})"