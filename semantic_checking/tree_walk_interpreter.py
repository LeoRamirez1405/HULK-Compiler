import math
import random
import visitor
from AST import *
from semantic import *

class TreeWalkInterpreter():
    
    def __init__(self):
        self.context = Context()
        self.errors = []
    
    @visitor.on('node')
    def visit(self, node, tabs):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode):
        for statement in node.statements:
            self.visit(statement)

    @visitor.when(PrintStatmentNode)
    def visit(self, node: PrintStatmentNode):
        value = self.visit(node.expression)
        print(value)

    @visitor.when(IfStructureNode)
    def visit(self, node: IfStructureNode):
        condition = self.visit(node.condition)
        if condition:
            self.visit(node.body)
        elif node._elif:
            for elif_node in node._elif:
                elif_condition = self.visit(elif_node.condition)
                if elif_condition:
                    self.visit(elif_node.body)
                    break
            else:
                if node._else:
                    self.visit(node._else.body)
        else:
            if node._else:
                self.visit(node._else.body)


    @visitor.when(WhileStructureNode)
    def visit(self, node: WhileStructureNode):
        while self.visit(node.condition):
            self.visit(node.body)

    @visitor.when(ForStructureNode)
    def visit(self, node: ForStructureNode):
        for init_assignment in node.init_assigments:
            self.visit(init_assignment)
        while self.visit(node.condition):
            self.visit(node.body)
            for increment_assignment in node.increment_condition:
                self.visit(increment_assignment)
        #NO LO TENGO CLARO

    @visitor.when(BoolIsTypeNode)
    def visit(self, node: BoolIsTypeNode):
        value = self.visit(node.expression)
        return isinstance(value, node.type)

    @visitor.when(BoolAndNode)
    def visit(self, node: BoolAndNode):
        left_value = self.visit(node.left)
        right_value = self.visit(node.right)
        return left_value and right_value

    @visitor.when(BoolOrNode)
    def visit(self, node: BoolOrNode):
        left_value = self.visit(node.left)
        right_value = self.visit(node.right)
        return left_value or right_value

    @visitor.when(BoolNotNode)
    def visit(self, node: BoolNotNode):
        value = self.visit(node.expression)
        return not value
    
    @visitor.when(BoolCompLessNode)
    def visit(self, node: BoolCompLessNode):
        left_value = self.visit(node.left)
        right_value = self.visit(node.right)
        return left_value < right_value

    @visitor.when(BoolCompGreaterNode)
    def visit(self, node: BoolCompGreaterNode):
        left_value = self.visit(node.left)
        right_value = self.visit(node.right)
        return left_value > right_value
    
    @visitor.when(BoolCompLessEqualNode)
    def visit(self, node: BoolCompLessEqualNode):
        left_value = self.visit(node.left)
        right_value = self.visit(node.right)
        return left_value <= right_value

    @visitor.when(BoolCompGreaterEqualNode)
    def visit(self, node: BoolCompGreaterEqualNode):
        left_value = self.visit(node.left)
        right_value = self.visit(node.right)
        return left_value >= right_value

    @visitor.when(BoolCompEqualNode)
    def visit(self, node: BoolCompEqualNode):
        left_value = self.visit(node.left)
        right_value = self.visit(node.right)
        return left_value == right_value

    @visitor.when(BoolCompNotEqualNode)
    def visit(self, node: BoolCompNotEqualNode):
        left_value = self.visit(node.left)
        right_value = self.visit(node.right)
        return left_value != right_value
    
    @visitor.when(PlusExpressionNode)
    def visit(self, node: PlusExpressionNode):
        left_value = self.visit(node.left)
        right_value = self.visit(node.right)
        return left_value + right_value

    @visitor.when(SubsExpressionNode)
    def visit(self, node: SubsExpressionNode):
        left_value = self.visit(node.left)
        right_value = self.visit(node.right)
        return left_value - right_value

    @visitor.when(DivExpressionNode)
    def visit(self, node: DivExpressionNode):
        left_value = self.visit(node.left)
        right_value = self.visit(node.right)
        return left_value / right_value

    @visitor.when(MultExpressionNode)
    def visit(self, node: MultExpressionNode):
        left_value = self.visit(node.left)
        right_value = self.visit(node.right)
        return left_value * right_value

    @visitor.when(ModExpressionNode)
    def visit(self, node: ModExpressionNode):
        left_value = self.visit(node.left)
        right_value = self.visit(node.right)
        return left_value % right_value

    @visitor.when(PowExpressionNode)
    def visit(self, node: PowExpressionNode):
        left_value = self.visit(node.left)
        right_value = self.visit(node.right)
        return left_value ** right_value

    @visitor.when(SqrtMathNode)
    def visit(self, node: SqrtMathNode):
        expression_value = self.visit(node.expression)
        return math.sqrt(expression_value)

    @visitor.when(SinMathNode)
    def visit(self, node: SinMathNode):
        expression_value = self.visit(node.expression)
        return math.sin(expression_value)

    @visitor.when(CosMathNode)
    def visit(self, node: CosMathNode):
        expression_value = self.visit(node.expression)
        return math.cos(expression_value)

    @visitor.when(TanMathNode)
    def visit(self, node: TanMathNode):
        expression_value = self.visit(node.expression)
        return math.tan(expression_value)

    @visitor.when(ExpMathNode)
    def visit(self, node: ExpMathNode):
        expression_value = self.visit(node.expression)
        return math.exp(expression_value)

    @visitor.when(RandomCallNode)
    def visit(self, node: RandomCallNode):
        return random.random()

    @visitor.when(LogCallNode)
    def visit(self, node: LogCallNode):
        base_value = self.visit(node.base)
        expression_value = self.visit(node.expression)
    
    @visitor.when(StringConcatNode)
    def visit(self, node: StringConcatNode):
        left_value = self.visit(node.left)
        right_value = self.visit(node.right)
        return str(left_value) + str(right_value)

    @visitor.when(StringConcatWithSpaceNode)
    def visit(self, node: StringConcatWithSpaceNode):
        left_value = self.visit(node.left)
        right_value = self.visit(node.right)
        return str(left_value) + " " + str(right_value)

# from typing import List

# class Node():
#     pass
        
# class AtomicNode(Node):
#     def __init__(self, lex):
#         self.lex = lex

# class UnaryNode(Node):
#     def __init__(self, node):
#         self.node = node

#     def evaluate(self):
#         value = self.node.evaluate()
#         return self.operate(value)

#     @staticmethod
#     def operate(value):
#         raise NotImplementedError()

# class BinaryNode(Node):
#     def __init__(self, left, right):
#         self.left = left
#         self.right = right

#     def evaluate(self):
#         lvalue = self.left.evaluate()
#         rvalue = self.right.evaluate()
#         return self.operate(lvalue, rvalue)

#     @staticmethod
#     def operate(lvalue, rvalue):
#         raise NotImplementedError()
    
# #-------------------------------------------------------------------------------------------------------------------------------------------------#
# class ProgramNode(Node):
#     def __init__(self, statments) -> None:
#         super().__init__()
#         self.statments = statments
             
# class PrintStatmentNode(Node):
#     def __init__(self, expression) -> None:
#         super().__init__()
#         self.expression = expression
        
# class KernAssigmentNode(Node):
#     def __init__(self, id, expression) -> None:
#         super().__init__()
#         self.id = id
#         self.expression = expression
        
# class DestroyNode(KernAssigmentNode):
#     def __init__(self, id, expression) -> None:
#         super().__init__(id, expression)
        
# class LetNode(KernAssigmentNode):
#     def __init__(self, id, expression) -> None:
#         super().__init__(id, expression)
        
# # TODO Podriamos instanciar la clase Type
# class TypeNode(Node):
#     def __init__(self, type) -> None:
#         super().__init__()
#         self.type = type
        
# class FunctionDefinitionNode(Node):
#     def __init__(self, id, type_annotation, parameters:list[dict], body) -> None:
#         super().__init__()
#         self.id = id
#         self.type_annotation = type_annotation
#         self.parameters = parameters
#         self.body = body
        
# #--------------------------------Non_Create-Statment-----------------------------------------------------------------------------------------------------------------------#
        
# class IfStructureNode(Node):
#     def __init__(self, condition, body, _elif, _else) -> None:
#         super().__init__()
#         self.condition = condition
#         self.body = body
#         self._elif = _elif
#         self._else = _else
        
# class ElifStructureNode(Node):
#     def __init__(self, condition, body) -> None:
#         super().__init__()
#         self.condition = condition
#         self.body = body

# class ElseStructureNode(Node):
#     def __init__(self, body) -> None:
#         super().__init__()
#         self.body = body
        
# class WhileStructureNode(Node):
#     def __init__(self, condition, body) -> None:
#         super().__init__()
#         self.condition = condition
#         self.body = body

# class ForStructureNode(Node):
#     def __init__(self, init_assigments: List[LetNode], condition, increment_assigment: List[KernAssigmentNode], body) -> None:
#         super().__init__() 
#         self.init_assigments = init_assigments
#         self.condition = condition
#         self.increment_condition = increment_assigment
#         self.body = body
        
# #-----------------------------------Class----------------------------------------------------------------------------------------------#
# class TypeDefinitionNode(Node):
#     def __init__(self, id, parameters:list[dict],inheritance, attributes: List[LetNode], methods) -> None:
#         super().__init__()
#         self.id = id
#         self.parameters = parameters
#         self.inheritance = inheritance
#         self.attribute: List[LetNode] = attributes
#         self.methods = methods
        
# # Esto debe recibir un type annotation?
# # class MethodDefinitionNode(Node):
# #     def __init__(self, id, parameters, body) -> None:
# #         super().__init__()
# #         self.id = id
# #         self.parameters = parameters
# #         self.body = body
        
# class InheritanceNode(Node):
#     def __init__(self, type) -> None:
#         super().__init__()
#         self.type = type
        
# #? Verificar si son necesarios tanto InstanceCreation node como KernInstanceCreationNode 
# #* R/ Aca se verifica si es valido la reacion de la variable por el id y el KernInstance creation se usa en caso de que se quiera parasar como parametro a alguna funcion
# #*         la creacion de una instancia de una clase
# class InstanceCreationNode(Node):
#     def __init__(self, id, type, arguments) -> None:
#         super().__init__()
#         self.id = id
#         self.type = type
#         self.arguments = arguments

# #TODO Verificar que son los parametros type y args
# class KernInstanceCreationNode(BinaryNode):
#     def __init__(self, type, args):
#         super().__init__(type, args)
#         self.type = type
#         self.args = args
        
# #TODO Ver bien que en que consiste el member acces
# class MemberAccesNode(Node):
#     def __init__(self, base_object, object_property_to_acces, args) -> None:
#         super().__init__()
#         self.base_object = base_object
#         self.object_property_to_acces = object_property_to_acces
#         self.args = args
        
# #! No son necesarios los operadores
# #------------------------------------Operators----------------------------------------------------------------------------------------------------#       
# class BooleanOperator(Node):
#     def __init__(self, operator) -> None:
#         super().__init__()
#         self.operator = operator
        
# class AritmeticOperator(Node):
#     def __init__(self, operator) -> None:
#         super().__init__()
#         self.operator = operator
        
# class ConcatOperator(Node):
#     def __init__(self, operator) -> None:
#         super().__init__()
#         self.operator = operator
        
# #-------------------------------------------Abstrct-Expressions------------------------------------------------------------------------------------------#
# class BooleanExpression(BinaryNode):
#     def __init__(self, expression_1, expression_2) -> None:
#         super().__init__(expression_1, expression_2)
#         # self.expression_1 = expression_1
#         # self.expressiin_2 = expression_2
        
# class AritmeticExpression(Node):
#     def __init__(self, expression_1, expression_2) -> None:
#         super().__init__()
#         self.expression_1 = expression_1
#         self.expression_2 = expression_2
        
# #-------------------------------Aritmetic-Expressions-------------------------------------------------------------------------------------------------#
# class PlusExpressionNode(AritmeticExpression):
#     def __init__(self, expression_1, expresion_2) -> None:
#         super().__init__(expression_1, expresion_2)
#         self.expression_1 = expression_1
#         self.expression_2 = expresion_2
        
# class SubsExpressionNode(AritmeticExpression):
#     def __init__(self, expression_1, expresion_2) -> None:
#         super().__init__(expression_1, expresion_2)
#         self.expression_1 = expression_1
#         self.expression_2 = expresion_2
        
# class DivExpressionNode(AritmeticExpression):
#     def __init__(self, expression_1, expresion_2) -> None:
#         super().__init__(expression_1, expresion_2)
#         self.expression_1 = expression_1
#         self.expression_2 = expresion_2
        
# class MultExpressionNode(AritmeticExpression):
#     def __init__(self, expression_1, expresion_2) -> None:
#         super().__init__(expression_1, expresion_2)
#         self.expression_1 = expression_1
#         self.expression_2 = expresion_2
# class ModExpressionNode(AritmeticExpression):
#     def __init__(self, expression_1, expresion_2) -> None:
#         super().__init__(expression_1, expresion_2)
#         self.expression_1 = expression_1
#         self.expression_2 = expresion_2

# class PowExpressionNode(AritmeticExpression):
#     def __init__(self, expression_1, expresion_2) -> None:
#         super().__init__(expression_1, expresion_2)
#         self.expression_1 = expression_1
#         self.expression_2 = expresion_2
        
# class LetInExpressionNode(Node):
#     def init(self, assigments, body) -> None:
#         super().init()
#         self.assigments = assigments
#         self.body = body        
# #------------------------------------------------------------Math-Operations-----------------------------------------------------------------------------------#
# class MathOperationNode(UnaryNode):
#     def __init__(self, expression) -> None:
#         super().__init__(expression)
#         self.expression = expression

# class SqrtMathNode(MathOperationNode):
#     def __init__(self, expression) -> None:
#         super().__init__(expression)
#         self.expression = expression
        
# class SinMathNode(MathOperationNode):
#     def __init__(self, expression) -> None:
#         super().__init__(expression)
#         self.expression = expression
        
# class CosMathNode(MathOperationNode):
#     def __init__(self, expression) -> None:
#         super().__init__(expression)
#         self.expression = expression
        
# class TanMathNode(MathOperationNode):
#     def __init__(self, expression) -> None:
#         super().__init__(expression)
#         self.expression = expression

# class ExpMathNode(MathOperationNode):
#     def __init__(self, expression) -> None:
#         super().__init__(expression)
#         self.expression = expression

# class RandomCallNode(Node):
#     def __init__(self) -> None:
#         super().__init__()
        
# class LogCallNode(Node):
#     def __init__(self, base, expression) -> None:
#         super().__init__()
#         self.base = base
#         self.expression = expression

# #-----------------------------------Let-In--------------------------------------------------------------------------------------------------------------------#
# class LetInNode(Node):
#     def __init__(self, assigments, body) -> None:
#         super().__init__()
#         self.assigments = assigments
#         self.body = body

# #----------------------------------Factor-Nodes----------------------------------------------------------------------------------------------------------------#
# class FunctionCallNode(Node):
#     def __init__(self, id, args) -> None:
#         super().__init__()
#         self.id = id
#         self.args = args

# class BooleanNode(Node):
#     def __init__(self, value) -> None:
#         super().__init__()
#         self.value = value

# class NumberNode(Node):
#     def __init__(self, value) -> None:
#         super().__init__()
#         self.value = value
        
# class StringNode(Node):
#     def __init__(self, value) -> None:
#         super().__init__()
#         self.value = value
        
# class IdentifierNode(Node):
#     def __init__(self) -> None:
#         super().__init__()
        
# class StringConcatNode(BinaryNode):
#     def __init__(self, left, right):
#         super().__init__(left, right)
#         # self.left = left
#         # self.right = right
        
# class StringConcatWithSpaceNode(StringConcatNode):
#     def __init__(self, left, right):
#         super().__init__(left, right)
#         # self.left = left
#         # self.right = right
        
# #TODO Ver que es esto
# class BoolIsTypeNode(BinaryNode):
#     def __init__(self, expression, type):
#         super().__init__(expression, type)
#         self.expression = expression
#         self.type = type
        
# class BoolAndNode(BooleanExpression):
#     def __init__(self, expression_1, expression_2) -> None:
#         super().__init__(expression_1, expression_2)
#     # def __init__(self, left, right):
#     #     super().__init__(left, right)
#     #     self.left = left
#     #     self.right = right
        
# class BoolOrNode(BooleanExpression):
#     def __init__(self, expression_1, expression_2) -> None:
#         super().__init__(expression_1, expression_2)
#     # def __init__(self, left, right):
#     #     super().__init__(left, right)
#     #     self.left = left
#     #     self.right = right
        
# class BoolCompAritNode(BinaryNode):
#     def __init__(self, left, right):
#         super().__init__(left, right)
#         # self.left = left
#         # self.right = right
        
# class BoolNotNode(UnaryNode):
#     def __init__(self, node):
#         super().__init__(node)
#         # self.node = node
        
# class BoolCompLessNode(BoolCompAritNode):
#     def __init__(self, left, right):
#         super().__init__(left, right)
#     # def __init__(self, left, right):
#     #     super().__init__(left, right)
#     #     self.left = left
#     #     self.right = right
             
# class BoolCompGreaterNode(BoolCompAritNode):
#     def __init__(self, left, right):
#         super().__init__(left, right)
#     # def __init__(self, left, right):
#     #     super().__init__(left, right)
#     #     self.left = left
#     #     self.right = right
        
# class BoolCompEqualNode(BoolCompAritNode):
#     def __init__(self, left, right):
#         super().__init__(left, right)
#     # def __init__(self, left, right):
#     #     super().__init__(left, right)
#     #     self.left = left
#     #     self.right = right
        
# class BoolCompLessEqualNode(BoolCompAritNode):
#     def __init__(self, left, right):
#         super().__init__(left, right)
#         # self.left = left
#         # self.right = right
        
# class BoolCompGreaterEqualNode(BoolCompAritNode):
#     def __init__(self, left, right):
#         super().__init__(left, right)
#         # self.left = left
#         # self.right = right
        
# class BoolCompNotEqualNode(BoolCompAritNode):
#     def __init__(self, left, right):
#         super().__init__(left, right)
#         # self.left = left
#         # self.right = right
        
