from visitor import ASTVisitor


class SemanticError(Exception):
    """Raised when semantic analysis fails."""
    pass


class SemanticAnalyzer(ASTVisitor):
    def __init__(self, catalog):
        self.catalog = catalog

        # Current table being analyzed
        self.current_table = None

        # Symbol table for the current query
        self.symbols = {}


    def analyze(self, ast):
        self.visit(ast)


    def visit_SelectStatement(self, node):
        self.visit(node.table)
        for column in node.columns:
            self.visit(column)

        if node.where_clause is not None:
            self.visit(node.where_clause)

   
    def visit_Table(self, node):
        table_name = node.identifier.name

        # checks in catalog which is a python dictionary representing the 
        # database passed to semantic analyzer
        if table_name not in self.catalog: 
            raise SemanticError(f"Unknown table '{table_name}'.")

        self.current_table = table_name
        self.symbols = self.catalog[table_name]

    
    def visit_Column(self, node):
        self.visit(node.identifier)

    
    def visit_Identifier(self, node):
        if node.name not in self.symbols:
            raise SemanticError(f"Unknown column '{node.name}'.")
        node.type = self.symbols[node.name]


    def visit_Literal(self, node):
        if isinstance(node.value, int):
            node.type = "INTEGER"

        elif isinstance(node.value, str):
            node.type = "TEXT"

        else:
            raise SemanticError(f"Unsupported literal '{node.value}'.")

    
    def visit_BinaryExpression(self, node):
        self.visit(node.left)
        self.visit(node.right)
        left_type = node.left.type
        right_type = node.right.type

        if left_type != right_type:
            raise SemanticError(f"Cannot compare {left_type} with {right_type}")

        node.type = "BOOLEAN"