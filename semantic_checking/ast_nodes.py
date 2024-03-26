from abc import ABC
from typing import List

from semantic_checking.Token import Token

class Node(ABC):
    def __init__(self, token):
        self.token: Token = token
        
class AtomicNode(Node):
    def __init__(self, lex):
        self.lex = lex

class UnaryNode(Node):
    def __init__(self, token, node):
        super().__init__(token)
        self.node = node

    def evaluate(self):
        value = self.node.evaluate()
        return self.operate(value)

    @staticmethod
    def operate(value):
        raise NotImplementedError()

class BinaryNode(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def evaluate(self):
        lvalue = self.left.evaluate()
        rvalue = self.right.evaluate()
        return self.operate(lvalue, rvalue)

    @staticmethod
    def operate(lvalue, rvalue):
        raise NotImplementedError()
    
#----------------------------------------------------------Basic-Nodes---------------------------------------------------------------------------------------------#

class StatmentNode(Node):
    pass

class ProgramNode(Node):
    def __init__(self, statement_list: List[StatmentNode]):
        self.statement_list: List[StatmentNode] = statement_list
        
#------------------------------------------------------------------------Non-Create-statments----------------------------------------------------------------------#
class PrintStatementNode(StatmentNode):
    def __init__(self, expression):
        self.expression = expression
        
class IfStructureNode(StatmentNode):
    def __init__(self, condition, statement_list, contElif, contElse):
        self.condition = condition
        self.statement_list = statement_list
        self.contElif = contElif
        self.contElse = contElse
        
class WhileStructureNode(StatmentNode):
    def __init__(self, condition, statement_list):
        self.condition = condition
        self.statement_list = statement_list
        
class AssigNode(Node):
    def __init__(self, id, type, expression) -> None:
        self.id = id
        self.type = type
        self.expression = expression
        
class ForStructureNode(StatmentNode):
    def __init__(self, init_assignments, condition, statement_list, assignments):
        self.init_assignments: List[AssigNode] = init_assignments
        self.increment_assignments = assignments
        self.condition = condition
        self.statement_list = statement_list
        
#----------------------------------------------------------------------Create-Statments-----------------------------------------------------------------------------#

        
class LetNode(StatmentNode):
    def __init__(self, assigments: List[AssigNode]) -> None:
        self.assigments = assigments

class AttributeDefinitionNode(Node):
    def __init__(self, identifier, type_annotation, expression):
        self.identifier = identifier
        self.type_annotation = type_annotation
        self.expression = expression
        
class ArgNode(Node):
    def __init__(self, id, type) -> None:
        self.id = id
        self.type_definition = type
        
class FunctionDefinitionNode(StatmentNode):
    def __init__(self, identifier, type_anotation, parameters: List[ArgNode], statement_list):
        self.identifier = identifier
        self.type_anotation = type_anotation
        self.parameters = parameters
        self.statement_list = statement_list

class TypeDefinitionNode(StatmentNode):
    def __init__(self, identifier, inheritance, attribute_definition: List[AttributeDefinitionNode], method_definition: List[FunctionDefinitionNode]):
        self.identifier = identifier
        self.inheritance = inheritance
        self.attribute_definition = attribute_definition
        self.method_definition = method_definition

# class AssignmentNode(StatmentNode):
#     def __init__(self, identifiers, expressions):
#         self.identifiers = identifiers
#         self.expressions = expressions
        
class InstanceCreationNode(StatmentNode):
    def __init__(self, identifier, type, arguments):
        self.identifier = identifier
        self.type = type
        self.arguments = arguments
        
#--------------------------------------------------------------------------------------------------------------------------------------------------------------#        
        
class TypeNode(Node):
    def __init__(self, type) :
        self.type_name = type
        
class Expression(Node):
    pass
        
class BooleanExpression(Node):
    def __init__(self, expression, operator, expresion_2) -> None:
        self.expression = expression
        self.operator = operator
        self.expression_2 = expresion_2
    
class NotConditionNode(Node):
    def __init__(self, condition) -> None:
        self.condition = condition
        
class ConditionsCollectionNode(Node):
    def __init__(self, conditions, operators) -> None:
        self.conditions = conditions
        self.operators = operators
        
class IsNode(Node):
    def __init__(self, expression, type) -> None:
        self.expression = expression
        self.type = type

class FunctionCallNode(AtomicNode):
    def __init__(self, identifier, arguments):
        self.identifier = identifier
        self.arguments = arguments
        
class AritmeticExpressions(BinaryNode):
    def __init__(self, left, right, operator):
        super().__init__(left, right)
        self.operator = operator

class MemberAccesNode(Node):
    def __init__(self, identifier, member):
        self.identifier = identifier # can be a function
        self.member = member

class InheritanceNode(Node):
    def __init__(self, identifier):
        self.identifier = identifier

class MethodOverrideNode(Node):
    def __init__(self, identifier, parameters, expression):
        self.identifier = identifier
        self.parameters = parameters
        self.expression = expression
        
class VariableNode(AtomicNode):
    def __init__(self, lex):
        super().__init__(lex)
        self.identifier = lex
        
class NumberNode(UnaryNode):
    def __init__(self, token, node):
        super().__init__(token, node)
        
