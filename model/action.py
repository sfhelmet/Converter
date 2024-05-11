class Action:
    def __init__(self, type, parameter) -> None:
        self.type = type
        self.parameter = parameter

    def __str__(self) -> str:
        return self.parameter
    
    def __hash(self) -> int:
        return hash(f"{self.type} {self.parameter}")