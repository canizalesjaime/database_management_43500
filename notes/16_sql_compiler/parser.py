from lexer import Lexer, TokenType


class SelectStatement:
    def __init__(self, columns, table, where_clause):
        self.columns = columns
        self.table = table
        self.where_clause = where_clause

    def __repr__(self):
        return (
            f"SelectStatement("
            f"columns={self.columns}, "
            f"table={self.table}, "
            f"where={self.where_clause})"
        )


class Column:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Column({self.name})"


class Table:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Table({self.name})"


class Comparison:
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):
        return (
            f"Comparison("
            f"{self.left} "
            f"{self.operator.name} "
            f"{self.right})"
        )


class Parser:

    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0


    def peek(self):
        return self.tokens[self.pos]


    def advance(self):
        token = self.peek()
        self.pos += 1
        return token


    def consume(self, expected):
        token = self.peek()
        if token.type != expected:
            raise Exception(
                f"Expected {expected.name}, got {token.type.name}"
            )
        return self.advance()


    def parse(self):
        self.consume(TokenType.SELECT)
        columns = self.parse_select_list()
        self.consume(TokenType.FROM)
        table = self.parse_table()
        where_clause = None
        if self.peek().type == TokenType.WHERE:
            where_clause = self.parse_where()

        self.consume(TokenType.SEMICOLON)
        self.consume(TokenType.EOF)

        return SelectStatement(
            columns,
            table,
            where_clause
        )


    def parse_select_list(self):
        columns = []

        while True:
            token = self.consume(TokenType.IDENTIFIER)
            columns.append(Column(token.value))
            if self.peek().type != TokenType.COMMA:
                break

            self.advance()

        return columns


    def parse_table(self):
        token = self.consume(TokenType.IDENTIFIER)
        return Table(token.value)


    def parse_where(self):
        self.consume(TokenType.WHERE)
        left = self.consume(TokenType.IDENTIFIER)
        operator = self.advance()
        if operator.type not in (
            TokenType.EQUAL,
            TokenType.GREATER_THAN,
            TokenType.LESS_THAN,
        ):
            raise Exception("Expected comparison operator.")

        right = self.advance()

        if right.type not in (
            TokenType.NUMBER,
            TokenType.STRING,
            TokenType.IDENTIFIER,
        ):
            raise Exception("Expected value.")

        return Comparison(
            left.value,
            operator.type,
            right.value,
        )


query = """
SELECT id, name
FROM Users
WHERE age > 18;
"""

lexer = Lexer(query)

tokens = lexer.tokenize()

parser = Parser(tokens)

ast = parser.parse()

print(ast)