from prolog.query import file_load
from puml.puml_parser import parse_plantuml
from puml.puml_generate import generate_plantuml
from prolog.prolog_parser import parse_prolog
from prolog.prolog_generate import generate_prolog

import sys

if len(sys.argv) > 4 or len(sys.argv) < 3:
    sys.stderr.write("Error: Usage: python myscript.py [ -f ] arg1 arg2\n")
    exit(1)

flag = None
arg1 = None
arg2 = None

if sys.argv[1].startswith('-') and len(sys.argv) == 4:
    flag = sys.argv[1]
    input_file = sys.argv[2]
    output_file = sys.argv[3] if len(sys.argv) > 3 else None
elif len(sys.argv) == 3:
    input_file = sys.argv[1]
    output_file = sys.argv[2]
else:
    sys.stderr.write("Error: Usage: python myscript.py [ -f ] arg1 arg2\n")
    exit(1)

# input_file = "./resources/PUML/output.puml"
# output_file = "./resources/db/output.pl"

input_language = input_file.split(".")[-1]
output_language = output_file.split(".")[-1]

if input_language == "pl":
    file_load(input_file) # Load prolog file
    states, transitions = parse_prolog()

elif input_language == "puml":
    states, transitions = parse_plantuml(input_file)

else:
    sys.stderr.write("Not Supported Yet")
    exit(1)

if output_language == "pl":
    sub_code = generate_prolog(states, transitions)

elif output_language == "puml":
    sub_code = generate_plantuml(states, transitions)
    
else:
    sys.stderr.write("Not Supported Yet")
    exit(1)

with open(output_file, 'w') as file:
    file.write(sub_code)
    print(output_file + " has been generated")
