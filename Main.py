from parser import parser, MyAst
from lexer import lexer as lex
import ast
import subprocess


# Read the Input.pp file
with open('Input.pp', 'r') as file:
    input_str = file.read()



lexer = lex.input(input_str)


# Tokenize the input
while True:
    tok = lex.token()
    if not tok:
        break
    print(tok)

result = parser.parse(input_str, lexer=lexer)
print(MyAst.dump(result, indent=4))
# Compile AST to bytecode
filename = 'output.py'
with open(filename, 'w') as file:
    file.write(MyAst.unparse(result))

# Convert Python script to exe with PyInstaller
subprocess.run(['pyinstaller', '--onefile', filename])
