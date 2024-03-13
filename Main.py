import subprocess

from parser import parser, errors
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

    # Read the Input.dillen file
    with open('Input.dillen', 'r') as file:
        input_str = file.read()

    lexer = lex.input(input_str)
    x = lex.lineno


    # Tokenize the input
    while True:
        tok = lex.token()
        if not tok:
            break
        print(tok)

    parser.input_string = input_str
    result: ast.AST = parser.parse(input=input_str, lexer=lex)



    # Print the errors
    if len(errors) > 0:
        print("\nErrors:")
        print("---------")
        for error in errors:
            print(error)
        print("---------")


    if result is None:
        exit("Ast is none")
    print(ast.dump(result, indent=4))


    # Write the AST to the file
    with open(file_path, 'w') as f:
        f.write(ast.unparse(result))

    subprocess.run(['python', '-m', 'compileall', folder_name])
