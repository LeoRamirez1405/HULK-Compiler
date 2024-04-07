from typing import List
import math

from cmp.utils import Token

class Node():
    def __init__(self, token: Token = None):
        self.location = token.location if token is not None else None
        pass
        
class AtomicNode(Node):
    def init(self, lex, token):
        super().__init__(token)
        self.lex = lex

class UnaryNode(Node):
    def __init__(self, node, token : Token):
        super().__init__(token)
        self.node = node

    def evaluate(self):
        value = self.node.evaluate()
        return self.operate(value)

    @staticmethod
    def operate(value):
        raise NotImplementedError()

class BinaryNode(Node):
    def __init__(self, left, right, token):
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
    
#-------------------------------------------------------------------------------------------------------------------------------------------------#
class ProgramNode(Node):
    def __init__(self, statments, token = None) -> None:
        super().__init__(token)
        self.statments = statments
        
class IdentifierNode(Node):
    def __init__(self, tokenID : Token) -> None:
        super().__init__(tokenID)
        self.id = tokenID.lex
        print(f"Identifier: {id}")

           
class SelfNode(Node):
    def __init__(self, identifier, token) -> None:
        super().__init__(token)
        self.identifier = identifier             
        self.id : str = id
        
class SelfNode(Node):
    def __init__(self, id : IdentifierNode, token) -> None:
        super().__init__(token)
        self.identifier: IdentifierNode = id
        self.id : str = id

class PrintStatmentNode(Node):
    def __init__(self, expression, tokenPrint : Token) -> None:
        super().__init__(tokenPrint)
        self.expression = expression
        
#TODO creo que se deberia poner el type_annotation en el kern_assigment
class KernAssigmentNode(Node):
    def __init__(self, id, expression, token : Token) -> None:
        super().__init__(token)
        self.id : IdentifierNode = id
        self.expression = expression
        
class DestroyNode(Node):
    def __init__(self, id, expression, tokenDestroy : Token) -> None:
        super().__init__(tokenDestroy)
        self.id : IdentifierNode = id
        self.expression = expression
        
# class LetNode(KernAssigmentNode):
#     def __init__(self, id, expression) -> None:
#         super().__init__(id, expression)
        
#? Podriamos instanciar la clase Type
#* Eso se hace luego cuando se viita el nodo en el visitor
class TypeNode(Node):
    def __init__(self, type) -> None:
        super().__init__()
        self.type = type.lex
        if type != 'object':
            self.location = type.location
        
class FunctionDefinitionNode(Node):
    def __init__(self, id: IdentifierNode, type_annotation: TypeNode, parameters:list[dict[IdentifierNode, TypeNode]], body) -> None:
        super().__init__(id)
        self.id: IdentifierNode = id
        self.type_annotation = type_annotation
        self.parameters = parameters
        self.body = body
        
#--------------------------------Non_Create-Statment-----------------------------------------------------------------------------------------------------------------------#
        
class IfStructureNode(Node):
    def __init__(self, condition, body, _elif, _else, tokenIf : Token) -> None:
        super().__init__(tokenIf)
        self.condition = condition
        self.body = body
        self._elif = _elif
        self._else = _else
        
class ElifStructureNode(Node):
    def __init__(self, tokenElif : Token, condition, body) -> None:
        super().__init__(tokenElif)
        self.condition = condition
        self.body = body
        
    def __len__(self):
        return len(self.body)
    
class ElseStructureNode(Node):
    def __init__(self, body, tokenElse : Token = None) -> None:
        super().__init__(tokenElse)
        self.body = body

    def __len__(self):
        return len(self.body)

        
class WhileStructureNode(Node):
    def __init__(self, condition, body, tokenWhile : Token) -> None:
        super().__init__(tokenWhile)
        self.condition = condition
        self.body = body

class ForStructureNode(Node):
    def __init__(self, init_assigments: List[KernAssigmentNode], condition, increment_assigment: List[KernAssigmentNode], body, tokenFor : Token) -> None:
        super().__init__(tokenFor) 
        self.init_assigments = init_assigments
        self.condition = condition
        self.increment_condition = increment_assigment
        self.body = body
        
#-----------------------------------Class----------------------------------------------------------------------------------------------#
class TypeDefinitionNode(Node):
    def __init__(self, id : IdentifierNode, parameters:list[dict],inheritance, attributes: List[KernAssigmentNode], methods) -> None:
        super().__init__()
        self.id = id
        self.location = id.location
        self.parameters = parameters
        self.inheritance: InheritanceNode = inheritance
        self.attributes: List[KernAssigmentNode] = attributes
        self.methods = methods
        
class InheritanceNode(Node):
    def __init__(self, type : IdentifierNode, args) -> None:
        super().__init__()
        self.type : IdentifierNode = type
        self.args: list[dict[IdentifierNode, TypeNode]] = args
        self.location = type.location

#? Verificar que son los parametros type y args
#* En new type (args = [param_1, param_2, ...])
class KernInstanceCreationNode(BinaryNode):
    def __init__(self, type : IdentifierNode, args):
        super().__init__(type, args)
        self.type = type
        self.args = args
        self.location = type.location
        
#? Ver bien que en que consiste el member acces
#* x.method_name(parametro_1, parametro_2, ...)
class MemberAccessNode(Node):
    def __init__(self, base_object, object_property_to_acces : IdentifierNode, args) -> None:
        super().__init__()
        self.base_object = base_object
        self.object_property_to_acces = object_property_to_acces
        self.args = args
        self.location = object_property_to_acces.location
        
#! No son necesarios los operadores
#------------------------------------Operators----------------------------------------------------------------------------------------------------#       
# class BooleanOperator(Node):
#     def __init__(self, operator) -> None:
#               super().__init__(token)
#         self.operator = operator
        
# class AritmeticOperator(Node):
#     def __init__(self, operator) -> None:
#               super().__init__(token)
#         self.operator = operator
        
# class ConcatOperator(Node):
#     def __init__(self, operator) -> None:
#               super().__init__(token)
#         self.operator = operator
        
#-------------------------------------------Abstrct-Expressions------------------------------------------------------------------------------------------#
class BooleanExpression(BinaryNode):
    def __init__(self, expression_1, expression_2, tokenBool) -> None:
        super().__init__(expression_1, expression_2, tokenBool)
        # self.expression_1 = expression_1
        # self.expressiin_2 = expression_2
        
class AritmeticExpression(Node):
    def __init__(self, expression_1, expression_2, tokenArit : Token) -> None:
        super().__init__(tokenArit)
        self.expression_1 = expression_1
        self.expression_2 = expression_2
        print(f"Ari: {expression_1}, {expression_2}")
        
#-------------------------------Aritmetic-Expressions-------------------------------------------------------------------------------------------------#
class PlusExpressionNode(AritmeticExpression):
    def __init__(self, expression_1, expresion_2, tokenArit) -> None:
        super().__init__(expression_1, expresion_2, tokenArit)
        
class SubsExpressionNode(AritmeticExpression):
    def __init__(self, expression_1, expresion_2, tokenArit) -> None:
        super().__init__(expression_1, expresion_2, tokenArit)
        self.expression_1 = expression_1
        
class DivExpressionNode(AritmeticExpression):
    def __init__(self, expression_1, expresion_2, tokenArit) -> None:
        super().__init__(expression_1, expresion_2, tokenArit)
        
class MultExpressionNode(AritmeticExpression):
    def __init__(self, expression_1, expresion_2, tokenArit) -> None:
        super().__init__(expression_1, expresion_2, tokenArit)
class ModExpressionNode(AritmeticExpression):
    def __init__(self, expression_1, expresion_2, tokenArit) -> None:
        super().__init__(expression_1, expresion_2, tokenArit)
class PowExpressionNode(AritmeticExpression):
    def __init__(self, expression_1, expresion_2, tokenArit) -> None:
        super().__init__(expression_1, expresion_2, tokenArit)

class NumberNode(Node):
    def __init__(self, value : Token) -> None:
        super().__init__(value)
        self.value = value.lex

class PINode(NumberNode):
    def __init__(self, tokenPI : Token) -> None:
        super().__init__(math.pi, tokenPI)
    
#------------------------------------------------------------Math-Operations-----------------------------------------------------------------------------------#
class MathOperationNode(UnaryNode):
    def __init__(self, expression, tokenOp : Token) -> None:
        super().__init__(expression, tokenOp)

class SqrtMathNode(MathOperationNode):
    def __init__(self, expression, token : Token) -> None:
        super().__init__(expression, token)
        
class SinMathNode(MathOperationNode):
    def __init__(self, expression, token : Token) -> None:
        super().__init__(expression, token)
        
class CosMathNode(MathOperationNode):
    def __init__(self, expression, token : Token) -> None:
        super().__init__(expression, token)
        
class TanMathNode(MathOperationNode):
    def __init__(self, expression, token : Token) -> None:
        super().__init__(expression, token)

class ExpMathNode(MathOperationNode):
    def __init__(self, expression, token : Token) -> None:
        super().__init__(expression, token)

#-----------------------------------Let-In--------------------------------------------------------------------------------------------------------------------#
class LetInNode(Node):
    def __init__(self, assigments, body) -> None:
        super().__init__()
        self.assigments = assigments
        self.body = body
        
class LetInExpressionNode(Node):
    def __init__(self, assigments, body, tokenIn : Token) -> None:
        super().__init__(tokenIn)
        self.assigments = assigments
        self.body = body 

#----------------------------------Factor-Nodes----------------------------------------------------------------------------------------------------------------#
class FunctionCallNode(Node):
    def __init__(self, tokenFunc : Token, args) -> None:
        super().__init__(tokenFunc)
        self.id = tokenFunc.lex
        self.args = args

class BooleanNode(Node):
    def __init__(self, value : Token) -> None:
        super().__init__(value)
        self.value = value.lex

        
class StringNode(Node):
    def __init__(self, value : Token) -> None:
        super().__init__(value)
        self.value = value.lex
        
class StringConcatNode(BinaryNode):
    def __init__(self, left, right, tokenBinary: Token):
        super().__init__(left, right, tokenBinary)
        
class StringConcatWithSpaceNode(StringConcatNode):
    def __init__(self, left, right, tokenConcat : Token):
        super().__init__(left, right, tokenConcat)
        
#TODO Ver que es esto
class BoolIsTypeNode(BinaryNode):
    def __init__(self, expression, type, token):
        super().__init__(expression, type, token)
        # self.expression = expression
        # self.type = type
        
class BoolAndNode(BooleanExpression):
    def __init__(self, expression_1, expression_2, tokenBool) -> None:
        super().__init__(expression_1, expression_2, tokenBool)
        
class BoolOrNode(BooleanExpression):
    def __init__(self, expression_1, expression_2, tokenBool) -> None:
        super().__init__(expression_1, expression_2, tokenBool)

class BoolCompAritNode(BinaryNode):
    def __init__(self, left, right, tokenBinary: Token):
        super().__init__(left, right, tokenBinary)
        
class BoolNotNode(UnaryNode):
    def __init__(self, node, tokenNot : Token):
        super().__init__(node, tokenNot)  
class BoolCompLessNode(BoolCompAritNode):
    def __init__(self, left, right, tokenBinary: Token):
        super().__init__(left, right, tokenBinary)

class BoolCompGreaterNode(BoolCompAritNode):
    def __init__(self, left, right, tokenBinary: Token):
        super().__init__(left, right, tokenBinary)
        
class BoolCompEqualNode(BoolCompAritNode):
    def __init__(self, left, right, tokenBinary: Token):
        super().__init__(left, right, tokenBinary)
        
class BoolCompLessEqualNode(BoolCompAritNode):
    def __init__(self, left, right, tokenBinary: Token):
        super().__init__(left, right, tokenBinary)
        
class BoolCompGreaterEqualNode(BoolCompAritNode):
    def __init__(self, left, right, tokenBinary: Token):
        super().__init__(left, right, tokenBinary)
        
class BoolCompNotEqualNode(BoolCompAritNode):
    def __init__(self, left, right, tokenBinary: Token):
        super().__init__(left, right, tokenBinary)
        
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
    def __init__(self, tokenRan : Token) -> None:
        super().__init__(tokenRan)
        
class LogFunctionCallNode(Node):
    def __init__(self, base, expression, tokenLog : Token) -> None:
        super().__init__(tokenLog)
        self.base = base
        self.expression = expression
        
class CollectionNode(Node):
    def __init__(self, collection) -> None:
        super().__init__()
        self.collection = collection