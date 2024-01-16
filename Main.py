from parser import parser
from lexer import lexer
import ast
import subprocess


# Read the Input.pp file
with open('Input.pp', 'r') as file:
    input_str = file.read()



lexer.input(input_str)


# Tokenize the input
while True:
    tok = lexer.token()
    if not tok:
        break
    print(tok)

result = parser.parse(input_str)

# Compile AST to bytecode
filename = 'output.py'
with open(filename, 'w') as file:
    file.write(ast.unparse(result))

# Convert Python script to exe with PyInstaller
subprocess.run(['pyinstaller', '--onefile', filename])
