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

def p_statement(p):
    """
    statement : command
    """
    # Create a root 'Statement' node for consistency
    statement_node = Node("Statement")
    statement_node.children.append(p[1])
    p[0] = statement_node

def p_command(p):
    """
    command : COMMAND argument_list
    """
    # p[1] is the Token for the command name (e.g., 'ls')
    # p[2] is the list of argument Nodes from argument_list
    
    # Create the main 'Command' node
    command_node = Node("Command")
    
    # Create the child node for the command name, passing the token to it
    command_name_node = Node("COMMAND_NAME", token=p[1])
    
    # The children of the 'Command' node are the name and the arguments
    command_node.children.append(command_name_node)
    command_node.children.extend(p[2]) # .extend adds all items from the list
    
    p[0] = command_node

def p_argument_list(p):
    """
    argument_list : argument_list argument
    """
    # Recursively build a list of argument nodes
    # p[1] is the list so far, p[2] is the new argument node
    p[0] = p[1] + [p[2]]

def p_argument_list_empty(p):
    """
    argument_list :
    """
    # The base case: an empty list if there are no arguments
    p[0] = []

def p_argument(p):
    """
    argument : ARG
             | STRING_LITERAL
    """
    # p[1] is the Token for either ARG or STRING_LITERAL.
    # We create an 'ARG' node, passing the actual token to it.
    p[0] = Node("ARG", token=p[1])

# --- 4. Error Handling ---
def p_error(p):
    if p:
        raise SyntaxError(f"Syntax error at token {p.type} ('{p.value}')")
    else:
        raise SyntaxError("Syntax error at end of input")


parser = yacc.yacc()
  



