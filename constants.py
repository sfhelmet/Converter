'''
Constants defined for prolog
'''

NIL = "nil"
BYTES_TYPE_AS_STRING = "<class 'bytes'>"
UTF8_CONSTANT = "utf-8"

STATE_PREFIX = "state"
TRANSITION_PREFIX = "transition"
INITIAL_PREFIX = "initial"
FINAL_PREFIX = "final"
ALIAS_PREFIX = "alias"
SUPERSTATE_PREFIX = "substate"
REGION_PREFIX = "region"
ENTRY_PSEUDOSTATE_PREFIX = "entry_pseudostate"
CHOICE_STATE_PREFIX = "choice"
JUNCTION_STATE_PREFIX = "junction"
EXIT_PSEUDOSTATE_PREFIX = "exit_pseudostate"
ON_ENTRY_ACTION_PREFIX = "onentry_action"
DO_ACTION_PREFIX = "do_action"
ON_EXIT_ACTION_PREFIX = "onexit_action"
EVENT_PREFIX = "event"
ACTION_PREFIX = "action"
PROCEDURE_PREFIX = "proc"
INTERNAL_TRANSITION_PREFIX = "internal_transition"


'''
Constants defined for Mermaid
'''

from enum import Enum
STATE_STRING = "state"
INITIAL_STATE = "[*]"
FINAL_STATE = "[*]"
ENTRY_STEREOTYPE = "entryPoint"
EXIT_STEREOTYPE = "exitPoint"
CHOICE_STEREOTYPE = "choice"
JUNCTION_STEREOTYPE = "start"
ARROW_TYPE = "-->"

STATE_DIAGRAM_HEADER = "stateDiagram"

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

REGION_SEPERATOR_VERTICAL = "||"
REGION_SEPERATOR_HORIZONTAL = "--"
LEGEND = "note"
EPSILON = 'ε'

'''
Constants defined for PlantUML
'''

from enum import Enum
STATE_STRING = "state"
INITIAL_STATE = "[*]"
FINAL_STATE = "[*]"
ENTRY_STEREOTYPE = "entryPoint"
EXIT_STEREOTYPE = "exitPoint"
CHOICE_STEREOTYPE = "choice"
JUNCTION_STEREOTYPE = "start"
ARROW_TYPE = "-->"

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

REGION_SEPERATOR_VERTICAL = "||"
REGION_SEPERATOR_HORIZONTAL = "--"
LEGEND = "note"
EPSILON = 'ε'