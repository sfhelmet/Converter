from query import *
from puml_generate import generate_plantuml, write_plantuml_code_to_file
from prolog_parser import parse_prolog


file_load("./db/tcs_flattened.pl")

states, transitions = parse_prolog()

uml_code = generate_plantuml(states, transitions)
write_plantuml_code_to_file(uml_code, "./PUML/tcs_flattened.puml")










