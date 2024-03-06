# Parser
import ply.yacc as yacc
import lexer  # Import the lexer
import ast
import Models.Variable as Var
import Models.Level
import sys

tokens = lexer.tokens
levels = Models.Level.Level()

statements = []
modules = []
level = 0

start = 'statements'

def p_statements(p):
    '''statements : statement SEMICOLON statements
                  | statement SEMICOLON'''
    p[0] = ast.Module(body=modules, type_ignores=[])

def p_statement_var(p):
    'statement : VAR IDENTIFIER COLON TYPE EQUALS value'
    print(f"VAR {p[2]} : {p[4]} = {p[6]}")
    crt_var = Var.Variable(p[2], p[4], p[6])
    if levels.check_data_below_current_level(level, crt_var):
        print(f"ERROR: Variable {p[2]} already exists in current scope")
        sys.exit(1)
    else:
        levels.add_data(level, crt_var)
    p[0] = modules.append(ast.parse(f"{p[2]} = {p[6]}").body)


def p_value(p):
    '''value : INT
             | FLOAT
             | STRING
             | BOOL'''
    p[0] = p[1]

def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}'")
    else:
        print("Syntax error at EOF")


parser = yacc.yacc()
