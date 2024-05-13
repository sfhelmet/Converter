class Guard:
    def __init__(self, condition) -> None:
        self.condition = condition

    def __str__(self) -> str:
        return self.condition
    
    def __hash__(self) -> int:
        return hash(self.condition)
    
    def __repr__(self) -> str:
        return f"Guard({self.condition})"
    