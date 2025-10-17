# lexer.py

"""
lexer for pysh
"""

import ply.lex as lex


tokens = (
    'COMMAND',
    'ARG',
    'STRING_LITERAL',
    'PIPE',
    'REDIRECT_OUT',
    'REDIRECT_OUT_APPEND',
    'REDIRECT_IN',
    'SEMICOLON',
    'BACKGROUND',
    'LOGICAL_AND',
    'LOGICAL_OR',
    'VARIABLE',
)


def t_LOGICAL_OR(t):
    r'\|\|'
    t.lexer.is_command_position = True  # Next word must be a command
    return t

def t_LOGICAL_AND(t):
    r'&&'
    t.lexer.is_command_position = True  # Next word must be a command
    return t

def t_REDIRECT_OUT_APPEND(t):
    r'>>'
    t.lexer.is_command_position = False # Next word is an arg (filename)
    return t

def t_PIPE(t):
    r'\|'
    t.lexer.is_command_position = True  # Next word must be a command
    return t

def t_REDIRECT_OUT(t):
    r'>'
    t.lexer.is_command_position = False # Next word is an arg (filename)
    return t

def t_REDIRECT_IN(t):
    r'<'
    t.lexer.is_command_position = False # Next word is an arg (filename)
    return t

def t_SEMICOLON(t):
    r';'
    t.lexer.is_command_position = True  # Next word must be a command
    return t

def t_BACKGROUND(t):
    r'&'
    t.lexer.is_command_position = True  # Next word must be a command
    return t

def t_VARIABLE(t):
    r'\$[a-zA-Z_][a-zA-Z0-9_]*'
    t.lexer.is_command_position = False # A variable is an argument
    return t

# A string literal, which is always an argument
def t_STRING_LITERAL(t):
    r'\"[^"]*\"|\'[^\']*\''  # Handles "..." or '...'
    t.value = t.value[1:-1]     # Strip the quotes
    t.lexer.is_command_position = False
    return t

# A rule for comments (discarded)
def t_COMMENT(t):
    r'\#.*'
    pass  # No return value means the token is skipped

# This rule handles both COMMAND and ARG
def t_WORD(t):
    r'[^\s|&;<>#$"\']+'  # Any non-space, non-special char
    
    # This is the same logic you had, but using the lexer's state
    if t.lexer.is_command_position:
        t.type = 'COMMAND'
        t.lexer.is_command_position = False # The *next* word is an ARG
    else:
        t.type = 'ARG'
    return t

# Rule to track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    t.lexer.is_command_position = True  # New line, expect a command

# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'

# Error handling rule
def t_error(t):
    print(f"Illegal character '{t.value[0]}' on line {t.lexer.lineno}")
    t.lexer.skip(1)  # Skip the bad character


lexer = lex.lex()

# We need to initialize our custom state
lexer.is_command_position = True
