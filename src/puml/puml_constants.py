from enum import Enum
SPECIAL_STATE = "[*]"
ENTRY_STEREOTYPE = "entryPoint"
EXIT_STEREOTYPE = "exitPoint"
CHOICE_STEREOTYPE = "choice"
ARROW_TYPE = "-->"

class EventType(Enum):
    CALL = "call"
    SIGNAL = "signal"
    TIME = "time"
    CHANGE = "change"

    INACTIVITY = "inactivity"
    UPDATE = "update"
    COMPLETION = "completion"

class ActionType(Enum):
    LOG = "log"
EVENT_TYPES = {EventType.CALL, EventType.SIGNAL, EventType.TIME, EventType.CHANGE, EventType.INACTIVITY, EventType.UPDATE, EventType.COMPLETION} 


