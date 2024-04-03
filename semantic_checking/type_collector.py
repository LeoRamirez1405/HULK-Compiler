from semantic_checking.semantic import Context, Scope, SemanticError
import semantic_checking.visitor as visitor
from semantic_checking.AST import *
# from AST import *

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
            print(statment)
            self.visit(statment)
        
        # print('Context')
        # for name, type in self.context.types.items():
        #     print(f'Type: {name} : ')
        #     if type.parent: print(type.parent.name)
        #     print(f'attributes: {[attr.name for attr in type.attributes]}')
        #     print(f'attributes: {[method.name for method in type.methods]}')
            
    @visitor.when(TypeDefinitionNode)
    def visit(self, node: TypeDefinitionNode):
        # node_id: IdentifierNode = node.id
        try:
            self.context.create_type(node.id.id)
        except:
            self.errors.append(SemanticError(f'El nombre de tipo {node.id.id} ya ha sido tomado'))
            
    #Aqui solo se va a entrar si la funcion esta definida en el ProgramNode
    @visitor.when(FunctionDefinitionNode)
    def visit(self, node: FunctionDefinitionNode):
        # print(type(node.id))
        if not node.id.id in self.scope.functions:
            self.scope.functions[node.id.id] = []
        else:
            self.errors.append(SystemError(f'El metodo {node.id.id} ya existe'))
    
    @visitor.when(KernAssigmentNode)
    def visit(self, node: KernAssigmentNode):
        print('kern assigment: ', node)
        if not self.scope.is_defined(node.id.id):
            self.scope.define_variable(node.id.id, self.context.get_type('object')) 
        else:
            # print(node.id.id)
            self.errors.append(SemanticError(f'La variable {node.id.id} ya existe')) 
            
    @visitor.when(CollectionNode)
    def visit(self, node: CollectionNode):
        for item in node.collection:
            self.visit(item)