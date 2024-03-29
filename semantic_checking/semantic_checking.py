from AST import *
import visitor
from semantic import Context, Scope, SemanticError, Method, Type
from type_collector import TypeCollectorVisitor
from type_builder import TypeBuilderVisitor
from type_checker import TypeCheckerVisitor

class SemanticCheckingVisitor:
    def __init__(self) -> None:
    #------------------Inicializando tipos por defecto---------------------------------------------------#
        self.context = Context()
        default_types = ['object', 'number', 'string', 'bool']
        for type in default_types:
            self.context.create_type(type)     
    #----------------------------------------------------------------------------------------------------#   
        self.errors = []

        
    def semantic_checking(self, ast):
        type_collector = TypeCollectorVisitor(self.context, self.errors)
        type_collector.visit(ast)
        
        type_builder = TypeBuilderVisitor(self.context)
        type_builder.visit(ast)
        
        type_checker = TypeCheckerVisitor(self.context, self.errors)
        type_checker.visit(ast, self.context, self.errors)
    
        return self.errors
                      

    
    