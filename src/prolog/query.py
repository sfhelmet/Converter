import os
import sys

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(root_path)

from pyswip import Prolog

from src.util.logger_config import logger

prolog = Prolog()

def file_load(file_name):
  prolog.consult(file_name)

# {relations}({X}, {Y})
def __query_relation(relations, *args):
  query = f"{relations}({args[0]}"
  for i in range(1, len(args)):
    query += f", {args[i]}"
  query += ")"
  try:
    results = list(prolog.query(query))
  except:
    logger.debug(f"No {relations}s found")
    return []
  return results

#query_name
def get_state(var_name):
  return __query_relation("state", var_name)

def get_alias(var_name, alias):
  return __query_relation("alias", var_name, alias)

def get_initial(var_name):
  return __query_relation("initial", var_name)

def get_final(var_name):
  return __query_relation("final", var_name)

def get_choice(var_name):
  return __query_relation("choice", var_name)

def get_junction(var_name):
  return __query_relation("junction", var_name)

def get_entry_pseudostate(entry, substate):
  return __query_relation("entry_pseudostate", entry, substate)

def get_exit_pseudostate(exit, superstate):
  return __query_relation("exit_pseudostate", exit, superstate)

def get_substate(superstate, substate):
  return __query_relation("substate", superstate, substate)

def get_region(superstate, region):
  return __query_relation("region", superstate, region)

def get_onentry_action(var_name, action):
  return __query_relation("onentry_action", var_name, action)

def get_onexit_action(var_name, action):
  return __query_relation("onexit_action", var_name, action)

def get_do_action(var_name, proc):
  return __query_relation("do_action", var_name, proc)

def get_transition(source, destination, event, guard, action):
  return __query_relation("transition", source, destination, event, guard, action)

def get_internal_transition(state, event, guard, action):
  return __query_relation("internal_transition", state, event, guard, action)

def get_event(type, argument):
  return __query_relation("event", type, argument)

def get_action(type, argument):
  return __query_relation("action", type, argument)

def get_proc(procedure):
  return __query_relation("proc", procedure)