#parser/node.py

'''
A node class for building the parse tree.

|---------------|
| name          |
| token         |
| children = [] |
|---------------|
'''

class Node:
    
    def __init__(self, name, token=None):
        self.name = name        # Name of grammar variable / token type
        self.token = token      # Token object (for terminals)
        self.children = []      # List of child nodes

    def __repr__(self):
        if self.token is not None:
            # Support both token objects (with .value) and raw strings
            val = getattr(self.token, "value", self.token)
            return f"{self.name}({val})"
        return f"{self.name}"