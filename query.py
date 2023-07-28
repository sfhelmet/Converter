from pyswip import Prolog
import os

def main():
  prolog = Prolog()
  prolog.consult("decl.pl")

  def query_relation(relations, X, Y):
    query = f"{relations}({X}, {Y})"
    return list(prolog.query(query))

  print("Superstate:")
  for result in query_relation("superstate", "X", "Y"):
    print(f"{result['X']} is the superstate of {result['Y']}")

if __name__ == "__main__":
  main()
