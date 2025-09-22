#!/usr/bin/env python3
from lexer import Lexer
import parser
import checker
import executor
import os
import atexit
import readline   # history (arrow key navigation)
from pathlib import Path

from commands import help

# ANSI color for light grey
LOG_COLOR = "\033[90m"
RESET_COLOR = "\033[0m"

HISTORY_FILE = Path.home() / ".pysh_history"

class REPL:
    def __init__(self):
        self.parser = parser.Parser()
        self.checker = checker.SemanticChecker()
        self.executor = executor.Executor()
        self.show_logs = False  # Start with logs off
        self.commands = {"bye", "help", "--log", "--nolog", "clear"}

        # Load history file if it exists
        if HISTORY_FILE.exists():
            readline.read_history_file(HISTORY_FILE)

        # Save history automatically when pysh exits
        atexit.register(self._save_history)

    def _save_history(self):
        try:
            readline.write_history_file(HISTORY_FILE)
        except Exception as e:
            print(f"Warning: could not save history: {e}")

    def handle_commands(self, inp : str):
        if inp == "--log":
            self.show_logs = True
            return
        if inp == "--nolog":
            self.show_logs = False
            return
        if inp == "bye":
            print("bye ฅ^>⩊<^ฅ")
            return 0
        if inp == "help":
            help.run()
            return
        if inp == "clear":
            os.system("clear")
            return
        pass        


    def run(self):
        while True:
            try:
                inp = input("pysh$ ").strip()
                if not inp:
                    continue

                # if the input is in the pysh commands / flags
                if inp in self.commands:
                    if self.handle_commands(inp) == 0:
                        break
                    else:
                        continue

                # tokenize input
                tokens = Lexer(inp)
                if self.show_logs:
                    print(f"{LOG_COLOR}Tokens: {tokens}{RESET_COLOR}")
                
                '''
                # Parse tokens
                self.parser.parse(tokens)
                if self.show_logs:
                    print(f"{LOG_COLOR}Parse tree:{RESET_COLOR}")
                    self.parser.tree.display()

                # Semantic check
                try:
                    self.checker.check(self.parser.tree)
                except RuntimeError as e:
                    print(f"Semantic error: {e}")
                    continue

                # Execute the command
                self.executor.execute(self.parser.tree)
                '''
            
            except KeyboardInterrupt:
                print()
            except EOFError:
                print()
                break

def main():
    repl = REPL()
    repl.run()

if __name__ == "__main__":
    main()
