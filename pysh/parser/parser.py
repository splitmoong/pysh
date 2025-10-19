# parser.py
'''
the yacc file for pysh
'''

import ply.yacc as yacc

#tuple of tokens
from lexer.lexer import tokens
#the node class
from parser.node import Node


'''
write the grammar rules here
'''

# precedence and associativity helps resolve shift/reduce for operators
precedence = (
    ('left', 'SEMICOLON'),
    ('left', 'LOGICAL_OR'),
    ('left', 'LOGICAL_AND'),
    ('left', 'PIPE'),
    ('right', 'BACKGROUND'),
)

def p_statement(p):
    """
    statement : sequence
    """
    statement_node = Node("Statement")
    statement_node.children.append(p[1])
    p[0] = statement_node

# Sequence separated by ';' (left-associative)
def p_sequence_single(p):
    "sequence : conditional"
    p[0] = p[1]

def p_sequence_many(p):
    "sequence : sequence SEMICOLON conditional"
    node = Node("SEQUENCE")
    node.children.append(p[1])
    node.children.append(p[3])
    p[0] = node

# Conditional operators && and || (left-associative)
def p_conditional_single(p):
    "conditional : pipeline"
    p[0] = p[1]

def p_conditional_and(p):
    "conditional : conditional LOGICAL_AND pipeline"
    node = Node("AND")
    node.children.append(p[1])
    node.children.append(p[3])
    p[0] = node

def p_conditional_or(p):
    "conditional : conditional LOGICAL_OR pipeline"
    node = Node("OR")
    node.children.append(p[1])
    node.children.append(p[3])
    p[0] = node

# Pipeline handling (a | b | c) -> PIPELINE node with ordered children
def p_pipeline_single(p):
    "pipeline : simple_command"
    p[0] = p[1]

def p_pipeline_many(p):
    "pipeline : pipeline PIPE simple_command"
    # If left is already a PIPELINE, append; otherwise create new PIPELINE.
    if p[1].name == "PIPELINE":
        p[1].children.append(p[3])
        p[0] = p[1]
    else:
        node = Node("PIPELINE")
        node.children.append(p[1])
        node.children.append(p[3])
        p[0] = node

# Simple command: COMMAND with arguments; optional trailing BACKGROUND (&)
def p_simple_command(p):
    "simple_command : COMMAND argument_list"
    cmd = Node("Command")
    cmd_name = Node("COMMAND_NAME", token=p[1])
    cmd.children.append(cmd_name)
    # argument_list is a Python list of Node("ARG", token=...)
    cmd.children.extend(p[2])
    p[0] = cmd

def p_simple_command_bg(p):
    "simple_command : COMMAND argument_list BACKGROUND"
    cmd = Node("Command")
    cmd_name = Node("COMMAND_NAME", token=p[1])
    cmd.children.append(cmd_name)
    cmd.children.extend(p[2])
    bg = Node("BACKGROUND")
    bg.children.append(cmd)
    p[0] = bg

# --- Argument list rules (unchanged logic) ---
def p_argument_list(p):
    """
    argument_list : argument_list argument
    """
    p[0] = p[1] + [p[2]]

def p_argument_list_empty(p):
    """
    argument_list :
    """
    p[0] = []

def p_argument(p):
    """
    argument : ARG
             | STRING_LITERAL
    """
    p[0] = Node("ARG", token=p[1])

# --- Error Handling ---
def p_error(p):
    if p:
        raise SyntaxError(f"Syntax error at token {p.type} ('{p.value}')")
    else:
        raise SyntaxError("Syntax error at end of input")


parser = yacc.yacc()




