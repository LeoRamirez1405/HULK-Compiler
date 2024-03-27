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
             
class PrintStatmentNode(Node):
    def __init__(self, expression) -> None:
        super().__init__()
        self.expression = expression
        
#TODO Se debe poner el type definition en el asigment qu ecreo que en la gramatica no esta hecho y luego ponerlo aqui tambien
class KernAssigmentNode(Node):
    def __init__(self, id, expression) -> None:
        super().__init__()
        self.id = id
        self.expression = expression
        
# TODO Podriamos instanciar la clase Type
class TypeNode(Node):
    def __init__(self, type) -> None:
        super().__init__()
        self.type = type
        
class FunctionDefinitionNode(Node):
    def __init__(self, id, type_annotation, parameters, body) -> None:
        super().__init__()
        self.id = id
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
    def __init__(self, init_assigments, condition, increment_assigment, body) -> None:
        super().__init__()
        self.init_assigments = init_assigments
        self.condition = condition
        self.increment_condition = increment_assigment
        self.body = body
        
#-----------------------------------Class----------------------------------------------------------------------------------------------#
class TypeDefinitionNode(Node):
    def __init__(self, id, inheritance, attributes, methods) -> None:
        super().__init__()
        self.id = id
        self.inheritance = inheritance
        self.attribute = attributes
        self.methods = methods
        
#TODO Esto debe recibir un type annotation?
class MethodDefinitionNode(Node):
    def __init__(self, id, parameters, body) -> None:
        super().__init__()
        self.id = id
        self.parameters = parameters
        self.body = body
        
class InheritanceNode(Node):
    def __init__(self, type) -> None:
        super().__init__()
        self.type = type
        
class InstanceCreationNode(Node):
    def __init__(self, id, type, arguments) -> None:
        super().__init__()
        self.id = id
        self.type = type
        self.arguments = arguments
        
#TODO Ver bien que en que consiste el member acces
class MemberAccesNode(Node):
    def __init__(self, base_object, object_property_to_acces, args) -> None:
        super().__init__()
        self.base_object = base_object
        self.object_property_ti_acces = object_property_to_acces
        self.args = args
        
#! No son necesarios los operadores
#------------------------------------Operators----------------------------------------------------------------------------------------------------#       
class BooleanOperator(Node):
    def __init__(self, operator) -> None:
        super().__init__()
        self.operator = operator
        
class AritmeticOperator(Node):
    def __init__(self, operator) -> None:
        super().__init__()
        self.operator = operator
        
class ConcatOperator(Node):
    def __init__(self, operator) -> None:
        super().__init__()
        self.operator = operator
        
#-------------------------------------------Abstrct-Expressions------------------------------------------------------------------------------------------#
class BooleanExpression(Node):
    def __init__(self, expression_1, expression_2) -> None:
        super().__init__()
        self.expression = expression_1
        self.expressiin_2 = expression_2
        
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
        
class DivExpressionNode(AritmeticExpression):
    def __init__(self, expression_1, expresion_2) -> None:
        super().__init__(expression_1, expresion_2)
        
class MultExpressionNode(AritmeticExpression):
    def __init__(self, expression_1, expresion_2) -> None:
        super().__init__(expression_1, expresion_2)
        
class ModExpressionNode(AritmeticExpression):
    def __init__(self, expression_1, expresion_2) -> None:
        super().__init__(expression_1, expresion_2)
        
        
#------------------------------------------------------------Math-Operations-----------------------------------------------------------------------------------#
class MathOperationCallNode(Node):
    def __init__(self, operator, expression) -> None:
        super().__init__()
        self.expression = expression
        self.operator = operator
        
class RandomCallNode(Node):
    def __init__(self) -> None:
        super().__init__()
        
class LogCallNode(Node):
    def __init__(self, base, expression) -> None:
        super().__init__()
        self.base = base
        self.expression = expression

#-----------------------------------Let-In--------------------------------------------------------------------------------------------------------------------#
class LetInNode(Node):
    def __init__(self, assigments, body) -> None:
        super().__init__()
        self.assigments = assigments
        self.body = body

#----------------------------------Factor-Nodes----------------------------------------------------------------------------------------------------------------#
class FunctioncallNode(Node):
    def __init__(self) -> None:
        super().__init__()

class BooleanNode(Node):
    def __init__(self, value) -> None:
        super().__init__()
        self.value = value

class NumberNode(Node):
    def __init__(self, value) -> None:
        super().__init__()
        self.value = value
        
class StringNode(Node):
    def __init__(self, value) -> None:
        super().__init__()
        self.value = value
        
class IdentifierNode(Node):
    def __init__(self) -> None:
        super().__init__()
        
        
        

        

        

