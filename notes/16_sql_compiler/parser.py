from lexer import TokenType
from ast import (
    SelectStatement,
    Column,
    Table,
    Identifier,
    Literal,
    BinaryExpression
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


    # --------------------------------------------------------

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


    # --------------------------------------------------------

    def parse_select_list(self):

        columns = []

        while True:

            token = self.consume(TokenType.IDENTIFIER)

            columns.append(
                Column(
                    Identifier(token.value)
                )
            )

            if self.peek().type != TokenType.COMMA:
                break

            self.advance()


        return columns


    # --------------------------------------------------------

    def parse_table(self):

        token = self.consume(TokenType.IDENTIFIER)

        return Table(
            Identifier(token.value)
        )


    # --------------------------------------------------------

    def parse_where(self):

        self.consume(TokenType.WHERE)

        return self.parse_binary_expression()


    # --------------------------------------------------------

    def parse_binary_expression(self):

        left = Identifier(
            self.consume(TokenType.IDENTIFIER).value
        )


        operator = self.advance()


        if operator.type not in (
            TokenType.EQUAL,
            TokenType.GREATER_THAN,
            TokenType.LESS_THAN,
        ):
            raise Exception(
                "Expected comparison operator."
            )


        token = self.advance()


        if token.type == TokenType.NUMBER:

            right = Literal(token.value)


        elif token.type == TokenType.STRING:

            right = Literal(token.value)


        elif token.type == TokenType.IDENTIFIER:

            right = Identifier(token.value)


        else:

            raise Exception(
                "Expected literal or identifier."
            )


        return BinaryExpression(
            left,
            operator.type,
            right
        )