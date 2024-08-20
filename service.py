from query import file_load
from prolog_generate import generate_prolog
from prolog_parser import parse_prolog
from puml_generate import generate_plantuml
from puml_parser import parse_plantuml
from md_generate import generate_mermaid
from md_parser import parse_mermaid
from exceptions import NotSupportedError


def transform(input_language, output_language, code):
    legend = False
    states = None
    transitions = None
    sub_code = None
    ega_dict = None

    if input_language == "Prolog":
        file_load(code) # Load prolog file
        states, transitions, ega_dict = parse_prolog(legend)
    elif input_language == "PlantUML":
        states, transitions = parse_plantuml(code)
    elif input_language == "Mermaid":
        states, transitions = parse_mermaid(code)

    else:
        raise NotSupportedError("Input file type not supported")

    if output_language == "Prolog":
        sub_code = generate_prolog(states, transitions)

    elif output_language == "PlantUML":
        sub_code = generate_plantuml(states, transitions, ega_dict, legend)

    elif output_language == "Mermaid":
        sub_code = generate_mermaid(states, transitions, ega_dict, legend)
        
    else:
        raise NotSupportedError("Output file type not supported")
    
    response = {
        "input_language": input_language,
        "output_language": output_language,
        "code": sub_code,
    }

    return response