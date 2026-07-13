from lexer import Lexer
from parser import Parser
from visitors import ASTPrinter


def main():
    query = """
    SELECT id, name
    FROM Users
    WHERE age > 18;
    """

    lexer = Lexer(query)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    printer=ASTPrinter()
    printer.visit(ast)



if __name__ == "__main__":
    main()