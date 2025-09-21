import subprocess
from parser import Node, ParseTree
from commands import cd, cpu, disk, ls, mem, mkdir, ps, pwd, rm

# map of built-in command names to their module run() functions
BUILTIN_COMMANDS = {
    "cd": cd.run,
    "cpu": cpu.run,
    "disk": disk.run,
    "ls": ls.run,
    "mem" : mem.run,
    "mkdir": mkdir.run,
    "ps": ps.run,
    "pwd": pwd.run,
    "rm": rm.run,
}

class Executor:
    """
    Executes commands from a parse tree.
    
    Built-in commands are dispatched to their respective module run() functions.
    External commands are executed via subprocess.
    """

    def __init__(self):
        pass

    def execute(self, tree: ParseTree):
        if tree.root is None:
            return
        self._execute_node(tree.root)

    def _execute_node(self, node: Node):
        if node.name == "Command":
            self._execute_command(node)
        else:
            for child in getattr(node, "children", []):
                self._execute_node(child)

    def _execute_command(self, command_node: Node):
        if not command_node.children:
            return

        command_name_node = command_node.children[0]
        command_name = command_name_node.token.value
        args = [child.token.value for child in command_node.children[1:]]

        if command_name in BUILTIN_COMMANDS:
            self._execute_builtin_command(command_name, args)
        else:
            self._execute_external_command(command_name, args)

    def _execute_builtin_command(self, command_name: str, args: list):
        """Dispatch built-in commands to their respective module run() functions."""
        try:
            func = BUILTIN_COMMANDS.get(command_name)
            if func:
                func(args)
            else:
                print(f"Unknown built-in command: {command_name}")
        except Exception as e:
            print(f"Error executing {command_name}: {e}")

    def _execute_external_command(self, command_name: str, args: list):
        """Execute external commands using subprocess."""
        try:
            cmd = [command_name] + args
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=False
            )
            if result.stdout:
                print(result.stdout, end='')
            if result.stderr:
                print(result.stderr, end='')
        except FileNotFoundError:
            print(f"Command not found: {command_name}")
        except Exception as e:
            print(f"Error executing {command_name}: {e}")
