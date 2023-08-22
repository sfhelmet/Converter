from enum import Enum

from puml_parser import parse_plantuml_file
from prolog_generate import generate_prolog, write_prolog_code_to_file

states, transitions = parse_plantuml_file("./PUML/TCS.puml")
prolog_code = generate_prolog(states, transitions)
write_prolog_code_to_file(prolog_code=prolog_code, output_file="./db/output.pl")