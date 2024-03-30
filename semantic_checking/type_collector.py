from semantic import Context, Scope, SemanticError, Type
import visitor
# from semantic_checking.AST import *
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
        #print('TypeCollector')
        # self.context.types['test'] = Type('test')
        for statment in node.statments:
            self.visit(statment)
            
        # print(f'Context in Collector: {[item for item in self.context.types.keys()]}')
        # print(f'Scope in Collector: {[func for func in self.scope.functions.keys()]}')
        return self.context, self.scope, self.errors
            
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
    