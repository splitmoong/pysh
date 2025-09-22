#a token object contains (type, lexeme)
class Token:
    def __init__(self, ttype, lexeme):
        self.type = ttype
        self.lexeme = lexeme
    def __repr__(self):
        return f"{self.type}({self.lexeme})"

'''there are three token types in bash
    1. reserved words 
    exceptions like for, in, do which are only reserved given certian conditions
    2. words
    your commands, arguments, everything goes here mostly
    3. operators
    pipes, ampersand, redirections etc.

see the sets below
'''

#these are the words that are always reserved
RESERVED_ALWAYS = {
    "if", "then", "elif", "else", "fi", "time",
    "until", "while", "do", "done",
    "case", "esac", "coproc", "select", "function",
    "{", "}", "[[", "]]", "!"
}

#these are operators
OPERATORS = {"|", "||", "&", "&&", ";", ">", "<", ">>"}

#a function to classify buffer into reserved and words
def classify_word(word, prev_tokens):
    if word in RESERVED_ALWAYS:
        return "RESERVED"
    if word == "for":
        if not prev_tokens or prev_tokens[-1].type in {"OPERATOR", "RESERVED"}:
            return "RESERVED"
    if word == "in":
        if prev_tokens and prev_tokens[-1].lexeme in {"for", "case", "select"}:
            return "RESERVED"
    if word == "do":
        if prev_tokens and prev_tokens[-1].lexeme in {"for", "while", "until"}:
            return "RESERVED"
    return "WORD"

#the lexer!
def Lexer(code):
    tokens = []
    state = "START"
    buffer = []
    i = 0

    while i < len(code):
        ch = code[i]

        if state == "START":
            if ch.isspace():
                i += 1
                continue
            elif ch == "'":
                state = "IN_SQUOTE"
                buffer.clear()
            elif ch == '"':
                state = "IN_DQUOTE"
                buffer.clear()
            elif any(ch in op for op in OPERATORS):
                state = "OP"
                buffer.clear()
                buffer.append(ch)
            else:
                state = "WORD"
                buffer.clear()
                buffer.append(ch)

        elif state == "WORD":
            if ch.isspace() or any(''.join(buffer)+ch == op or ch == op for op in OPERATORS):
                word = ''.join(buffer)
                ttype = classify_word(word, tokens)
                tokens.append(Token(ttype, word))
                buffer.clear()
                state = "START"
                continue
            else:
                buffer.append(ch)

        elif state == "OP":
            if ''.join(buffer)+ch in OPERATORS:
                buffer.append(ch)
                i += 1
            tokens.append(Token("OPERATOR", ''.join(buffer)))
            buffer.clear()
            state = "START"
            continue

        elif state == "IN_SQUOTE":
            if ch == "'":
                tokens.append(Token("WORD", ''.join(buffer)))
                buffer.clear()
                state = "START"
            else:
                buffer.append(ch)

        elif state == "IN_DQUOTE":
            if ch == '"':
                tokens.append(Token("WORD", ''.join(buffer)))
                buffer.clear()
                state = "START"
            else:
                buffer.append(ch)

        i += 1

    if buffer:
        if state == "WORD":
            word = ''.join(buffer)
            ttype = classify_word(word, tokens)
            tokens.append(Token(ttype, word))
        elif state in {"IN_SQUOTE", "IN_DQUOTE"}:
            raise SyntaxError("Unterminated quoted string")
        elif state == "OP":
            tokens.append(Token("OPERATOR", ''.join(buffer)))

    return tokens
