from ast import (
    ASTNode,
    Statement,
    Expression,
    SelectStatement,
    Column,
    Table,
    Identifier,
    Literal,
    BinaryExpression,
)


class ASTVisitor:
    """
    Base class for all AST visitors.

    Uses dynamic dispatch to call the appropriate visit_<NodeType>()
    method based on the node's class.
    """

    def visit(self, node):
        """
        Dispatch to the appropriate visit_<ClassName>() method.
        """

        method_name = f"visit_{type(node).__name__}"

        visitor = getattr(
            self,
            method_name,
            self.generic_visit
        )

        return visitor(node)

    def generic_visit(self, node):
        """
        Called if no visit_<NodeType>() method exists.
        """

        raise NotImplementedError(
            f"No visit method defined for {type(node).__name__}"
        )

    # =========================================================
    # Default Traversal Methods
    #
    # These recursively visit child nodes.
    # Future compiler passes can override only the methods
    # they care about.
    # =========================================================

    def visit_SelectStatement(self, node):

        for column in node.columns:
            self.visit(column)

        self.visit(node.table)

        if node.where_clause is not None:
            self.visit(node.where_clause)

    def visit_Column(self, node):

        self.visit(node.identifier)

    def visit_Table(self, node):

        self.visit(node.identifier)

    def visit_BinaryExpression(self, node):

        self.visit(node.left)

        self.visit(node.right)

    def visit_Identifier(self, node):
        """
        Leaf node.
        """
        pass

    def visit_Literal(self, node):
        """
        Leaf node.
        """
        pass


# ============================================================
# Example Visitor
# ============================================================

class ASTPrinter(ASTVisitor):
    """
    Simple visitor that prints the order in which
    nodes are visited.
    """

    def visit_SelectStatement(self, node):

        print("SelectStatement")

        super().visit_SelectStatement(node)

    def visit_Column(self, node):

        print("Column")

        super().visit_Column(node)

    def visit_Table(self, node):

        print("Table")

        super().visit_Table(node)

    def visit_BinaryExpression(self, node):

        print(f"BinaryExpression ({node.operator.name})")

        super().visit_BinaryExpression(node)

    def visit_Identifier(self, node):

        print(f"Identifier: {node.name}")

    def visit_Literal(self, node):

        print(f"Literal: {node.value}")