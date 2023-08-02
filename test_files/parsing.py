from test_files.parse import parse_prolog_file, generate_plantuml, write_plantuml_code_to_file

prolog_file = "decl.pl"
plantUML_file = "plantUML.puml"
states, transitions = parse_prolog_file(prolog_file)
plantuml_code = generate_plantuml(states, transitions)
write_plantuml_code_to_file(plantuml_code, plantUML_file)

print(plantuml_code)




