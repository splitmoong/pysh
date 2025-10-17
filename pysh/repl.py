#!/usr/bin/env python3
import sys
import os
import atexit
import readline
from pathlib import Path

# ensure project root is in sys.path
sys.path.append(str(Path(__file__).resolve().parent))

#import lex file and the wrapper class
from lexer.lexer import lexer as lexer
from lexer.logginglexer import LoggingLexer

#import yacc file
from parser.parser import parser as parser
from parser.display import display_parse_tree

from checker import SemanticChecker
from executor import Executor


from ai.ai import AI
import ai.managekeys

# ANSI color for light grey
LOG_COLOR = "\033[90m"
RESET_COLOR = "\033[0m"

HISTORY_FILE = Path.home() / ".pysh_history"

class REPL:
    def __init__(self):
        
        self.lexer = LoggingLexer(lexer)
        self.parser = parser
        # instantiate checker and executor that accept AST root nodes
        
        self.checker = SemanticChecker()
        self.executor = Executor()

        # log flag
        self.show_logs = False

        #creating the .pysh_history file if doesnt exist
        if HISTORY_FILE.exists():
            readline.read_history_file(HISTORY_FILE)
        atexit.register(self._save_history)

    def _save_history(self):
        try:
            readline.write_history_file(HISTORY_FILE)
        except Exception as e:
            print(f"Warning: could not save history: {e}")

    def process_command(self, cmd: str):
        try:
            self.lexer.is_command_position = True
            self.lexer.lineno = 1
            self.lexer.input(cmd)
            ast_root = self.parser.parse(lexer=self.lexer)

            if self.show_logs:
                print(f"{LOG_COLOR}Tokens: {self.lexer.token_log}{RESET_COLOR}")
                print(f"{LOG_COLOR}Parse tree:{RESET_COLOR}")
                display_parse_tree(ast_root)

            self.checker.check(ast_root)
            self.executor.execute(ast_root)

        except RuntimeError as e:
            print(f"Semantic error: {e}")
        except Exception as e:
            print(f"Error executing command: {e}")

    def run(self):
        while True:
            try:
                inp = input("pysh$ ").strip()
                if not inp:
                    continue

                # Toggle logging
                if inp == "--log":
                    self.show_logs = True
                    print("logging enabled")
                    continue
                elif inp == "--nolog":
                    self.show_logs = False
                    print("logging disabled")
                    continue

                # Exit / clear
                if inp == "bye":
                    print("bye (っ＾▿＾)っ")
                    break
                if inp == "clear":
                    os.system("clear")
                    continue

                # AI commands
                if inp.startswith("!"):
                    user_cmd = inp[1:].strip()
                    if not user_cmd:
                        print("Usage: !<instruction>")
                        continue
                    try:
                        # Ensure API key is loaded (and prompt shown)
                        ai.managekeys.load_or_check_ai_api_key()

                        # pass the user's instruction (user_cmd) to the AI
                        ai_output = AI.call_gemini(user_cmd)
                        if self.show_logs:
                            print(f"{LOG_COLOR}AI generated: {ai_output}{RESET_COLOR}")
                        # Pass AI output into the normal pipeline
                        self.process_command(ai_output)
                    except Exception as e:
                        print(f"AI error: {e}")
                    continue

                # Normal commands
                self.process_command(inp)

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