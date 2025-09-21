"""
parser for pysh shell
called from repl.py, the parse function accepts a list of token objects and generates a parse tree.
"""

from lexer import Token

class Node:
    """a node that can have multiple children"""
    def __init__(self, name, token=None):
        self.name = name        # Name of the grammar variable or token type
        self.token = token      # Token object (for terminals)
        self.children = []      # List of child nodes

    def __repr__(self):
        if self.token:
            return f"{self.name}({self.token.value})"
        return f"{self.name}"

class ParseTree:
    GRAY = "\033[90m"
    RESET = "\033[0m"

    def display(self, node=None, prefix="", is_last=True):
        """
        Display the parse tree in a visually structured top-down tree format.
        Supports multiple children per node.
        """
        if node is None:
            node = self.root
        if node is None:
            return

        # Print the current node
        connector = "└── " if is_last else "├── "
        print(f"{self.GRAY}{prefix}{connector}{str(node)}{self.RESET}")

        # Prepare the prefix for children
        if hasattr(node, "children") and node.children:
            new_prefix = prefix + ("    " if is_last else "│   ")
            for i, child in enumerate(node.children):
                self.display(child, new_prefix, i == len(node.children) - 1)    


class Parser:
    """recursive-descent parser for pysh"""
    def __init__(self):
        self.tree = ParseTree()
        self.tokens = []
        self.pos = 0

    def parse(self, tokens):
        """Parse tokens and build the parse tree"""
        self.tokens = tokens
        self.pos = 0
        self.tree.root = self.parse_statement()
        if self.pos < len(self.tokens):
            raise SyntaxError(f"Unexpected token: {self.tokens[self.pos]}")
        return self.tree

    def parse_statement(self):
        """Statement -> Command"""
        command_node = self.parse_command()
        statement_node = Node("Statement")
        statement_node.children.append(command_node)
        return statement_node

    def parse_command(self):
        """Command -> COMMAND_NAME (ARG)*"""
        if self.pos >= len(self.tokens):
            raise SyntaxError("Expected COMMAND token")
        if self.tokens[self.pos].type != "COMMAND":
            raise SyntaxError(f"Expected COMMAND token, got {self.tokens[self.pos].type}")

        # Create Command node (non-terminal)
        command_node = Node("Command")

        # Add COMMAND_NAME as a child
        command_name_token = self.tokens[self.pos]
        command_node.children.append(Node("COMMAND_NAME", command_name_token))
        self.pos += 1

        # Add all ARG or STRING_LITERAL tokens as children
        while self.pos < len(self.tokens) and self.tokens[self.pos].type in ("ARG", "STRING_LITERAL"):
            arg_token = self.tokens[self.pos]
            command_node.children.append(Node("ARG", arg_token))
            self.pos += 1

        return command_node
