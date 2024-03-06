from parser import parser
from lexer import lexer as lex
import marshal
import py_compile
import time
import ast


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

result: ast.AST = parser.parse(input_str, lexer=lexer)
print(ast.dump(result, indent=4))


with open('out.py', 'w') as f:
    f.write(ast.unparse(result))

with open('out.pyc', 'wb') as fc:
    bytecode = compile(ast.unparse(result), '', 'exec')
    fc.write(marshal.dumps(bytecode))

