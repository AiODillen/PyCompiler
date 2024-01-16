# Parser
import ply.yacc as yacc
import lexer  # Import the lexer
import ast
import sys

tokens = lexer.tokens

statements = []

start = 'statements'

def p_statements(p):
    '''statements : statement SEMICOLON statements
                  | statement SEMICOLON'''
    p[0] = statements
    statements.insert(0, p[1])

def p_statement_var(p):
    'statement : VAR IDENTIFIER COLON TYPE EQUALS value'
    p[0] = ast.parse(f"{p[2]} = {p[6]}")



def p_value(p):
    '''value : INT
             | FLOAT
             | STRING
             | BOOL'''
    p[0] = p[1]

def p_error(p):
    print(f"Syntax error at '{p.value}'")


parser = yacc.yacc()
