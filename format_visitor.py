import cmp.visitor as visitor
from semantic_checking.AST import *

class FormatVisitor(object):
    @visitor.on('node')
    def visit(self, node, tabs = 0):
        pass
    
    @visitor.when(ProgramNode)
    def visit(self, node : ProgramNode, tabs=0):
        ans = '\t' * tabs + f'\\__ProgramNode [<class> ... <class>]'
        statements = '\n'.join(self.visit(child, tabs + 1) for child in node.statments)
        return '\t' * tabs + f'{ans}\n{statements}'
    

    @visitor.when(PrintStatmentNode)
    def visit(self, node : PrintStatmentNode, tabs=0):
        ans = '\t' * tabs + f'\\__PrintStatmentNode'
        expression = self.visit(node.expression, tabs + 1)
        return '\t' * tabs + f'{ans}\n{expression}'
    
    @visitor.when(KernAssigmentNode)
    def visit(self, node : KernAssigmentNode, tabs=0):
        ans = '\t' * tabs + f'\\__KernAssigmentNode'
        id = self.visit(node.id, tabs + 1)
        expression = self.visit(node.expression, tabs + 1)
        return '\t' * tabs + f'{ans}\n{id}\n{expression}'
    
    @visitor.when(DestroyNode)
    def visit(self, node : DestroyNode, tabs=0):
        ans = '\t' * tabs + f'\\__DestroyNode'
        id = self.visit(node.id, tabs + 1)
        expression = self.visit(node.expression, tabs + 1)
        return '\t' * tabs + f'{ans}\n{id}\n{expression}'
    
    @visitor.when(TypeNode)
    def visit(self, node: TypeNode, tabs = 0 ):
       return '\t' * tabs + f'\\__TypeNode [{node.type}]'

    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode, tabs = 0):
        ans = f'\\__ProgramNode [{len(node.statments)} statements]'
        statements = '\n'.join(self.visit(child, tabs + 1) for child in node.statments)
        return '\t' * tabs + f'{ans}\n{statements}'

    @visitor.when(PrintStatmentNode)
    def visit(self, node: PrintStatmentNode, tabs = 0):
        expression = self.visit(node.expression, tabs + 1)
        return '\t' * tabs + f'\\__PrintStatmentNode\n{expression}'

    @visitor.when(KernAssigmentNode)
    def visit(self, node: KernAssigmentNode, tabs = 0):
        id = self.visit(node.id, tabs + 1)
        expression = self.visit(node.expression, tabs + 1)
        return '\t' * tabs + f'\\__KernAssigmentNode\n{id}\n{expression}'

    @visitor.when(DestroyNode)
    def visit(self, node: DestroyNode, tabs = 0):
        id = self.visit(node.id, tabs + 1)
        expression = self.visit(node.expression, tabs + 1)
        return '\t' * tabs + f'\\__DestroyNode\n{id}\n{expression}'

    @visitor.when(FunctionDefinitionNode)
    def visit(self, node: FunctionDefinitionNode, tabs = 0):
        params = ', '.join(f'{param["id"]} : {self.visit(param["type_annotation"], tabs + 1)}' for param in node.parameters)
        body = self.visit(node.body, tabs + 1)
        return '\t' * tabs + f'\\__FunctionDefinitionNode\n\\____ID: {node.id}\n\\____Parameters: {params}\n\\____Body:\n{body}'

    @visitor.when(IfStructureNode)
    def visit(self, node: IfStructureNode, tabs = 0):
        condition = self.visit(node.condition, tabs + 1)
        body = self.visit(node.body, tabs + 1)
        _elif = self.visit(node._elif, tabs + 1) if node._elif else ''
        _else = self.visit(node._else, tabs + 1) if node._else else ''
        return '\t' * tabs + f'\\__IfStructureNode\n\\____Condition:\n{condition}\n\\____Body:\n{body}\n\\____Elif:\n{_elif}\n\\____Else:\n{_else}'

    @visitor.when(ElifStructureNode)
    def visit(self, node: ElifStructureNode, tabs = 0):
        condition = self.visit(node.condition, tabs + 1)
        body = self.visit(node.body, tabs + 1)
        return '\t' * tabs + f'\\__ElifStructureNode\n\\____Condition:\n{condition}\n\\____Body:\n{body}'

    @visitor.when(ElseStructureNode)
    def visit(self, node: ElseStructureNode, tabs = 0):
        body = self.visit(node.body, tabs + 1)
        return '\t' * tabs + f'\\__ElseStructureNode\n\\____Body:\n{body}'

    @visitor.when(WhileStructureNode)
    def visit(self, node: WhileStructureNode, tabs = 0):
        condition = self.visit(node.condition, tabs + 1)
        body = self.visit(node.body, tabs + 1)
        return '\t' * tabs + f'\\__WhileStructureNode\n\\____Condition:\n{condition}\n\\____Body:\n{body}'

    @visitor.when(ForStructureNode)
    def visit(self, node: ForStructureNode, tabs = 0):
        init_assigments = '\n'.join(self.visit(assigment, tabs + 1)  for assigment in node.init_assigments)
        condition = self.visit(node.condition, tabs + 1)
        increment_assigment = '\n'.join(self.visit(assigment, tabs + 1) for assigment in node.increment_assigment)
        body = self.visit(node.body, tabs + 1)
        return '\t' * tabs + f'\\__ForStructureNode\n\\____Init Assigments:\n{init_assigments}\n\\____Condition:\n{condition}\n\\____Increment Assigment:\n{increment_assigment}\n\\____Body:\n{body}'

    @visitor.when(TypeDefinitionNode)
    def visit(self, node: TypeDefinitionNode, tabs = 0):
        id = self.visit(node.id, tabs + 1)
        parameters = ', '.join(f'{param["id"]} : {self.visit(param["type_annotation"], tabs + 1)}' for param in node.parameters)
        attributes = '\n'.join(self.visit(attr, tabs + 1) for attr in node.attributes)
        methods = '\n'.join(self.visit(method, tabs + 1) for method in node.methods)
        return '\t' * tabs + f'\\__TypeDefinitionNode\n\\____ID: {id}\n\\____Parameters: {parameters}\n\\____Attributes:\n{attributes}\n\\____Methods:\n{methods}'

    @visitor.when(InheritanceNode)
    def visit(self, node: InheritanceNode, tabs = 0):
        parent = self.visit(node.type, tabs + 1)
        return '\t' * tabs + f'\\__InheritanceNode\n\\____Parent: {parent}'

    @visitor.when(KernInstanceCreationNode)
    def visit(self, node: KernInstanceCreationNode, tabs = 0):
        id = self.visit(node.type, tabs + 1)
        return '\t' * tabs + f'\\__KernInstanceCreationNode\n\\____ID: {id}'

    @visitor.when(MemberAccessNode)
    def visit(self, node: MemberAccessNode, tabs = 0):
        obj = self.visit(node.base_object, tabs + 1)
        member = self.visit(node.args, tabs + 1)
        return '\t' * tabs + f'\\__MemberAccessNode\n\\____Object:\n{obj}\n\\____Member:\n{member}'

    @visitor.when(PlusExpressionNode)
    def visit(self, node: PlusExpressionNode, tabs = 0):
        expression_1 = self.visit(node.expression_1, tabs + 1)
        expression_2 = self.visit(node.expression_2, tabs + 1)
        return '\t' * tabs + f'\\__PlusExpressionNode\n' + '\t' * tabs + f'\\____expression_1:\n{expression_1}\n' + '\t' * tabs + f'\\____expression_2:\n{expression_2}'

    @visitor.when(SubsExpressionNode)
    def visit(self, node: SubsExpressionNode, tabs = 0):
        expression_1 = self.visit(node.expression_1, tabs + 1)
        expression_2 = self.visit(node.expression_2, tabs + 1)
        return '\t' * tabs + f'\\__SubsExpressionNode\n' + '\t' * tabs + f'\\____expression_1:\n{expression_1}\n' + '\t' * tabs + f'\\____expression_2:\n{expression_2}'

    @visitor.when(DivExpressionNode)
    def visit(self, node: DivExpressionNode, tabs = 0):
        expression_1 = self.visit(node.expression_1, tabs + 1)
        expression_2 = self.visit(node.expression_2, tabs + 1)
        return '\t' * tabs + f'\\__DivExpressionNode\n' + '\t' * tabs + f'\\____expression_1:\n{expression_1}\n' + '\t' * tabs + f'\\____expression_2:\n{expression_2}'

    @visitor.when(MultExpressionNode)
    def visit(self, node: MultExpressionNode, tabs = 0):
        expression_1 = self.visit(node.expression_1, tabs + 1)
        expression_2 = self.visit(node.expression_2, tabs + 1)
        return '\t' * tabs + f'\\__MultExpressionNode\n' + '\t' * tabs + f'\\____expression_1:\n{expression_1}\n' + '\t' * tabs + f'\\____expression_2:\n{expression_2}'

    @visitor.when(ModExpressionNode)
    def visit(self, node: ModExpressionNode, tabs = 0):
        expression_1 = self.visit(node.expression_1, tabs + 1)
        expression_2 = self.visit(node.expression_2, tabs + 1)
        return '\t' * tabs + f'\\__ModExpressionNode\n' + '\t' * tabs + f'\\____expression_1:\n{expression_1}\n' + '\t' * tabs + f'\\____expression_2:\n{expression_2}'

    @visitor.when(PowExpressionNode)
    def visit(self, node: PowExpressionNode, tabs = 0):
        expression_1 = self.visit(node.expression_1, tabs + 1)
        expression_2 = self.visit(node.expression_2, tabs + 1)
        return '\t' * tabs + f'\\__PowExpressionNode\n' + '\t' * tabs + f'\\____expression_1:\n{expression_1}\n' + '\t' * tabs + f'\\____expression_2:\n{expression_2}'

    @visitor.when(NumberNode)
    def visit(self, node: NumberNode, tabs = 0):
        return '\t' * tabs + f'\\__NumberNode [{node.value}]'

    @visitor.when(PINode)
    def visit(self, node: PINode , tabs = 0  ):
        return '\t' * tabs + '\\__PINode'

    @visitor.when(SqrtMathNode)
    def visit(self, node: SqrtMathNode, tabs = 0):
        expression = self.visit(node.expression, tabs + 1)
        return '\t' * tabs + f'\\__SqrtMathNode\n{expression}'

    @visitor.when(SinMathNode)
    def visit(self, node: SinMathNode, tabs = 0):
        expression = self.visit(node.expression, tabs + 1)
        return '\t' * tabs + f'\\__SinMathNode\n{expression}'

    @visitor.when(CosMathNode)
    def visit(self, node: CosMathNode, tabs = 0):
        expression = self.visit(node.expression, tabs + 1)
        return '\t' * tabs + f'\\__CosMathNode\n{expression}'

    @visitor.when(TanMathNode)
    def visit(self, node: TanMathNode, tabs = 0):
        expression = self.visit(node.expression, tabs + 1)
        return '\t' * tabs + f'\\__TanMathNode\n{expression}'

    @visitor.when(ExpMathNode)
    def visit(self, node: ExpMathNode, tabs = 0):
        expression = self.visit(node.expression, tabs + 1)
        return '\t' * tabs + f'\\__ExpMathNode\n{expression}'

    @visitor.when(RandomCallNode)
    def visit(self, node: RandomCallNode, tabs = 0):
        return '\t' * tabs + '\\__RandomCallNode'

    @visitor.when(LogCallNode)
    def visit(self, node: LogCallNode, tabs = 0):
        expression = self.visit(node.expression, tabs + 1)
        return '\t' * tabs + f'\\__LogCallNode\n{expression}'


    
    


# from typing import List
# import math

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
#     def __init__(self, expression_1, expression_2):
#         self.expression_1 = expression_1
#         self.expression_2 = right

#     def evaluate(self):
#         lvalue = self.expression_1.evaluate()
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
        
# #TODO creo que se deberia poner el type_annotation en el kern_assigment
# class KernAssigmentNode(Node):
#     def __init__(self, id, expression) -> None:
#         super().__init__()
#         self.id = id
#         self.expression = expression
        
# class DestroyNode(KernAssigmentNode):
#     def __init__(self, id, expression) -> None:
#         super().__init__(id, expression)
        
# # class LetNode(KernAssigmentNode):
# #     def __init__(self, id, expression) -> None:
# #         super().__init__(id, expression)
        
# #? Podriamos instanciar la clase Type
# #* Eso se hace luego cuando se viita el nodo en el visitor
# class TypeNode(Node):
#     def __init__(self, type) -> None:
#         super().__init__()
#         self.type = type
        
# class FunctionDefinitionNode(Node):
#     def __init__(self, id, type_annotation: TypeNode, parameters:list[dict], body) -> None:
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
#     def __init__(self, init_assigments: List[KernAssigmentNode], condition, increment_assigment: List[KernAssigmentNode], body) -> None:
#         super().__init__() 
#         self.init_assigments = init_assigments
#         self.condition = condition
#         self.increment_condition = increment_assigment
#         self.body = body
        
# #-----------------------------------Class----------------------------------------------------------------------------------------------#
# class TypeDefinitionNode(Node):
#     def __init__(self, id, parameters:list[dict],inheritance, attributes: List[KernAssigmentNode], methods) -> None:
#         super().__init__()
#         self.id = id
#         self.parameters = parameters
#         self.inheritance = inheritance
#         self.attributes: List[KernAssigmentNode] = attributes
#         self.methods = methods
        
# class InheritanceNode(Node):
#     def __init__(self, type) -> None:
#         super().__init__()
#         self.type = type

# #? Verificar que son los parametros type y args
# #* En new type (args = [param_1, param_2, ...])
# class KernInstanceCreationNode(BinaryNode):
#     def __init__(self, type, args):
#         super().__init__(type, args)
#         self.type = type
#         self.args = args
        
# #? Ver bien que en que consiste el member acces
# #* x.method_name(parametro_1, parametro_2, ...)
# class MemberAccessNode(Node):
#     def __init__(self, base_object, object_property_to_acces, args) -> None:
#         super().__init__()
#         self.base_object = base_object
#         self.object_property_to_acces = object_property_to_acces
#         self.args = args
        
# #! No son necesarios los operadores
# #------------------------------------Operators----------------------------------------------------------------------------------------------------#       
# # class BooleanOperator(Node):
# #     def __init__(self, operator) -> None:
# #         super().__init__()
# #         self.operator = operator
        
# # class AritmeticOperator(Node):
# #     def __init__(self, operator) -> None:
# #         super().__init__()
# #         self.operator = operator
        
# # class ConcatOperator(Node):
# #     def __init__(self, operator) -> None:
# #         super().__init__()
# #         self.operator = operator
        
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
        
# class SubsExpressionNode(AritmeticExpression):
#     def __init__(self, expression_1, expresion_2) -> None:
#         super().__init__(expression_1, expresion_2)
#         self.expression_1 = expression_1
        
# class DivExpressionNode(AritmeticExpression):
#     def __init__(self, expression_1, expresion_2) -> None:
#         super().__init__(expression_1, expresion_2)
        
# class MultExpressionNode(AritmeticExpression):
#     def __init__(self, expression_1, expresion_2) -> None:
#         super().__init__(expression_1, expresion_2)
# class ModExpressionNode(AritmeticExpression):
#     def __init__(self, expression_1, expresion_2) -> None:
#         super().__init__(expression_1, expresion_2)
# class PowExpressionNode(AritmeticExpression):
#     def __init__(self, expression_1, expresion_2) -> None:
#         super().__init__(expression_1, expresion_2)
           
# class NumberNode(Node):
#     def __init__(self, value) -> None:
#         super().__init__()
#         self.value = value
# class PINode(NumberNode):
#     def __init__(self) -> None:
#         super().__init__(math.pi)
    
# #------------------------------------------------------------Math-Operations-----------------------------------------------------------------------------------#
# class MathOperationNode(UnaryNode):
#     def __init__(self, expression) -> None:
#         super().__init__(expression)
#         self.expression = expression

# class SqrtMathNode(MathOperationNode):
#     def __init__(self, expression) -> None:
#         super().__init__(expression)
        
# class SinMathNode(MathOperationNode):
#     def __init__(self, expression) -> None:
#         super().__init__(expression)
        
# class CosMathNode(MathOperationNode):
#     def __init__(self, expression) -> None:
#         super().__init__(expression)
        
# class TanMathNode(MathOperationNode):
#     def __init__(self, expression) -> None:
#         super().__init__(expression)
#         self.expression = expression

# class ExpMathNode(MathOperationNode):
#     def __init__(self, expression) -> None:
#         super().__init__(expression)
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
        
# class LetInExpressionNode(Node):
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
        
# class StringNode(Node):
#     def __init__(self, value) -> None:
#         super().__init__()
#         self.value = value
        
# class IdentifierNode(Node):
#     def __init__(self,id) -> None:
#         super().__init__()
#         self.id = id
        
# class StringConcatNode(BinaryNode):
#     def __init__(self, expression_1, right):
#         super().__init__(expression_1, right)
        
# class StringConcatWithSpaceNode(StringConcatNode):
#     def __init__(self, expression_1, right):
#         super().__init__(expression_1, right)
        
# #TODO Ver que es esto
# class BoolIsTypeNode(BinaryNode):
#     def __init__(self, expression, type):
#         super().__init__(expression, type)
#         self.expression = expression
#         self.type = type
        
# class BoolAndNode(BooleanExpression):
#     def __init__(self, expression_1, expression_2) -> None:
#         super().__init__(expression_1, expression_2)
        
# class BoolOrNode(BooleanExpression):
#     def __init__(self, expression_1, expression_2) -> None:
#         super().__init__(expression_1, expression_2)

# class BoolCompAritNode(BinaryNode):
#     def __init__(self, expression_1, right):
#         super().__init__(expression_1, right)
        
# class BoolNotNode(UnaryNode):
#     def __init__(self, node):
#         super().__init__(node)        
# class BoolCompLessNode(BoolCompAritNode):
#     def __init__(self, expression_1, right):
#         super().__init__(expression_1, right)
             
# class BoolCompGreaterNode(BoolCompAritNode):
#     def __init__(self, expression_1, right):
#         super().__init__(expression_1, right)
        
# class BoolCompEqualNode(BoolCompAritNode):
#     def __init__(self, expression_1, right):
#         super().__init__(expression_1, right)
        
# class BoolCompLessEqualNode(BoolCompAritNode):
#     def __init__(self, expression_1, right):
#         super().__init__(expression_1, right)
        
# class BoolCompGreaterEqualNode(BoolCompAritNode):
#     def __init__(self, expression_1, right):
#         super().__init__(expression_1, right)
        
# class BoolCompNotEqualNode(BoolCompAritNode):
#     def __init__(self, expression_1, right):
#         super().__init__(expression_1, right)
        