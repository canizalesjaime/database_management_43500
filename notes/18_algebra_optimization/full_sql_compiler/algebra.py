"""
AST -> Relational Algebra Generator

This module converts an annotated AST into a logical
relational algebra tree.
"""

from visitor import ASTVisitor

from relational_algebra import (
    TableScan,
    Selection,
    Projection,
)


class AlgebraGenerator(ASTVisitor):
    def visit_SelectStatement(self, node):
        root = self.visit(node.table) # FROM, root is TableScan node

        # WHERE, sets tablescan as child of selection
        if node.where_clause is not None: 
            root = Selection(node.where_clause,root,)

        # SELECT, sets selection as child of projection
        root = Projection(node.columns,root,) 

        return root # functional form: Projection(Selection(TableScan(table)))

    def visit_Table(self, node):
        return TableScan(node)

    # The remaining AST nodes don't generate relational operators directly.
    def visit_Column(self, node):
        return node

    def visit_Identifier(self, node):
        return node

    def visit_Literal(self, node):
        return node

    def visit_BinaryExpression(self, node):
        return node