'''
When encounter comments, copy and paste the comments to the output file, then go next line.

'''

# read_data = ""
# with open('decl.pl', encoding="utf-8") as f:
#     read_data = f.read()


# for statement in read_data.split("\n"):
#     if statement != "":
#         print(statement)

from parse import parse_prolog_file, generate_plantuml, write_plantuml_code_to_file

prolog_file = "decl.pl"
plantUML_file = "plantUML.puml"
states, transitions = parse_prolog_file(prolog_file)
plantuml_code = generate_plantuml(states, transitions)
write_plantuml_code_to_file(plantuml_code, plantUML_file)

print(plantuml_code)




