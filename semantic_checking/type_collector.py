import visitor

class TypeCollevtorVisitor:
    def __init__(self, context) -> None:
        self.context = context
    
    @visitor.on('node')
    def visit(self, node, tabs):
        pass