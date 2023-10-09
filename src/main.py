from prolog.query import file_load
from puml.puml_parser import parse_plantuml
from puml.puml_generate import generate_plantuml
from prolog.prolog_parser import parse_prolog
from prolog.prolog_generate import generate_prolog

input_file = "./resources/PUML/output.puml"
output_file = "./resources/db/output.pl"

input_language = input_file.split(".")[-1]
output_language = output_file.split(".")[-1]

if input_language == "pl":
    file_load(input_file) # Load prolog file
    states, transitions = parse_prolog()

elif input_language == "puml":
    states, transitions = parse_plantuml(input_file)

else:
     print("Not Supported Yet")


if output_language == "pl":
    sub_code = generate_prolog(states, transitions)

elif output_language == "puml":
    sub_code = generate_plantuml(states, transitions)

else:
    print("Not Supported Yet")

with open(output_file, 'w') as file:
        file.write(sub_code)
