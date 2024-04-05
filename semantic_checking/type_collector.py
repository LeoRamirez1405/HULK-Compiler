from semantic_checking.semantic import Context, Scope, SemanticError
import semantic_checking.visitor as visitor
from semantic_checking.AST import *
# from AST import *

class TypeCollectorVisitor:
    def __init__(self, context: Context, errors) -> None:
        self.context: Context = context
        self.errors: List[str] = errors
        
    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode):
        for statment in node.statments:
            print(f"Statement (Collector): {statment}")
            print(statment)
            self.visit(statment)
            
    @visitor.when(TypeDefinitionNode)
    def visit(self, node: TypeDefinitionNode):
        try:
            self.context.create_type(node.id.id)
        except:
            self.errors.append(SemanticError(f'El nombre de tipo {node.id.id} ya ha sido tomado [L:{node.location[0]}, C:{node.location[1]}]'))
