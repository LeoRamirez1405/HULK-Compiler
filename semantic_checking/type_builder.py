import visitor
import AST

class TypeBuilderVisitor():
    def __init__(self,context) -> None:
        self.context = context
    
    @visitor.on('node')
    def visit(self, node, tabs):
        pass