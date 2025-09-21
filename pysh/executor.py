import os
import shutil
import subprocess
from parser import Node, ParseTree

BUILTIN_COMMANDS = {"cd", "pwd", "mkdir", "rm", "ls"}

class Executor:
    """
    Executes commands from a parse tree.
    Built-in commands are dispatched to dedicated methods.
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
        """Dispatch to the appropriate method for built-in commands."""
        try:
            dispatch_table = {
                "cd": self._cd,
                "pwd": self._pwd,
                "mkdir": self._mkdir,
                "rm": self._rm,
                "ls": self._ls
            }

            func = dispatch_table.get(command_name)
            if func:
                func(args)
            else:
                print(f"Unknown built-in command: {command_name}")

        except Exception as e:
            print(f"Error executing {command_name}: {e}")

    # Built-in command implementations
    def _cd(self, args):
        path = args[0] if args else os.path.expanduser("~")
        os.chdir(path)
        print(f"Changed to directory: {os.getcwd()}")

    def _pwd(self, args):
        print(os.getcwd())

    def _mkdir(self, args):
        if not args:
            raise RuntimeError("mkdir: missing operand")
        for dir_path in args:
            os.makedirs(dir_path, exist_ok=True)
        print(f"Created directories: {', '.join(args)}")

    def _rm(self, args):
        if not args:
            raise RuntimeError("rm: missing operand")
        for item in args:
            if os.path.isfile(item):
                os.remove(item)
                print(f"Removed file: {item}")
            elif os.path.isdir(item):
                shutil.rmtree(item)
                print(f"Removed directory: {item}")
            else:
                print(f"rm: cannot remove '{item}': No such file or directory")

    def _ls(self, args):
        show_all = False
        paths = []

        for arg in args:
            if arg.startswith("-"):
                if "a" in arg:
                    show_all = True
            else:
                paths.append(arg)

        if not paths:
            paths = ["."]
        
        items = []
        for path in paths:
            if os.path.isdir(path):
                for f in os.listdir(path):
                    if show_all or f not in (".DS_Store", ".localized"):
                        items.append(os.path.join(path, f) if path != "." else f)
            elif os.path.exists(path):
                items.append(path)
            else:
                print(f"ls: cannot access '{path}': No such file or directory")

        for item in sorted(items):
            print(item)

    def _execute_external_command(self, command_name: str, args: list):
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
