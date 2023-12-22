from prolog.query import file_load
from puml.puml_parser import parse_plantuml
from puml.puml_generate import generate_plantuml
from prolog.prolog_parser import parse_prolog
from prolog.prolog_generate import generate_prolog
from exceptions import InvalidUsageError, NotSupportedError

from logger_config import logging
import sys

def main():
    if len(sys.argv) > 4 or len(sys.argv) < 3:
        raise InvalidUsageError("\nUsage: python main.py [ -f ] arg1 arg2")

    flags = None
    input_file = None # "./resources/PUML/output.puml"
    output_file = None # "./resources/db/output.pl"

    if sys.argv[1].startswith('-') and len(sys.argv) == 4:
        flags = sys.argv[1]
        input_file = sys.argv[2]
        output_file = sys.argv[3]
    elif len(sys.argv) == 3:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
    else:
        raise InvalidUsageError("\nUsage: python main.py [ -f ] arg1 arg2")

    input_language = input_file.split(".")[-1]
    output_language = output_file.split(".")[-1]

    states = None
    transitions = None
    sub_code = None

    if input_language == "pl":
        file_load(input_file) # Load prolog file
        states, transitions = parse_prolog()

    elif input_language == "puml":
        states, transitions = parse_plantuml(input_file)

    else:
        raise NotSupportedError("Input file type not supported")

    if output_language == "pl":
        sub_code = generate_prolog(states, transitions)

    elif output_language == "puml":
        sub_code = generate_plantuml(states, transitions)
        
    else:
        raise NotSupportedError("Output file type not supported")

    with open(output_file, 'w') as file:
        file.write(sub_code)
        logging.info(output_file + " has been generated")

if __name__ == "__main__":
    main()