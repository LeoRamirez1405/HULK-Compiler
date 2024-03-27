from abc import ABC
from typing import List

from semantic_checking.Token import Token

class Node(ABC):
    def __init__(self, token):
        self.token: Token = token
        
class AtomicNode(Node):
    def __init__(self, token, lex):
        super().__init__(token)
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
    def __init__(self,token, left, right):
        super().__init__(token)
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
    def __init__(self, token):
        super().__init__(token)

class ProgramNode(Node):
    def __init__(self, statement_list):
        super().__init__(Token('','',(0,0)))
        self.statement_list = statement_list # : List[StatmentNode]
        
#------------------------------------------------------------------------Non-Create-statments----------------------------------------------------------------------#
class PrintStatementNode(StatmentNode):
    def  __init__(self, token, expression):
        super().__init__(token)
        self.expression = expression
        
class IfStructureNode(StatmentNode):
    def __init__(self,token, condition, statement_list, contElif, contElse):
        super().__init__(token)
        self.condition = condition
        self.statement_list = statement_list
        self.contElif = contElif
        self.contElse = contElse
        
class WhileStructureNode(StatmentNode):
    def __init__(self,token, condition, statement_list):
        super().__init__(token)
        self.condition = condition
        self.statement_list = statement_list
        
class AssigNode(Node):
    def __init__(self,token, id, type, expression) -> None:
        super().__init__(token)
        self.id = id
        self.type = type
        self.expression = expression
        
class ForStructureNode(StatmentNode):
    def __init__(self,token, init_assignments, condition, statement_list, assignments):
        super().__init__(token)
        self.init_assignments: List[AssigNode] = init_assignments
        self.increment_assignments = assignments
        self.condition = condition
        self.statement_list = statement_list
        
#----------------------------------------------------------------------Create-Statments-----------------------------------------------------------------------------#

        
class LetNode(StatmentNode):
    def __init__(self,token, assigments: List[AssigNode]) -> None:
        super().__init__(token)
        self.assigments = assigments

class AttributeDefinitionNode(Node):
    def __init__(self,token, identifier, type_annotation, expression):
        super().__init__(token)
        self.identifier = identifier
        self.type_annotation = type_annotation
        self.expression = expression
        
class ArgNode(Node):
    def __init__(self,token, id, type) -> None:
        super().__init__(token)
        self.id = id
        self.type_definition = type
        
class FunctionDefinitionNode(StatmentNode):
    def __init__(self,token, identifier, type_anotation, parameters: List[ArgNode], statement_list):
        super().__init__(token)
        self.identifier = identifier
        self.type_anotation = type_anotation
        self.parameters = parameters
        self.statement_list = statement_list
        
# class TypeDefinitionNode():
#     def __init__(self, identifier, inheritance, attribute_definition: List[AttributeDefinitionNode], method_definition: List[FunctionDefinitionNode]):
#         self.identifier = identifier
#         self.inheritance = inheritance
#         self.attribute_definition = attribute_definition
#         self.method_definition = method_definition

class TypeDefinitionNode(StatmentNode):
    def __init__(self,token, identifier, inheritance, attribute_definition: List[AttributeDefinitionNode], method_definition: List[FunctionDefinitionNode]):
        super().__init__(token)
        self.identifier = identifier
        self.inheritance = inheritance
        self.attribute_definition = attribute_definition
        self.method_definition = method_definition

# class AssignmentNode(StatmentNode):
#     def __init__(self, identifiers, expressions):
#         self.identifiers = identifiers
#         self.expressions = expressions
        
class InstanceCreationNode(StatmentNode):
    def __init__(self,token, identifier, type, arguments):
        super().__init__(token)
        self.identifier = identifier
        self.type = type
        self.arguments = arguments
        
#--------------------------------------------------------------------------------------------------------------------------------------------------------------#        
        
class TypeNode(Node):
    def __init__(self, token, type) :
        super().__init__(token)
        self.type_name = type
        
class Expression(Node):
    pass
        
class BooleanExpression(Node):
    def __init__(self, token, expression, operator, expresion_2) -> None:
        super().__init__(token)
        self.expression = expression
        self.operator = operator
        self.expression_2 = expresion_2
    
class NotConditionNode(Node):
    def __init__(self, token, condition) -> None:
        super().__init__(token)
        self.condition = condition
        
class ConditionsCollectionNode(Node):
    def __init__(self, token, conditions, operators) -> None:
        super().__init__(token)
        self.conditions = conditions
        self.operators = operators
        
class IsNode(Node):
    def __init__(self, token, expression, type) -> None:
        super().__init__(token)
        self.expression = expression
        self.type = type

class FunctionCallNode(AtomicNode):
    def __init__(self, token, identifier, arguments):
        super().__init__(token)
        self.identifier = identifier
        self.arguments = arguments
        
class AritmeticExpressions(BinaryNode):
    def __init__(self, left, right, operator):
        super().__init__(left, right)
        self.operator = operator

class MemberAccesNode(Node):
    def __init__(self, token, identifier, member):
        super().__init__(token)
        self.identifier = identifier # can be a function
        self.member = member

class InheritanceNode(Node):
    def __init__(self, token, identifier):
        super().__init__(token)
        self.identifier = identifier

class MethodOverrideNode(Node):
    def __init__(self, token, identifier, parameters, expression):
        super().__init__(token)
        self.identifier = identifier
        self.parameters = parameters
        self.expression = expression
        
class VariableNode(AtomicNode):
    def __init__(self, lex):
        super().__init__(lex)
        self.identifier = lex
        
class NumberNode(StatmentNode):
    def __init__(self, token, node):
        super().__init__(token)
        self.node = node
        
class BooleanNode(Node):
    def __init__(self, value, token):
        super().__init__(token)
        self.value = value
        