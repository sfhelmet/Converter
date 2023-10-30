class Event:
    def __init__(self, type, parameter) -> None:
        self.type = type
        self.parameter = parameter

    def __str__(self) -> str:
        return self.parameter
