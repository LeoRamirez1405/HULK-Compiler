from AST import *
import visitor
from semantic import Scope, SemanticError

class SemanticCheckingVisitor:
    def __init__(self) -> None:
        self.errors = {}
    
    @visitor.on('node')
    def visit(self, node, scope):
        pass
    
    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode, scope):
        print('ProgramNode')
        for statment in node.statments:
            self.visit(statment)
            
    @visitor.when(PrintStatmentNode)
    def visit(self, node: PrintStatmentNode, scope):
        self.visit(node.expression)
        
    @visitor.when(KernAssigmentNode)
    def visit(self, node: KernAssigmentNode, scope: Scope):
        if not scope.is_defined(node.id):
            self.errors
        
        
    
            
    