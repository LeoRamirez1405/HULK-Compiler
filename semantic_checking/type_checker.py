from AST import *
class TypeCheckerVisitor:
    def __init__(self, context, errors) -> None:
        self.context = context
        self.errors = errors

    @visitor.when()
    def visit(self, node: BinaryNode, logger):
        self.visit(node.left, logger)
        self.visit(node.right, logger)
        if node.left.computed_type != node.right.computed_type:
            logger.error("Type mismatch...")
            node.computed_type = None
        else:
            node.computed_type = node.left.computed_type

    @visitor.on('node')
    def visit(self, node, logger):
        for child in node.children:
            self.visit(child, logger)

    def visitor(arg_type):
        def decorator(fn):
            declaring_class = _declaring_class(fn)
            _methods[(declaring_class, arg_type)] = fn
            return _visitor_impl
        return decorator
    
    def _visitor_impl(self, arg):
        method = _methods[(_qualname(type(self)), type(arg))]
        return method(self, arg)
