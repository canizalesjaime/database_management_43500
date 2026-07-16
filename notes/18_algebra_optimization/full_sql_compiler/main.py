from lexer import Lexer
from parser import Parser
from visitor import ASTPrinter
from semantic import SemanticAnalyzer
from algebra import AlgebraGenerator
from rel_tree_printer import RelPrinter
from optimizer import Optimizer

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
    #print(ast)
    
    #printer=ASTPrinter()
    #printer.visit(ast)

    analyzer = SemanticAnalyzer(catalog)
    analyzer.analyze(ast)
    print("semantic analysis completed with no errors!")

    generator = AlgebraGenerator()
    tree = generator.visit(ast)

    opty=Optimizer()
    tree= opty.visit(tree)
    
    printer = RelPrinter()
    printer.visit(tree)



if __name__ == "__main__":
    main()