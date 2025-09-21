"""
semantic checker for pysh shell

checks the meaning of commands and arguments after parsing.
raises errors for invalid commands, missing files/directories, or invalid environment variables.
"""

import os
import shutil
from parser import Node, ParseTree

# Define built-in commands for mandatory requirements
BUILTIN_COMMANDS = {"cd", "cpu", "ls", "mkdir", "pwd", "rm"}

class SemanticChecker:
    def __init__(self):
        pass

    def check(self, tree: ParseTree):
        """
        Entry point for semantic analysis.
        Traverses the parse tree and checks each node.
        """
        if tree.root is None:
            raise RuntimeError("Empty parse tree")
        self.check_node(tree.root)

    def check_node(self, node: Node):
        """
        Recursively check a node and its children.
        """
        if node.name == "Command":
            self.check_command(node)
        else:
            # Recurse through children
            for child in node.children:
                self.check_node(child)

    def check_command(self, command_node: Node):
        """
        Check the command node:
        - Validate COMMAND_NAME
        - Validate ARGs for built-ins
        """
        if not command_node.children:
            raise RuntimeError("Empty Command node")

        # First child is COMMAND_NAME
        cmd_name_node = command_node.children[0]
        cmd_name = cmd_name_node.token.value

        # Check if command exists
        if not self.command_exists(cmd_name):
            raise RuntimeError(f"Command not found: {cmd_name}")

        # Check arguments for built-ins
        for arg_node in command_node.children[1:]:
            arg_value = arg_node.token.value
            self.check_argument(cmd_name, arg_value)

    def command_exists(self, cmd_name: str) -> bool:
        """
        Check if command is built-in or available in system PATH.
        """
        if cmd_name in BUILTIN_COMMANDS:
            return True
        return shutil.which(cmd_name) is not None

    def check_argument(self, cmd_name: str, arg_value: str):
        """
        Validate arguments depending on the command.
        """
        if cmd_name == "cd":
            if not os.path.isdir(arg_value):
                raise RuntimeError(f"Directory does not exist: {arg_value}")
        elif cmd_name == "rm":
            if not os.path.exists(arg_value):
                raise RuntimeError(f"File does not exist: {arg_value}")
        elif cmd_name == "mkdir":
            # Optional: check if directory already exists
            pass
        # For other commands like ls, pwd, accept args as-is
        # Variables ($VAR) can be handled here if you implement expansion
