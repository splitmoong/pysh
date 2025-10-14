"""
lexer for pysh shell

Token types:
- COMMAND: First word in a command sequence (e.g., ls, echo, mkdir)
- ARG: Arguments for commands (e.g., -l, file.txt, ^car)
- STRING_LITERAL: Quoted strings preserving spaces ("Hello World")

- PIPE: | operator for piping commands
- REDIRECT_OUT: > operator for output redirection
- REDIRECT_OUT_APPEND: >> operator for appending output
- REDIRECT_IN: < operator for input redirection
- SEMICOLON: ; to separate multiple commands
- BACKGROUND: & for background execution
- VARIABLE: $VAR environment variables
- COMMENT: # and rest of line (ignored like us :)

new
- LOGICAL_AND: && operator for chaining commands
- LOGICAL_OR: || operator for chaining commands
"""

class Token:
    def __init__(self, typ, value):
        self.type = typ
        self.value = value
    
    def __repr__(self):
        return f"{self.type}({self.value})"

class Lexer:
    def __init__(self):
        pass
    
    def tokenize(self, inp: str):
        inp = inp.strip()
        i = 0
        tokens = []

        while i < len(inp):
            
            if inp[i].isspace():
                i += 1
                continue
            

            #STRING_LITERAL
            if inp[i] in ('"', "'"):
                quote_char = inp[i]
                j = i + 1
                while j < len(inp) and inp[j] != quote_char:
                    j += 1
                if j < len(inp):
                    tokens.append(Token("STRING_LITERAL", inp[i+1:j]))
                    i = j + 1
                else:
                    # Unclosed quote
                    tokens.append(Token("STRING_LITERAL", inp[i+1:]))
                    i = len(inp)
                    
            
            #LOGICAL_OR
            elif inp[i] == '|' and i+1 < len(inp) and inp[i+1] == '|':
                tokens.append(Token("LOGICAL_OR", "||"))
                i += 2
                
                
            #PIPE
            elif inp[i] == '|':
                tokens.append(Token("PIPE", "|"))
                i += 1
            
            
            #REDIRECTION
            elif inp[i] == '>' and i+1 < len(inp) and inp[i+1] == '>':
                tokens.append(Token("REDIRECT_OUT_APPEND", ">>"))
                i += 2
            elif inp[i] == '>':
                tokens.append(Token("REDIRECT_OUT", ">"))
                i += 1
            elif inp[i] == '<':
                tokens.append(Token("REDIRECT_IN", "<"))
                i += 1
                
            
            #SEMICOLON
            elif inp[i] == ';':
                tokens.append(Token("SEMICOLON", ";"))
                i += 1
            
            
            #LOGICAL_AND       
            elif inp[i] == '&' and i+1 < len(inp) and inp[i+1] == '&':
                tokens.append(Token("LOGICAL_AND", "&&"))
                i += 2
            
            
            #BACKGROUND
            elif inp[i] == '&':
                tokens.append(Token("BACKGROUND", "&"))
                i += 1
            

            #VARIABLE
            elif inp[i] == '$':
                start = i
                i += 1
                while i < len(inp) and (inp[i].isalnum() or inp[i] == '_'):
                    i += 1
                tokens.append(Token("VARIABLE", inp[start:i]))
            
            
            #COMMENT
            elif inp[i] == '#':
                break  # ignore rest of line
            
            
            #COMMAND / ARGUMENT
            else:
                start = i
                while i < len(inp) and not inp[i].isspace() and inp[i] not in '|&;<>':
                    i += 1
                word = inp[start:i]
                # Determine type
                if len(tokens) == 0 or tokens[-1].type in ("PIPE", "SEMICOLON", "LOGICAL_OR", "LOGICAL_AND", "BACKGROUND"):
                    token_type = "COMMAND"
                else:
                    token_type = "ARG"
                tokens.append(Token(token_type, word))
        
        
        return tokens
