# Parser
import ply.yacc as yacc
import lexer
import ast
import textwrap
import Models.Function as Func
from Models.Level import *

input_string = ""
tokens = lexer.tokens
levels = [Level("global")]

statements = []
modules = []
curr_line = 1
errors = []
start = 'start'

def p_start(p):
    '''start : expressions'''
    p[0] = ast.Module(body=modules, type_ignores=[])


def p_expressions(p):
    '''expressions : expression
                | expressions expression'''

def p_expression(p):
    '''expression : function
                | statement'''


def p_function(p):
    'function : FUNC IDENTIFIER COLON TYPE fn_level LPAREN parameters RPAREN LBRACE fn_block RBRACE SEMICOLON'
    print("Parsed a function")
    if levels[0].check_data_below_current_level(p[2]):
        errors.append(f"Error: Function {p[2]} already exists in current scope")
    else:
        statements = "\n    ".join(p[10])
        levels[0].add_data(0, p[2])
        print("--\n"+p[10]+"\n--")
        s = f"""
def {p[2]}({p[7]}) -> {p[4]}:
    {p[10]}
"""
        a = ast.parse(s)

        modules.append(a.body)
    levels.pop()


def p_fn_block(p):
    '''fn_block : fn_block_parse
                | fn_block fn_block_parse'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] + "\n    " + p[2]

def p_fn_block_parse(p):
    '''fn_block_parse : VAR IDENTIFIER COLON TYPE EQUALS value SEMICOLON'''
    if not p[6]:
        return

    print(f"VAR {p[2]} : {p[4]} = {p[6]}")
    if levels[-1].check_data_below_current_level(p[2]):
        errors.append(f"Error: Variable {p[2]} already exists in current scope")
        p[0] = None
        return
    else:
        levels[-1].add_data(levels[-1].level, p[2])
        p[0] = f"{p[2]} = {p[6]}"

def p_fn_level(p):
    'fn_level :'
    levels.append(Level(p[-4]))
    p[0] = None

def p_parameter(p):
    '''parameter : IDENTIFIER COLON TYPE'''
    p[0] = p[1] + " : " + p[3]
def p_parameters(p):
    '''parameters : parameter
                  | parameter COMMA parameters'''
    print("starting params")
    if levels[-1].check_data_below_current_level(p[1]):
        errors.append(f"Error: Parameter {p[1]} already exists in current function. At line {curr_line} column {find_column(p.lexer.lexdata, p.slice[1])}")
        return
    levels[-1].add_data(levels[-1].level, p[1])
    if len(p) == 2:
        print("parameters : IDENTIFIER COLON TYPE")
        p[0] = p[1]
    else:
        print("parameters : IDENTIFIER COLON TYPE COMMA parameters")
        p[0] = p[1] + ", " + p[3]


def p_expression_var(p):
    'statement : VAR IDENTIFIER COLON TYPE EQUALS value SEMICOLON'
    if not p[6]:
        return

    print(f"VAR {p[2]} : {p[4]} = {p[6]}")
    if levels[-1].check_data_below_current_level(p[2]):
        errors.append(f"Error: Variable {p[2]} already exists in current scope")
        return
    else:
        levels[-1].add_data(levels[-1].level, p[2])
        modules.append(ast.parse(f"{p[2]} = {p[6]}").body)

def p_statement_error(p):
    'statement : error'
    p[0] = None

def p_value_int(p):
    '''value : INT'''
    if "int" == p[-2]:
        p[0] = p[1]
    else:
        p[0] = None
        errors.append(f"Error: {p[1]} is not {p[-2]}, at line {curr_line} column {find_column(p.lexer.lexdata, p.slice[1])}, skipping statement")

def p_value_float(p):
    '''value : FLOAT'''
    if "float" == p[-2]:
        p[0] = p[1]
    else:
        p[0] = None
        errors.append(f"Error: {p[1]} is not {p[-2]}, at line {curr_line} column {find_column(p.lexer.lexdata, p.slice[1])}, skipping statement")

def p_value_string(p):
    '''value : STRING'''
    if "string" == p[-2]:
        p[0] = p[1]
    else:
        p[0] = None
        errors.append(f"Error: {p[1]} is not {p[-2]}, at line {curr_line} column {find_column(p.lexer.lexdata, p.slice[1])}, skipping statement")


def p_error(p):
    if p:
        errors.append(f"Syntax error at '{p.value}. At line {curr_line} column {find_column(p.lexer.lexdata, p)}")
    else:
        errors.append("Syntax error at EOF")


def p_empty(p):
    'empty :'
    pass

def find_column(input, token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1

parser = yacc.yacc(debug=True)

