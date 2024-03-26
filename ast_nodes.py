from cmp.ast import *
class ProgramNode(Node):
    def __init__(self, statement_list):
        self.statement_list = statement_list
        
#------------------------------------------------------------------------Non-Create-statments----------------------------------------------------------------------#
class PrintStatementNode(Node):
    def __init__(self, expression):
        self.expression = expression
        
class IfStructureNode(Node):
    def __init__(self, condition, statement_list, contElif, contElse):
        self.condition = condition
        self.statement_list = statement_list
        self.contElif = contElif
        self.contElse = contElse
        
class WhileStructureNode(Node):
    def __init__(self, condition, statement_list):
        self.condition = condition
        self.statement_list = statement_list
        
class ForStructureNode(Node):
    def __init__(self, init_assignments, condition, statement_list, assignments):
        self.init_assignments = init_assignments
        self.increment_assignments = assignments
        self.condition = condition
        self.statement_list = statement_list
        
#---------------------------------------Create-Statments-----------------------------------------------------------------------------------------------------------#
class TypeDefinitionNode(Node):
    def __init__(self, identifier, attribute_definition, method_definition, inheritance):
        self.identifier = identifier
        self.inheritance = inheritance
        self.attribute_definition = attribute_definition
        self.method_definition = method_definition
        
class FunctionDefinitionNode(Node):
    def __init__(self, identifier, type_anotation, parameters, statement_list):
        self.identifier = identifier
        self.type_anotation = type_anotation
        self.parameters = parameters
        self.statement_list = statement_list

class AssignmentNode(Node):
    def __init__(self, identifiers, expressions):
        self.identifiers = identifiers
        self.expressions = expressions
        
class InstanceCreationNode(Node):
    def __init__(self, identifier, type, arguments):
        self.identifier = identifier
        self.type = type
        self.arguments = arguments
        
#--------------------------------------------------------------------------------------------------------------------------------------------------------------#        
        
class TypeNode(Node):
    def __init__(self, type) :
        self.type_name = type
        
class BooleanExpression(Node):
    def __init__(self, expression, operator, expresion_2) -> None:
        self.expression = expression
        self.operator = operator
        self.expression_2 = expresion_2
    
class NotConditionNode(Node):
    def __init__(self, condition) -> None:
        self.condition = condition
        
class ConditionCollectionNode(Node):
    def __init__(self, conditions, operators) -> None:
        self.conditions = conditions
        self.operators = operators
        
class IsNode(Node):
    def __init__(self, expression, type) -> None:
        self.expression = expression
        self.type = type
        
     
        
class ConditionNode(Node):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

class ExpressionNode(Node):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

class TermNode(Node):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

class FactorNode(Node):
    def __init__(self, value):
        self.value = value

class FunctionCallNode(Node):
    def __init__(self, identifier, arguments):
        self.identifier = identifier
        self.arguments = arguments








class MemberAccessNode(Node):
    def __init__(self, identifier, member):
        self.identifier = identifier
        self.member = member

class AttributeDefinitionNode(Node):
    def __init__(self, type_annotation, expression):
        self.type_annotation = type_annotation
        self.expression = expression

class MethodDefinitionNode(Node):
    def __init__(self, identifier, parameters, expression):
        self.identifier = identifier
        self.parameters = parameters
        self.expression = expression

class InheritanceNode(Node):
    def __init__(self, identifier):
        self.identifier = identifier



class MethodOverrideNode(Node):
    def __init__(self, identifier, parameters, expression):
        self.identifier = identifier
        self.parameters = parameters
        self.expression = expression
