from pyswip import Prolog

# Initialize Prolog
prolog = Prolog()

# Import the knowledge base
prolog.consult("decl.pl")

# Query the Prolog knowledge base
def query_relation(relations, X, Y):
    query = f"{relations}({X}, {Y})"
    return list(prolog.query(query))

print("Grandparents:")
for result in query_relation("grandparent", "X", "Y"):
    print(f"{result['X']} is the grandparent of {result['Y']}")