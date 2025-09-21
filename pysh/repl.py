#!/usr/bin/env python3
import lexer
import parser
import checker
import executor

import os

class REPL:
    def __init__(self):
        self.lexer = lexer.Lexer()
        self.parser = parser.Parser()
        self.checker = checker.SemanticChecker()
        self.executor = executor.Executor()

    def run(self):
        while True:
            try:
                # Show prompt and read input
                inp = input("pysh$ ")
                if not inp.strip():
                    continue
                
                # Exit command
                if inp.strip() == "bye":
                    print("bye :)")
                    break
                
                # Clear command
                if inp.strip() == "clear":
                    os.system("clear")  # works on Linux/macOS
                    continue

                # Tokenize input
                tokens = self.lexer.tokenize(inp)
                print("Tokens:", tokens)  # for now, just debug output

                # Parse tokens
                self.parser.parse(tokens)
                self.parser.tree.display()
                
                # Semantic check
                try:
                    self.checker.check(self.parser.tree)
                except RuntimeError as e:
                    print(f"Semantic error: {e}")
                    continue  # don't exit the loop
                
                # Execute the command
                self.executor.execute(self.parser.tree)

            except KeyboardInterrupt:
                print()  # newline on Ctrl+C
            except EOFError:
                print()
                break

def main():
    repl = REPL()
    repl.run()

if __name__ == "__main__":
    main()
