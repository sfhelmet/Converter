from pyswip import Prolog

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
    print(f"Error: {relations} not found")
    return []
  return results

#query_name
def state(name):
  return __query_relation("state", name) #name -> var_name

def alias(name, alias):
  return __query_relation("alias", name, alias)

def initial(name):
  return __query_relation("initial", name)

def final(name):
  return __query_relation("final", name)

def entry_pseudostate(entry, substate):
  return __query_relation("entry_pseudostate", entry, substate)

def exit_pseudostate(exit, superstate):
  return __query_relation("exit_pseudostate", exit, superstate)

def superstate(superstate, substate):
  return __query_relation("superstate", superstate, substate)

def onentry_action(name, action):
  return __query_relation("onentry_action", name, action)

def onexit_action(name, action):
  return __query_relation("onexit_action", name, action)

def do_action(name, action):
  return __query_relation("do_action", name, action)

def transition(source, destination, event, guard, action):
  return __query_relation("transition", source, destination, event, guard, action)

def internal_transition(state, event, guard, action):
  return __query_relation("internal_transition", state, event, guard, action)

def event(type, argument):
  return __query_relation("event", type, argument)

def action(type, argument):
  return __query_relation("action", type, argument)

def proc(procedure):
  return __query_relation("proc", procedure)