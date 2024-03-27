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
        
# class StatmentNode(Node):
#     def __init__(self, node) -> None:
#         super().__init__()
#         self.node = node
        
# class NonCreateStatmentNode(StatmentNode):
#     def __init__(self, node) -> None:
#         super().__init__()
#         self.node = node
        
# class CreateStatmentNode(StatmentNode):
#     def __init__(self, node) -> None:
#         super().__init__()
#         self.node = node
        
class PrintStatmentNode(Node):
    def __init__(self, expression) -> None:
        super().__init__()
        self.expression = expression
        
class KernAssigmentNode(Node):
    def __init__(self, id, expression) -> None:
        super().__init__()
        self.id = id
        self.expression = expression
        
# TODO Podriamos instancias la clase Type
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

class ElseNode(Node):
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
        
class BooleanOperator(Node):
    def __init__(self, operator) -> None:
        super().__init__()
        self.operator = operator
        
class AritmeticOperator(Node):
    def __init__(self, operator) -> None:
        super().__init__()
        self.operator = operator
        
class BooleanExpression(Node):
    def __init__(self, expression) -> None:
        super().__init__()
        self.expression = expression
        
class AritmeticExpression(Node):
    def __init__(self, expression) -> None:
        super().__init__()
        self.expression = expression
        

        

        
