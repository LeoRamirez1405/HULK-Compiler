from AST import *
import visitor
from semantic import Context, Scope, SemanticError, Method

class SemanticCheckingVisitor:
    def __init__(self) -> None:
        self.errors = []
        self.context = Context()
        self.scope = Scope()
    
    @visitor.on('node')
    def visit(self, node, scope):
        pass
    
    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode, scope=None):
        print('ProgramNode')
        for statment in node.statments:
            self.visit(statment, self.scope)  
                      
    @visitor.when(PrintStatmentNode)
    def visit(self, node: PrintStatmentNode, scope):
        self.visit(node.expression, scope)
        
    @visitor.when(KernAssigmentNode)
    def visit(self, node: KernAssigmentNode, scope: Scope):
        if not scope.is_defined(node.id):
            self.errors.append(SemanticError('Asignacion de valor a una variable no definida'))
            
        self.visit(node.expression, scope)
        
    @visitor.when(TypeNode)
    def visit(self, node: TypeNode, scope):
        try:
            self.context.types[node.type]
        except:
            self.errors.append('Tipo no definido')
            
    @visitor.when(FunctionDefinitionNode)
    def visit(self, node: FunctionCallNode, scope: Scope):
        try:
            args_len = scope.functions[id]
            if args_len != len(node.args):
                self.errors.append(f'La funcion {node.id} ya esta definida')
        except:
            #TODO Se puede instanciar la clase Method de semanticÇ~seria algo similar a scope.functions[node.id] = nodmethod(node. ...)
            scope.functions[node.id] = node
            
    @visitor.when(FunctionCallNode)
    def visit(self, node: FunctionCallNode, scope: Scope):
        try: 
            args_len = scope.functions[id]
            if args_len != len(node.args):
                self.errors.append(f'La funcion {id} requiere {args_len} cantidad de parametros pero solo {len(node.args)} fueron dados')
        except:
            self.errors.append(f'La funcion {node.id} no esta definida.')
            
    
        
        
    
            
    