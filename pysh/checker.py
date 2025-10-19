"""
semantic checker for pysh
"""

import os
import shutil
from parser.node import Node

# define built-in commands for mandatory requirements
BUILTIN_COMMANDS = {"cd", "cpu", "disk", "ls", "mem", "mkdir", "pwd", "rm"}


class SemanticChecker:
    def __init__(self):
        pass

    def check(self, root: Node):
        """
        Entry point for semantic analysis.
        Accepts the AST root node (usually the Statement node) and traverses it.
        """
        if root is None:
            raise RuntimeError("Empty parse tree")
        self._check(root)

    def _check(self, node: Node):
        """
        Recursively check a node and its children.
        """
        if node.name == "Command":
            self.check_command(node)
        else:
            # Recurse through children
            for child in getattr(node, "children", []):
                self._check(child)

    def check_command(self, command_node: Node):
        """
        Check the command node:
        - Validate COMMAND_NAME
        - Validate ARGs for built-ins
        """
        if not getattr(command_node, "children", None):
            raise RuntimeError("Empty Command node")

        # First child is COMMAND_NAME
        cmd_name_node = command_node.children[0]
        cmd_name = getattr(cmd_name_node.token, "value", cmd_name_node.token)

        # Check if command exists
        if not self.command_exists(cmd_name):
            raise RuntimeError(f"Command not found: {cmd_name}")

        # Check arguments for built-ins
        for arg_node in command_node.children[1:]:
            arg_value = getattr(arg_node.token, "value", arg_node.token)
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
