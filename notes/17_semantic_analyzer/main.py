from lexer import Lexer
from parser import Parser
from visitor import ASTPrinter
from semantic import SemanticAnalyzer


def main():
    catalog = {
    "Users": {
        "id": "INTEGER",
        "name": "TEXT",
        "age": "INTEGER",
    }
}

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

    analyzer = SemanticAnalyzer(catalog)
    analyzer.analyze(ast)



if __name__ == "__main__":
    main()