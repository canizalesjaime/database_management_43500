class ASTNode:
    pass


class Statement(ASTNode):
    pass


class Expression(ASTNode):
    pass


# ============================================================
# Statement Nodes
# ============================================================

class SelectStatement(Statement):

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


# ============================================================
# Simple Nodes
# ============================================================

class Identifier(Expression):

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Identifier({self.name})"


class Literal(Expression):

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Literal({self.value})"


class Column(ASTNode):

    def __init__(self, identifier):
        self.identifier = identifier

    def __repr__(self):
        return f"Column({self.identifier})"


class Table(ASTNode):

    def __init__(self, identifier):
        self.identifier = identifier

    def __repr__(self):
        return f"Table({self.identifier})"


# ============================================================
# Expression Nodes
# ============================================================

class BinaryExpression(Expression):

    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):
        return (
            f"BinaryExpression("
            f"{self.left}, "
            f"{self.operator.name}, "
            f"{self.right})"
        )