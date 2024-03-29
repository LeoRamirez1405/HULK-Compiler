from semantic import Context, Scope, SemanticError
import visitor
from AST import *

class TypeCollectorVisitor:
    def __init__(self, context: Context, scope: Scope, errors) -> None:
        self.context: Context = context
        self.scope: Scope = scope
        self.errors: List[str] = errors
        
    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode):
        for statment in node.statments:
            self.visit(statment)
            
    @visitor.when(TypeDefinitionNode)
    def visit(self, node: TypeDefinitionNode):
        try:
            self.context.create_type(node.id)
        except:
            self.errors.append(SemanticError(f'El nombre de tipo {node.id} ya ha sido tomado'))
            
    #Aqui solo se va a entrar si la funcion esta definida en el ProgramNode
    @visitor.when(FunctionDefinitionNode)
    def visit(self, node: FunctionDefinitionNode):
        if not node.id in self.scope.functions:
            self.scope.functions[node.id] = []
    