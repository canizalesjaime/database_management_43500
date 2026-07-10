from enum import Enum, auto


class TokenType(Enum):
    SELECT = auto()
    FROM = auto()
    WHERE = auto()

    IDENTIFIER = auto()

    NUMBER = auto()
    STRING = auto()

    EQUAL = auto()
    GREATER_THAN = auto()
    LESS_THAN = auto()

    COMMA = auto()
    SEMICOLON = auto()

    EOF = auto()


class Token:
    def __init__(self, token_type, value=None):
        self.type = token_type
        self.value = value

    def __repr__(self):
        if self.value is None:
            return f"{self.type.name}"
        return f"{self.type.name}({self.value})"


class Lexer:
    KEYWORDS = {
        "SELECT": TokenType.SELECT,
        "FROM": TokenType.FROM,
        "WHERE": TokenType.WHERE,
    }

    def __init__(self, text):
        self.text = text # thing we are reading 
        self.pos = 0 # position in thing we are reading 

    def peek(self): # look at current character in position pos of text
        if self.pos >= len(self.text):
            return None
        return self.text[self.pos]

    def advance(self): # move pos up by one character
        self.pos += 1

    def skip_whitespace(self): # skip whitespaces
        while self.peek() is not None and self.peek().isspace():
            self.advance()

# find and set identifier(table, column name, etc) tokens, 
# if not identifier this will set to SELECT, WHERE, OR FROM token
    def identifier(self):  
        start = self.pos

        while (
            self.peek() is not None
            and (self.peek().isalnum() or self.peek() == "_")
        ):
            self.advance()

        word = self.text[start:self.pos]

        upper = word.upper()

        if upper in self.KEYWORDS:
            return Token(self.KEYWORDS[upper])

        return Token(TokenType.IDENTIFIER, word)
    

    def number(self): #if first character is a digit, start scanning for a number
        start = self.pos

        while self.peek() is not None and self.peek().isdigit():
            self.advance()

        value = int(self.text[start:self.pos])

        return Token(TokenType.NUMBER, value)
    

    def string(self): #if first character is an opening quote, start scanning for string
        self.advance()  # Skip opening quote

        start = self.pos

        while self.peek() != "'":
            if self.peek() is None:
                raise Exception("Unterminated string.")
            self.advance()

        value = self.text[start:self.pos]

        self.advance()  # Skip closing quote

        return Token(TokenType.STRING, value)


    def next_token(self): # scan for next token and call approriate method
        self.skip_whitespace()

        current = self.peek()

        if current is None:
            return Token(TokenType.EOF)

        if current.isalpha() or current == "_":
            return self.identifier()

        if current.isdigit():
            return self.number()

        if current == "'":
            return self.string()

        if current == ",":
            self.advance()
            return Token(TokenType.COMMA)

        if current == ";":
            self.advance()
            return Token(TokenType.SEMICOLON)

        if current == "=":
            self.advance()
            return Token(TokenType.EQUAL)

        if current == ">":
            self.advance()
            return Token(TokenType.GREATER_THAN)

        if current == "<":
            self.advance()
            return Token(TokenType.LESS_THAN)

        raise Exception(f"Unexpected character: {current}")


    def tokenize(self):
        tokens = []

        while True:
            token = self.next_token()
            tokens.append(token)
            if token.type == TokenType.EOF:
                break

        return tokens


query1 = """
SELECT name
FROM Users
WHERE age > 18;
"""

# AND doesnt quite work
query2 = """
SELECT id, name, birth_name
FROM Users
WHERE age > 18 and id < 10000;
"""
lexer = Lexer(query2)

tokens = lexer.tokenize()

for token in tokens:
    print(token)