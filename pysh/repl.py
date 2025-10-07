#!/usr/bin/env python3
import sys
import os
import atexit
import readline
from pathlib import Path

# Ensure project root is in sys.path (for ai.py and others)
sys.path.append(str(Path(__file__).resolve().parent))

import lexer
import parser
import checker
import executor


from ai.ai import AI
import contextlib

# ANSI color for light grey
LOG_COLOR = "\033[90m"
RESET_COLOR = "\033[0m"

HISTORY_FILE = Path.home() / ".pysh_history"

class REPL:
    def __init__(self):
        self.lexer = lexer.Lexer()
        self.parser = parser.Parser()
        self.checker = checker.SemanticChecker()
        self.executor = executor.Executor()
        self.show_logs = False

        if HISTORY_FILE.exists():
            readline.read_history_file(HISTORY_FILE)
        atexit.register(self._save_history)

    def _save_history(self):
        try:
            readline.write_history_file(HISTORY_FILE)
        except Exception as e:
            print(f"Warning: could not save history: {e}")

    def process_command(self, cmd: str):
        """Process any command string through lexer, parser, checker, executor."""
        try:
            tokens = self.lexer.tokenize(cmd)
            if self.show_logs:
                print(f"{LOG_COLOR}Tokens: {tokens}{RESET_COLOR}")

            self.parser.parse(tokens)
            if self.show_logs:
                print(f"{LOG_COLOR}Parse tree:{RESET_COLOR}")
                self.parser.tree.display()

            self.checker.check(self.parser.tree)
            self.executor.execute(self.parser.tree)
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
                        # pass the user's instruction (user_cmd) to the AI
                        with open(os.devnull, "w") as f, contextlib.redirect_stderr(f), contextlib.redirect_stdout(f):
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
