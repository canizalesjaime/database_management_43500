# Relational Algebra Node Hierarchy
#
# These nodes represent the logical query plan produced after
# semantic analysis. Unlike the AST, these nodes describe
# database operations instead of SQL syntax.


class RelNode:
    """Base class for every relational algebra node."""
    pass


class UnaryRelNode(RelNode):
    """Base class for relational operators with one child."""
    def __init__(self, child):
        self.child = child


class BinaryRelNode(RelNode):
    """Base class for relational operators with two children."""
    def __init__(self, left, right):
        self.left = left
        self.right = right


class TableScan(RelNode):
    """
    Read every tuple from a relation(aka read every row from table).
    """
    def __init__(self, table):
        self.table = table

    def __repr__(self):
        return (f"TableScan({self.table.identifier.name})")


class Selection(UnaryRelNode):
    """
    σ(condition) - filter rows from table based on condition
    """
    def __init__(self, condition, child):
        super().__init__(child)
        self.condition = condition

    def __repr__(self):
        return (f"Selection(condition={self.condition}, child={self.child})")


class Projection(UnaryRelNode):
    """
    π(columns) - select columns to display
    """
    def __init__(self, columns, child):
        super().__init__(child)
        self.columns = columns

    def __repr__(self):
        cols = ", ".join(repr(column) for column in self.columns)
        return (f"Projection(columns=[{cols}], child={self.child})")


class Join(BinaryRelNode):
    """
    Join operator - combines tables(left,right) side by side based on a condition.

    Included now even though the parser doesn't support JOIN yet.
    """
    def __init__(self, left, right, condition):
        super().__init__(left, right)
        self.condition = condition

    def __repr__(self):
        return (f"Join(\n left={self.left},\n right={self.right},\n condition={self.condition}\n)")