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
        default_types = ['object', 'number', 'string', 'bool', 'void']
        for type in default_types:
            self.context.create_type(type)   
    
    #------------------Inicializando funciones por defecto-----------------------------------------------#
        self.scope = Scope(parent=None)
        self.default_functions = ['sen', 'cos', 'sqrt', 'exp']
        for func in self.default_functions:
            self.scope.functions[func] = Method(func, ['expression'], [self.context.get_type('number')], self.context.get_type('number'))
            
        self.default_functions.extend(['rand', 'log', 'print'])
        self.scope.functions['rand'] = [Method(func, [], [], self.context.get_type('number'))]
        self.scope.functions['log'] = [Method(func, ['base', 'expression'], [self.context.get_type('number'), self.context.get_type('number')], self.context.get_type('number'))]
        self.scope.functions['print'] = [Method(func, ['expression'], [self.context.get_type('object')], self.context.get_type('string'))]

    #----------------------------------------------------------------------------------------------------# 
        self.errors = []

        
    def semantic_checking(self, ast):
        type_collector = TypeCollectorVisitor(self.context, self.errors)
        type_collector.visit(ast)
        
        type_builder = TypeBuilderVisitor(self.context, self.scope, self.errors)
        type_builder.visit(ast)
        
        type_checker = TypeCheckerVisitor(self.context, self.scope, self.errors, self.default_functions)
        type_checker.visit(ast)
    
        return self.errors
                      

    
    