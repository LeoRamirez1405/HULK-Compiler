from typing import List
import math

class Node():
    pass
        
class AtomicNode(Node):
    def __init__(self, lex):
        self.lex = lex

class UnaryNode(Node):
    def __init__(self, node):
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
    
#-------------------------------------------------------------------------------------------------------------------------------------------------#
class ProgramNode(Node):
    def __init__(self, statments) -> None:
        super().__init__()
        self.statments = statments
        
class IdentifierNode(Node):
    def __init__(self, id) -> None:
        super().__init__()
        self.id : str = id
             
class PrintStatmentNode(Node):
    def __init__(self, expression) -> None:
        super().__init__()
        self.expression = expression
        
#TODO creo que se deberia poner el type_annotation en el kern_assigment
class KernAssigmentNode(Node):
    def __init__(self, id, expression) -> None:
        super().__init__()
        self.id = id
        self.expression = expression
        
class DestroyNode(KernAssigmentNode):
    def __init__(self, id, expression) -> None:
        super().__init__(id, expression)
        
# class LetNode(KernAssigmentNode):
#     def __init__(self, id, expression) -> None:
#         super().__init__(id, expression)
        
#? Podriamos instanciar la clase Type
#* Eso se hace luego cuando se viita el nodo en el visitor
class TypeNode(Node):
    def __init__(self, type) -> None:
        super().__init__()
        self.type = type
        
class FunctionDefinitionNode(Node):
    def __init__(self, id: IdentifierNode, type_annotation: TypeNode, parameters:list[dict[IdentifierNode, TypeNode]], body) -> None:
        super().__init__()
        self.id: IdentifierNode = id
        self.type_annotation = type_annotation
        self.parameters = parameters
        self.body = body
        
#--------------------------------Non_Create-Statment-----------------------------------------------------------------------------------------------------------------------#
        
class IfStructureNode(Node):
    def __init__(self, condition, body, _elif, _else) -> None:
        super().__init__()
        self.condition = condition
        self.body = body
        self._elif = _elif
        self._else = _else
        
class ElifStructureNode(Node):
    def __init__(self, condition, body) -> None:
        super().__init__()
        self.condition = condition
        self.body = body

class ElseStructureNode(Node):
    def __init__(self, body) -> None:
        super().__init__()
        self.body = body
        
class WhileStructureNode(Node):
    def __init__(self, condition, body) -> None:
        super().__init__()
        self.condition = condition
        self.body = body

class ForStructureNode(Node):
    def __init__(self, init_assigments: List[KernAssigmentNode], condition, increment_assigment: List[KernAssigmentNode], body) -> None:
        super().__init__() 
        self.init_assigments = init_assigments
        self.condition = condition
        self.increment_condition = increment_assigment
        self.body = body
        
#-----------------------------------Class----------------------------------------------------------------------------------------------#
class TypeDefinitionNode(Node):
    def __init__(self, id, parameters:list[dict],inheritance, attributes: List[KernAssigmentNode], methods) -> None:
        super().__init__()
        self.id = id
        self.parameters = parameters
        self.inheritance: InheritanceNode = inheritance
        self.attributes: List[KernAssigmentNode] = attributes
        self.methods = methods
        
class InheritanceNode(Node):
    def __init__(self, type) -> None:
        super().__init__()
        self.type : IdentifierNode = type

#? Verificar que son los parametros type y args
#* En new type (args = [param_1, param_2, ...])
class KernInstanceCreationNode(BinaryNode):
    def __init__(self, type, args):
        super().__init__(type, args)
        self.type = type
        self.args = args
        
#? Ver bien que en que consiste el member acces
#* x.method_name(parametro_1, parametro_2, ...)
class MemberAccessNode(Node):
    def __init__(self, base_object, object_property_to_acces, args) -> None:
        super().__init__()
        self.base_object = base_object
        self.object_property_to_acces = object_property_to_acces
        self.args = args
        
#! No son necesarios los operadores
#------------------------------------Operators----------------------------------------------------------------------------------------------------#       
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
        
#-------------------------------------------Abstrct-Expressions------------------------------------------------------------------------------------------#
class BooleanExpression(BinaryNode):
    def __init__(self, expression_1, expression_2) -> None:
        super().__init__(expression_1, expression_2)
        # self.expression_1 = expression_1
        # self.expressiin_2 = expression_2
        
class AritmeticExpression(Node):
    def __init__(self, expression_1, expression_2) -> None:
        super().__init__()
        self.expression_1 = expression_1
        self.expression_2 = expression_2
        
#-------------------------------Aritmetic-Expressions-------------------------------------------------------------------------------------------------#
class PlusExpressionNode(AritmeticExpression):
    def __init__(self, expression_1, expresion_2) -> None:
        super().__init__(expression_1, expresion_2)
        
class SubsExpressionNode(AritmeticExpression):
    def __init__(self, expression_1, expresion_2) -> None:
        super().__init__(expression_1, expresion_2)
        self.expression_1 = expression_1
        
class DivExpressionNode(AritmeticExpression):
    def __init__(self, expression_1, expresion_2) -> None:
        super().__init__(expression_1, expresion_2)
        
class MultExpressionNode(AritmeticExpression):
    def __init__(self, expression_1, expresion_2) -> None:
        super().__init__(expression_1, expresion_2)
class ModExpressionNode(AritmeticExpression):
    def __init__(self, expression_1, expresion_2) -> None:
        super().__init__(expression_1, expresion_2)
class PowExpressionNode(AritmeticExpression):
    def __init__(self, expression_1, expresion_2) -> None:
        super().__init__(expression_1, expresion_2)
           
class NumberNode(Node):
    def __init__(self, value) -> None:
        super().__init__()
        self.value = value
class PINode(NumberNode):
    def __init__(self) -> None:
        super().__init__(math.pi)
    
#------------------------------------------------------------Math-Operations-----------------------------------------------------------------------------------#
class MathOperationNode(UnaryNode):
    def __init__(self, expression) -> None:
        super().__init__(expression)

class SqrtMathNode(MathOperationNode):
    def __init__(self, expression) -> None:
        super().__init__(expression)
        
class SinMathNode(MathOperationNode):
    def __init__(self, expression) -> None:
        super().__init__(expression)
        
class CosMathNode(MathOperationNode):
    def __init__(self, expression) -> None:
        super().__init__(expression)
        
class TanMathNode(MathOperationNode):
    def __init__(self, expression) -> None:
        super().__init__(expression)
        self.expression = expression

class ExpMathNode(MathOperationNode):
    def __init__(self, expression) -> None:
        super().__init__(expression)

#-----------------------------------Let-In--------------------------------------------------------------------------------------------------------------------#
class LetInNode(Node):
    def __init__(self, assigments, body) -> None:
        super().__init__()
        self.assigments = assigments
        self.body = body
        
class LetInExpressionNode(Node):
    def __init__(self, assigments, body) -> None:
        super().__init__()
        self.assigments = assigments
        self.body = body 

#----------------------------------Factor-Nodes----------------------------------------------------------------------------------------------------------------#
class FunctionCallNode(Node):
    def __init__(self, id, args) -> None:
        super().__init__()
        self.id = id
        self.args = args

class BooleanNode(Node):
    def __init__(self, value) -> None:
        super().__init__()
        self.value = value
        
class StringNode(Node):
    def __init__(self, value) -> None:
        super().__init__()
        self.value = value
        
class StringConcatNode(BinaryNode):
    def __init__(self, left, right):
        super().__init__(left, right)
        
class StringConcatWithSpaceNode(StringConcatNode):
    def __init__(self, left, right):
        super().__init__(left, right)
        
#TODO Ver que es esto
class BoolIsTypeNode(BinaryNode):
    def __init__(self, expression, type):
        super().__init__(expression, type)
        # self.expression = expression
        # self.type = type
        
class BoolAndNode(BooleanExpression):
    def __init__(self, expression_1, expression_2) -> None:
        super().__init__(expression_1, expression_2)
        
class BoolOrNode(BooleanExpression):
    def __init__(self, expression_1, expression_2) -> None:
        super().__init__(expression_1, expression_2)

class BoolCompAritNode(BinaryNode):
    def __init__(self, left, right):
        super().__init__(left, right)
        
class BoolNotNode(UnaryNode):
    def __init__(self, node):
        super().__init__(node)        
class BoolCompLessNode(BoolCompAritNode):
    def __init__(self, left, right):
        super().__init__(left, right)
             
class BoolCompGreaterNode(BoolCompAritNode):
    def __init__(self, left, right):
        super().__init__(left, right)
        
class BoolCompEqualNode(BoolCompAritNode):
    def __init__(self, left, right):
        super().__init__(left, right)
        
class BoolCompLessEqualNode(BoolCompAritNode):
    def __init__(self, left, right):
        super().__init__(left, right)
        
class BoolCompGreaterEqualNode(BoolCompAritNode):
    def __init__(self, left, right):
        super().__init__(left, right)
        
class BoolCompNotEqualNode(BoolCompAritNode):
    def __init__(self, left, right):
        super().__init__(left, right)
        
#------------------------------------------------Default-Functions-----------------------------------------------------------------------#
# class DefaultFunctionCallNode(FunctionCallNode):
#     def __init__(self, id, args) -> None:
#         super().__init__(id, args)
        
# class SinFunctionCallNode(DefaultFunctionCallNode):
#     def __init__(self, id, args) -> None:
#         super().__init__(id, args)
        
# class CosFunctionCallNode(DefaultFunctionCallNode):
#     def __init__(self, id, args) -> None:
#         super().__init__(id, args)
        
# class TanFunctionCallNode(DefaultFunctionCallNode):
#     def __init__(self, id, args) -> None:
#         super().__init__(id, args)
        
# class RandomFunctionCallNode(DefaultFunctionCallNode):
#     def __init__(self, id, args) -> None:
#         super().__init__(id, args)
        
# class LogFunctionCallNode(DefaultFunctionCallNode):
#     def __init__(self, id, args) -> None:
#         super().__init__(id, args)

class RandomFunctionCallNode(Node):
    def __init__(self) -> None:
        super().__init__()
        
class LogFunctionCallNode(Node):
    def __init__(self, base, expression) -> None:
        super().__init__()
        self.base = base
        self.expression = expression