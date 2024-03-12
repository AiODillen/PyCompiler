import ply.lex as lex


# Lexer

tokens = (
    #Newline
    'newline',
    # Keywords
    'VAR',
    'FUNC',
    'RETURN',
    'IF',
    # Identifiers
    'IDENTIFIER',
    'TYPE',
    # Symbols
    'COLON',
    'EQUALS',
    'SEMICOLON',
    'RPAREN',
    'LPAREN',
    'RBRACE',
    'LBRACE',
    'COMMA',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'IE',
    'NE',
    'LT',
    'GT',
    'LE',
    'GE',
    # Types
    'INT',
    'FLOAT',
    'STR',
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

def t_NE(t):
    r'!='
    return t

def t_IE(t):
    r'=='
    return t
def t_LE(t):
    r'<='
    return t

def t_GE(t):
    r'>='
    return t

def t_LT(t):
    r'<'
    return t

def t_GT(t):
    r'>'
    return t

def t_IF(t):
    r'if'
    return t

def t_FUNC(t):
    r'func'
    return t

def t_RETURN(t):
    r'return'
    return t
def t_LPAREN(t):
    r'\('
    return t

def t_PLUS(t):
    r'\+'
    return t

def t_MINUS(t):
    r'-'
    return t

def t_TIMES(t):
    r'\*'
    return t

def t_DIVIDE(t):
    r'/'
    return t


def t_RPAREN(t):
    r'\)'
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
    r'int|float|str|bool|list|dict'
    return t

def t_FLOAT(t):
    r'-?\d+\.\d+'
    return t


def t_INT(t):
    r'-?\d+'
    return t

def t_STR(t):
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

curr_line = 0
# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    global curr_line
    curr_line += 1


t_ignore = ' \t'

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)



lexer = lex.lex()

