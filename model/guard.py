class Guard:
    def __init__(self, condition) -> None:
        self.condition = condition

    def __str__(self) -> str:
        return self.condition
    
    def __hash(self) -> int:
        return hash(self.condition)