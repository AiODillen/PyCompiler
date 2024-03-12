# Parser
import ply.yacc as yacc
from lexer import tokens
import ast
from Models.Level import *

tokens = tokens
levels = [Level("global")]

statements = []
modules = []
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
                | statement
                | operation
                | print'''
def p_function(p):
    'function : FUNC IDENTIFIER COLON TYPE fn_level LPAREN parameters RPAREN LBRACE fn_block return RBRACE SEMICOLON'
    print("Parsed a function")
    print(p[10], p[11])
    if levels[0].check_data_below_current_level(p[2]):
        errors.append(f"Error: Function {p[2]} already exists in current scope")
    else:
        levels[0].add_data(0, p[2])
        if p[10] and p[11]:
            s = f"""
def {p[2]}({p[7]}) -> {p[4]}:
    {p[10]}
    {p[11]}
"""
        elif not p[10] and p[11]:
            s = f"""
def {p[2]}({p[7]}) -> {p[4]}:
    {p[11]}
"""
        elif p[10] and not p[11]:
            s = f"""
def {p[2]}({p[7]}) -> {p[4]}:
    {p[10]}
"""
        print(s)
        a = ast.parse(s)
        modules.append(a.body)
    levels.pop()

def p_return(p):
    '''return : RETURN IDENTIFIER SEMICOLON
            | empty'''
    print("Parsed a return")
    if not p[1]:
        p[0] = None
        return
    if not levels[-1].check_data_below_current_level(p[2]):
        errors.append(f"Error: {p[2]} is not defined in current scope")
    else:
        if levels[-1].get_data(p[2]).get_type() != p[-7]:
            errors.append(f"Error: {p[2]} is not of type {p[-7]}")
        else:
            p[0] = f"return {levels[-1].get_data(p[2]).get_name()}"
def p_fn_block(p):
    '''fn_block : fn_block_parse
                | fn_block fn_block_parse
                | empty'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        print(len(levels) + 1)
        p[0] = p[1] + "\n" + "    "*(len(levels)) + p[2]
def p_fn_block_parse(p):
    '''fn_block_parse : VAR IDENTIFIER COLON TYPE EQUALS value SEMICOLON
                    | IF LPAREN boolean RPAREN LBRACE level_up fn_block RBRACE SEMICOLON'''
    if p[1] == "var":
        value_type = p[6].split(";")[0]
        value = p[6].split(";")[1]
        print("data got: ", value_type, value)
        if value_type != p[4]:
            errors.append(f"Error: {value} is not of type {p[4]}")
            return

        print(f"VAR {p[2]} : {p[4]} = {p[6]}")
        if levels[-1].check_data_below_current_level(p[2]):
            errors.append(f"Error: Variable {p[2]} already exists in current scope")
            p[0] = None
            return
        else:
            levels[-1].add_data(levels[-1].level, Var.Variable(p[2], p[4], p[6]))
            if value_type == "str":
                p[0] = f"{p[2]} = \"{value}\""
            else:
                p[0] = f"{p[2]} = {value}"
    elif p[1] == "if":
        print("Parsed an if")
        print(len(levels))
        indentation = "    " * (len(levels) - 2)
        print(p[7])
        s = f"""
{indentation}if {p[3]}:
{indentation}    {p[7]}
"""
        print(s)
        levels.pop()
        p[0] = s
def p_fn_level(p):
    'fn_level :'
    levels.append(Level(p[-3]))
    p[0] = None

def p_level_up(p):
    'level_up :'
    levels.append(Level(""))

def p_boolean(p):
    '''boolean : value_atom
                | value_atom relation value_atom'''
    if len(p) == 2:
        if p[1].split(";")[0] == "bool":
            p[0] = str(eval(p[1].split(";")[1]))
        else:
            errors.append(f"Error: {p[1]} is not of type bool")
    else:
        print("parsing a relation")
        if p[1].split(';')[0] != p[3].split(';')[0]:
            errors.append(f"Error: {p[1]} and {p[3]} are not of the same type")
            p[0] = None
        else:
            print(f"{p[1].split(';')[1]} {p[2]} {p[3].split(';')[1]}")
            p[0] = str(eval(f"{p[1].split(';')[1]} {p[2]} {p[3].split(';')[1]}"))

def p_relation(p):
    '''relation : IE
                | NE
                | LT
                | GT
                | LE
                | GE'''
    p[0] = p[1]
def p_parameter(p):
    '''parameter : IDENTIFIER COLON TYPE'''
    print(f"parameter {p[1]} : {p[3]}")
    p[0] = p[1] + ":" + p[3]

def p_parameters(p):
    '''parameters : parameter
                  | parameter COMMA parameters'''
    print("starting params")
    if levels[-1].check_data_below_current_level(p[1]):
        from lexer import curr_line
        errors.append(f"Error: Parameter {p[1]} already exists in current function. At line {curr_line} column {find_column(p.lexer.lexdata, p.slice[1])}")
        return
    print(p[1])
    levels[-1].add_data(levels[-1].level, Var.Variable(p[1].split(":")[0], p[1].split(":")[1], None))
    if len(p) == 2:
        p[0] = p[1]
    else:
        if not p[3]:
            p[0] = p[1]
        else:
            p[0] = p[1] + ", " + p[3]

def p_assign_var(p):
    'statement : VAR IDENTIFIER COLON TYPE EQUALS value SEMICOLON'
    print(p[6])
    value_type = p[6].split(";")[0]
    value = p[6].split(";")[1]
    print("data got: ", value_type, value)
    if value_type != p[4]:
        errors.append(f"Error: {value} is not of type {p[4]}")
        return

    print(f"VAR {p[2]} : {p[4]} = {value}")
    if levels[-1].check_data_below_current_level(p[2]):
        errors.append(f"Error: Variable {p[2]} already exists in current scope")
        return
    else:
        levels[-1].add_data(levels[-1].level, Var.Variable(p[2], p[4], value))
        if value_type == "str":
            modules.append(ast.parse(f"{p[2]} = \"{value}\"").body)
        else:
            modules.append(ast.parse(f"{p[2]} = {value}").body)

def p_assign_var_error(p):
    'statement : VAR IDENTIFIER COLON TYPE EQUALS value error'

def p_value(p):
    '''value : operation
          | value_atom
          | IDENTIFIER'''
    p[0] = p[1]
def p_print(p):
    '''print : PRINT LPAREN value RPAREN SEMICOLON'''
    print(p[3])
    print("printing value")
    if ";" in p[3]:
        modules.append(ast.parse(f"print(str({p[3].split(';')[1]}))").body)
    modules.append(ast.parse(f"print(str({p[3]}))").body)
def p_atom_int(p):
    '''value_atom : INT'''
    p[0] = "int;" + p[1]
def p_atom_float(p):
    '''value_atom : FLOAT'''
    p[0] = "float;" + p[1]

def p_atom_bool(p):
    '''value_atom : BOOL'''
    p[0] = "bool;" + p[1]

def p_atom_dict(p):
    '''value_atom : DICT'''
    p[0] = "dict;" + p[1]
def p_atom_str(p):
    '''value_atom : STR'''
    p[0] = "str;" + p[1]
def p_atom_list(p):
    '''value_atom : LIST'''
    p[0] = "list;" + p[1]
def p_operation(p):
    '''operation : binop'''
    p[0] = p[1]
def p_binop(p):
    '''binop : value_atom operator value_atom'''
    left_type = p[1].split(";")[0]
    left_value = p[1].split(";")[1]
    right_type = p[3].split(";")[0]
    right_value = p[3].split(";")[1]
    if left_type != right_type:
        p[0] = None
        from lexer import curr_line
        errors.append(f"Error: {left_type} and {right_type} are not compatible, at line {curr_line} column {find_column(p.lexer.lexdata, p.slice[1])}, skipping statement")
    else:
        p[0] = f"{left_type};" + str(eval(f"{left_value} {p[2]} {right_value}"))

def p_operator(p):
    '''operator : PLUS
    | MINUS
    | TIMES
    | DIVIDE'''
    p[0] = p[1]
def p_error(p):
    if p:
        from lexer import curr_line
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

