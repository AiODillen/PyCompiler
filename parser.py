# Parser
import ply.yacc as yacc
import lexer
from lexer import line_counter
import ast
import Models.Variable as Var
import Models.Level
import sys

input_string = ""
tokens = lexer.tokens
levels = Models.Level.Level()


statements = []
modules = []
level = 0
curr_line = 0

start = 'statements'

def p_statements(p):
    '''statements : statement SEMICOLON newline statements
                  | statement SEMICOLON newline'''
    p[0] = ast.Module(body=modules, type_ignores=[])


def p_statement_error(p):
    'statement : statement error'
    print(f"Parser error: Unexpected token '{p[1]}' at line {p.lineno}, column {find_column(p.lexer.lexdata, p.slice[1])}")


def p_statement_var(p):
    'statement : VAR IDENTIFIER COLON TYPE EQUALS value'



    if not p[6]:
        return

    print(f"VAR {p[2]} : {p[4]} = {p[6]}")
    crt_var = Var.Variable(p[2], p[4], p[6])
    if levels.check_data_below_current_level(level, crt_var):
        print(f"ERROR: Variable {p[2]} already exists in current scope")
        sys.exit(1)
    else:
        levels.add_data(level, crt_var)
    p[0] = modules.append(ast.parse(f"{p[2]} = {p[6]}").body)



def p_value_int(p):
    '''value : INT'''
    if "int" == p[-2]:
        p[0] = p[1]
    else:
        p[0] = None
        print(f"ERROR: {p[1]} is not {p[-2]}, at line {curr_line} column {find_column(p.lexer.lexdata, p.slice[1])}, skipping statement")

def p_value_float(p):
    '''value : FLOAT'''
    if "float" == p[-2]:
        p[0] = p[1]
    else:
        p[0] = None
        print(f"ERROR: {p[1]} is not {p[-2]}, at line {curr_line} column {find_column(p.lexer.lexdata, p.slice[1])}, skipping statement")


def p_value_string(p):
    '''value : STRING'''
    if "string" == p[-2]:
        p[0] = p[1]
    else:
        p[0] = None
        print(f"ERROR: {p[1]} is not {p[-2]}, at line {curr_line} column {find_column(p.lexer.lexdata, p.slice[1])}, skipping statement")


def p_newline(p):
    '''newline : NEWLINE
               | empty'''
    if p[1]:
        global curr_line
        curr_line += 1

def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}'")
    else:
        print("Syntax error at EOF")
        p[0] = None

def p_empty(p):
    'empty :'
    pass

def find_column(input, token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1



parser = yacc.yacc()

