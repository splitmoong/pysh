#!/usr/bin/env python3
from lexer import Lexer

class REPL:
    def __init__(self):
        self.lexer = Lexer()

    def run(self):
        while True:
            try:
                # Show prompt and read input
                inp = input("pysh$ ")
                if not inp.strip():
                    continue

                # Tokenize input
                tokens = self.lexer.tokenize(inp)
                print("Tokens:", tokens)  # for now, just debug output

                # Parse tokens
                #ast = self.parser.parse(tokens)
                #print("AST:", ast)       # debug output

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
