"""
Logical Query Optimizer

This module performs rule-based optimization on the
relational algebra tree.

Current optimization rules

1. Remove Selection(TRUE)
2. Merge consecutive Selections
3. Merge consecutive Projections

Future rules

- Selection Pushdown
- Projection Pushdown
- Join Reordering
- Constant Folding
- Predicate Simplification
"""

from rel_visitor import RelVisitor

from relational_algebra import (
    TableScan,
    Selection,
    Projection,
)


class Optimizer(RelVisitor):
    def optimize(self, root):
        return self.visit(root)

    def visit_TableScan(self, node):
        return node

    def visit_Selection(self, node):
        # First optimize the subtree
        node.child = self.visit(node.child)

        # Rule 1: Remove Selection(TRUE)
        if self.is_true(node.condition):
            return node.child

        # Rule 2(Merge):
        # Selection(A)
        #     |
        # Selection(B)
        # into Selection(A AND B)
        if isinstance(node.child, Selection):
            merged = self.combine_conditions(node.condition,node.child.condition,)
            return Selection(merged,node.child.child,)
        return node


    def visit_Projection(self, node):
        node.child = self.visit(node.child)

        # Rule 3(Merge):
        # Projection
        #     |
        # Projection
        if isinstance(node.child, Projection):
            return Projection(node.columns,node.child.child,)

        return node


    def visit_Join(self, node):
        node.left = self.visit(node.left)
        node.right = self.visit(node.right)

        return node

    ####################################################
    # Helper Functions
    ####################################################

    def is_true(self, condition):
        """
        Returns True if the condition
        is logically TRUE.

        Placeholder implementation.
        """

        return condition is True

    def combine_conditions(self, left, right):
        """
        Combine two predicates.

        Placeholder implementation.

        Later this will create a BinaryExpression
        using the AND operator.
        """

        return ("AND", left, right)