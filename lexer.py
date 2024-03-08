import ply.lex as lex

# Lexer

tokens = (
    #Newline
    'NEWLINE',
    # Keywords
    'VAR',
    # Identifiers
    'IDENTIFIER',
    'TYPE',
    # Symbols
    'COLON',
    'EQUALS',
    'SEMICOLON',
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

def t_COLON(t):
    r':'
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
    global line_counter
    line_counter += 1
    print(f"line {line_counter}")
    t.lexer.lineno += len(t.value)



t_ignore = ' \t'

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)



lexer = lex.lex(debug=True)

