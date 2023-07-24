'''
When encounter comments, copy and paste the comments to the output file, then go next line.

'''

read_data = ""
with open('decl.pl', encoding="utf-8") as f:
    read_data = f.read()


for statement in read_data.split("\n"):
    if statement != "":
        print(statement)
        



