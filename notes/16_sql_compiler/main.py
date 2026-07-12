from lexer import Lexer
from parser import Parser


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


    print(ast)



if __name__ == "__main__":
    main()