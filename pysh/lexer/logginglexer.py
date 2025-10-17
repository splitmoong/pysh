# lexer/logginglexer

class LoggingLexer:
    
    def __init__(self, lexer):
        # Use object.__setattr__ to avoid recursion
        object.__setattr__(self, 'lexer', lexer)
        object.__setattr__(self, 'token_log', [])
        
    def __getattr__(self, name):
        return getattr(self.lexer, name)
    
    def __setattr__(self, name, value):
        # keep wrapper's own attributes local
        if name in ('lexer', 'token_log'):
            object.__setattr__(self, name, value)
        else:
            setattr(self.lexer, name, value)

    def token(self):
        """Called by the parser to get the next token."""
        tok = self.lexer.token()
        if tok:
            self.token_log.append(tok)
        return tok

    def input(self, data):
        """Called to feed a new string to the lexer."""
        self.token_log.clear()  # Clear log for new input
        self.lexer.input(data)

    def __iter__(self):
        """Required by ply.yacc."""
        return self