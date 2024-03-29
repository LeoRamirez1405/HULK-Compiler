from semantic import Context, SemanticError
import visitor
from AST import *

class TypeCollectorVisitor:
    def __init__(self, context, errors) -> None:
        self.context: Context = context
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
            
        # for method in node.methods:
        #     self.visit(method)
            
    # @visitor.when(FunctionDefinitionNode)
    # def visit(self, node: FunctionDefinitionNode):
    #     for statment in node.body:
    #         self.visit(statment)
            
    