from enum import Enum
INITIAL_STATE = "[*]"
FINAL_STATE = "[*]"
ENTRY_STEREOTYPE = "entryPoint"
EXIT_STEREOTYPE = "exitPoint"
CHOICE_STEREOTYPE = "choice"
JUNCTION_STEREOTYPE = "start"
ARROW_TYPE = "-->"
STATE_BEHAVIOR = "State Behavior"

START_PUML = "@startuml"
END_PUML = "@enduml"

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

class NoteType(Enum):
    ON_ENTRY = "Entry"
    DO_ACTION = "Do"
    ON_EXIT =  "Exit"
    INTERNAL_TRANSITION = "Internal Transition"


EVENT_TYPES = {EventType.CALL, EventType.SIGNAL, EventType.TIME, EventType.CHANGE, EventType.INACTIVITY, EventType.UPDATE, EventType.COMPLETION} 
NOTE_TYPES = {NoteType.ON_ENTRY, NoteType.DO_ACTION, NoteType.ON_EXIT}


