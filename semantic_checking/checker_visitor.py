from AST import *
import visitor
from semantic import Context, Scope, SemanticError, Method
from type_collector import TypeCollectorVisitor

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
        
        type_collector = TypeCollectorVisitor(self.context, self.errors)
        type_collector.visit(node)
        
        
        
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
        
    @visitor.when(LetNode)
    def visit(self, node: LetNode, scope: Scope):
        if scope.is_local(node.id):
            self.errors.append(SemanticError(f'La variable {node.id} ya esta definida.'))
        else:
            scope.define_variable(node.id, self.context.get_type('object'))
            self.visit(node.expression)
        
    @visitor.when(TypeNode)
    def visit(self, node: TypeNode, scope):
        try:
            self.context.types[node.type]
        except:
            self.errors.append(SemanticError(f'Tipo no definido'))
            
    @visitor.when(FunctionDefinitionNode)
    def visit(self, node: FunctionCallNode, scope: Scope):
        try:
            args_len = scope.functions[id]
            if args_len == len(node.args):
                self.errors.append(SemanticError(f'La funcion {node.id} ya esta definida'))
                #!aki poner una lista de parametros a las funciones ver en definicion de Scope
        except:
            #TODO Se puede instanciar la clase Method de semantic~seria algo similar a scope.functions[node.id] = nodmethod(node. ...)
            #* Por el momento en el diccionario tengo el id de la funcion con su cantidad de parametros
            scope.functions[node.id] = len(node.args)
            
    @visitor.when(FunctionCallNode)
    def visit(self, node: FunctionCallNode, scope: Scope):
        try: 
            args_len = scope.functions[id]
            if args_len != len(node.args):
                self.errors.append(f'La funcion {id} requiere {args_len} cantidad de parametros pero solo {len(node.args)} fueron dados')
        except:
            self.errors.append(f'La funcion {node.id} no esta definida.')
            

            
    
        
        
    
            
    