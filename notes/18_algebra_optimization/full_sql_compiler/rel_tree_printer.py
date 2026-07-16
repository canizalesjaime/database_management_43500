from rel_visitor import RelVisitor


class RelPrinter(RelVisitor):
    def visit_TableScan(self, node):
        print(node)

    def visit_Selection(self, node):
        print(node)
        self.visit(node.child)

    def visit_Projection(self, node):
        print(node)
        self.visit(node.child)

    def visit_Join(self, node):
        print("Join")
        self.visit(node.left)
        self.visit(node.right)