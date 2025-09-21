"""
parser for pysh shell

called from repl.py, the parse function accepts a list of token objects and generates a parse tree for the same.
"""
#a token object class
from lexer import Token

class Node:
    def __init__(self, token : Token):
        self.token = token
        self.left = None
        self.right = None
        
''' Grammar for pysh

    Statement -> Command

    Command -> COMMAND_NAME (ARG)*

'''
        
class ParseTree:
    def __init__(self):
        self.root = None
        pass
    
'''a recursive descent parser to build the parse tree'''
class Parser:
    def __init__(self):
        self.tree = ParseTree()
        pass
    
    
    
    pass