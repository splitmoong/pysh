#!/usr/bin/env python3
import lexer
import parser
import checker
import executor
import os

# ANSI color for light grey
LOG_COLOR = "\033[90m"
RESET_COLOR = "\033[0m"

class REPL:
    def __init__(self):
        self.lexer = lexer.Lexer()
        self.parser = parser.Parser()
        self.checker = checker.SemanticChecker()
        self.executor = executor.Executor()
        self.show_logs = False  # Start with logs off

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

                # Exit command
                if inp == "bye":
                    print("bye :)")
                    break

                # Clear command
                if inp == "clear":
                    os.system("clear")
                    continue

                # Tokenize input
                tokens = self.lexer.tokenize(inp)
                if self.show_logs:
                    print(f"{LOG_COLOR}Tokens: {tokens}{RESET_COLOR}")

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
