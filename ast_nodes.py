class Node:
    def evaluate(self):
        raise NotImplementedError()

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

class ProgramNode(Node):
    def __init__(self, statement_list):
        self.statement_list = statement_list

class PrintStatementNode(Node):
    def __init__(self, expression):
        self.expression = expression

class AssignmentNode(Node):
    def __init__(self, identifier, expression):
        self.identifier = identifier
        self.expression = expression

class FunctionDefinitionNode(Node):
    def __init__(self, identifier, parameters, expression):
        self.identifier = identifier
        self.parameters = parameters
        self.expression = expression

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
    def __init__(self, assignment, condition, statement_list):
        self.assignment = assignment
        self.condition = condition
        self.statement_list = statement_list

class TypeDefinitionNode(Node):
    def __init__(self, identifier, attribute_definition, method_definition, inheritance):
        self.identifier = identifier
        self.attribute_definition = attribute_definition
        self.method_definition = method_definition
        self.inheritance = inheritance

class MemberAccessNode(Node):
    def __init__(self, identifier, member):
        self.identifier = identifier
        self.member = member

class TypeDefinitionNode(Node):
    def __init__(self, identifier, attribute_definition, method_definition, inheritance):
        self.identifier = identifier
        self.attribute_definition = attribute_definition
        self.method_definition = method_definition
        self.inheritance = inheritance

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

class InstanceCreationNode(Node):
    def __init__(self, identifier, arguments, statement_list):
        self.identifier = identifier
        self.arguments = arguments
        self.statement_list = statement_list

class MethodOverrideNode(Node):
    def __init__(self, identifier, parameters, expression):
        self.identifier = identifier
        self.parameters = parameters
        self.expression = expression
