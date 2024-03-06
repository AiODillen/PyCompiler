import subprocess

from parser import parser
from lexer import lexer as lex
import marshal
import ast
import os



if __name__ == '__main__':
    # Specify the folder name and file name
    folder_name = 'out'
    file_name = 'out.py'

    # Create the folder if it doesn't exist
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # Specify the file path within the folder
    file_path = os.path.join(folder_name, file_name)

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

    with open(file_path, 'w') as f:
        f.write(ast.unparse(result))

    subprocess.run(['python', '-m', 'compileall', folder_name])
