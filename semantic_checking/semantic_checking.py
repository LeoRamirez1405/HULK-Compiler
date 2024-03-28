from AST import *
import visitor
from type_collector import *
from semantic import Scope, Context, SemanticError
# from cmp.semantic import Context, SemanticError
from Token import Token

class SemanticCheckingVisitor:
    def __init__(self):
        self.context = Context()
        default_types = ['Object','Number','Boolean','String','Vector']
        for type in default_types:
            self.context.create_type(type)
        self.errors = []
        print('inicializando checker visitor') #* ✔
        
    @visitor.on('node')
    def visit(self, node, scope):
        print('on visitor') #! No imprime
        pass
    
    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode):
        scope = Scope(parent=None)
        for statment in node.statement_list:
            print('visit') #! No imprime
            self.visit(statment, scope)
        
        # type_collector = TypeCollevtorVisitor()
        # ast = type_collector.visit(node)
        
    @visitor.when(PrintStatementNode)
    def visit(self, node: PrintStatementNode, scope: Scope):
        self.visit(node.expression, scope)
        
    @visitor.when(IfStructureNode)
    def visit(self, node: IfStructureNode, scope: Scope):
        # the condition variables needs to be defined in scope
        self.visit(node.condition, scope)
        
        inner_scope = scope.create_child(scope)
        for statment in node.statement_list:
            self.visit(statment, inner_scope) 
            
        # Each elif is an IfStructureNode with a elif = None and  else = None
        inner_scope = scope.create_child(scope)
        for elseif in node.contElif:
            self.visit(elseif, scope)
            
        # An else is an IfStructureNode with elif = None and else = None
        self.visit(node.contElse, scope)
        
    @visitor.when(WhileStructureNode)
    def visit(self, node: WhileStructureNode, scope: Scope):
        self.visit(node.condition, scope)
        inner_scope = scope.create_child(scope)
        for statment in node.statement_list:
            self.visit(statment, inner_scope)
            
    @visitor.when(ForStructureNode)
    def visit(self, node: ForStructureNode, scope: Scope):
        inner_scope: Scope = scope.create_child(scope)
        for var in node.init_assignments:
            if scope.is_defined(var.id):
                self.errors.append(SemanticError(f'The name {var.id} has already been taken. location: {var.token.location}'))
            else:
                inner_scope.define_variable(var.id, var.type)
        self.visit(node.condition, inner_scope)
        self.visit(node.increment_assignments, inner_scope)
        self.visit(node.statement_list, inner_scope)
        
    @visitor.when(TypeDefinitionNode)
    def visit(self, node, scope):
        print('entro')
        
    @visitor.when(LetNode)
    def visit(self, node: LetNode, scope: Scope):
        for var in node.assigments:
            self.visit(var, scope)
            
    @visitor.when(AssigNode)
    def visit(self, node: AssigNode, scope: Scope):
        if scope.is_defined(node.id):
            self.errors.append(SemanticError(f'The name {node.id} has already been taken. location: {node.token.location}'))
        else:
            scope.define_variable(node.id, node.type)
            
        self.visit(node.expression, scope)
        
    @visitor.when(AttributeDefinitionNode)
    def visit(self, node: AttributeDefinitionNode, scope: Scope):
        if scope.is_defined(node.identifier):
            self.errors.append(SemanticError(f'The name {node.identifier} has already been taken. location: {node.token.location}'))
        else:
            scope.define_variable(node.identifier, node.type_annotation)
        self.visit(node.expression, scope)
        
    @visitor.when(NumberNode)
    def visit(self, node: NumberNode, scope: Scope):
        print('llego')
        pass
    
    @visitor.when(BooleanNode)
    def visit(self, node: BooleanNode, scope: Scope):
        pass