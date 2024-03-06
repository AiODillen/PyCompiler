import ply.lex as lex

# Lexer

tokens = (
    'VAR',
    'IDENTIFIER',
    'COLON',
    'TYPE',
    'EQUALS',
    'INT',
    'FLOAT',
    'STRING',
    'BOOL',
    'SEMICOLON',
    'PRINT',
)

def t_SEMICOLON(t):
    r';'
    return t
def t_VAR(t):
    r'var'
    return t

def t_COLON(t):
    r':'
    return t


def t_TYPE(t):
    r'int|float|string|bool'
    return t

def t_EQUALS(t):
    r'='
    return t

def t_INT(t):
    r'\d+'
    return t

def t_FLOAT(t):
    r'\d+\.\d+'
    return t

def t_STRING(t):
    r'"[^"]*"'
    return t

def t_BOOL(t):
    r'True|False|true|false'
    return t

def t_PRINT(t):
    r'print'
    return t

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t




t_ignore = ' \t\n'

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)



lexer = lex.lex()
