class Lexer:
    
    def __init__(self):
        self.tokens = []
    
    def tokenize(self, inp: str):
        # Strip leading and trailing spaces
        inp = inp.strip()
        
        i = 0
        while i < len(inp):
            # Skip spaces
            if inp[i] == ' ':
                i += 1
                continue
            
            # Handle quoted strings
            if inp[i] == '"':
                # Find the matching closing quote
                j = i + 1
                while j < len(inp) and inp[j] != '"':
                    j += 1
                
                # If we found a closing quote, extract the string
                if j < len(inp):
                    # Add the quoted string as one token (including the quotes)
                    self.tokens.append(inp[i:j+1])
                    i = j + 1
                else:
                    # Unclosed quote, treat as regular text
                    self.tokens.append(inp[i:])
                    break
            else:
                # Regular tokenization by spaces
                start = i
                while i < len(inp) and inp[i] != ' ':
                    i += 1
                # Add the token (excluding leading/trailing spaces)
                self.tokens.append(inp[start:i])
        
        return self.tokens
    
    pass
