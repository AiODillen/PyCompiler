import ply.lex as lex

# Lexer

tokens = (
    #Newline
    'NEWLINE',
    # Keywords
    'VAR',
    'FUNC',
    # Identifiers
    'IDENTIFIER',
    'TYPE',
    # Symbols
    'COLON',
    'EQUALS',
    'SEMICOLON',
    'RPAREN',
    'LPAREN',
    'RBRACKET',
    'LBRACKET',
    'RBRACE',
    'LBRACE',
    'COMMA',
    # Types
    'INT',
    'FLOAT',
    'STRING',
    'BOOL',
    'LIST',
    'DICT',
    # Functions
    'PRINT',


)

def t_SEMICOLON(t):
    r';'
    return t

def t_VAR(t):
    r'var'
    return t

def t_FUNC(t):
    r'func'
    return t

def t_LPAREN(t):
    r'\('
    return t

def t_RPAREN(t):
    r'\)'
    return t

def t_LBRACKET(t):
    r'\['
    return t

def t_RBRACKET(t):
    r'\]'
    return t

def t_LBRACE(t):
    r'\{'
    return t

def t_RBRACE(t):
    r'\}'
    return t

def t_COLON(t):
    r':'
    return t

def t_COMMA(t):
    r','
    return t

def t_EQUALS(t):
    r'='
    return t


def t_TYPE(t):
    r'int|float|string|bool|list|dict'
    return t

def t_FLOAT(t):
    r'-?\d+\.\d+'
    return t


def t_INT(t):
    r'-?\d+'
    return t

def t_STRING(t):
    r'"[^"]*"'
    return t

def t_BOOL(t):
    r'True|False'
    return t

def t_LIST(t):
    r'\[[^\]]*\]'
    return t

def t_DICT(t):
    r'\{[^}]*\}'
    return t

def t_PRINT(t):
    r'print'
    return t

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t


line_counter = 1
# Define a rule so we can track line numbers
def t_NEWLINE(t):
    r'\n+'
    from parser import curr_line
    curr_line += 1


t_ignore = ' \t\n'

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)



lexer = lex.lex()

