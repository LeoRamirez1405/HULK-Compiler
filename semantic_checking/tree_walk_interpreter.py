import random
from semantic_checking.semantic import *
from semantic_checking.AST import *
import semantic_checking.visitor as visitor

class TreeWalkInterpreter:

    def __init__(self):
        self.context = Context()
        self.scope = Scope()
        self.errors = []
        self.currentType: Type = None

    @visitor.on("node")
    def visit(self, node, tabs):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode):
        for statement in node.statments:
            self.visit(statement)

    @visitor.when(PrintStatmentNode)
    def visit(
        self, node: PrintStatmentNode, scope: Scope = None, Context: Context = None
    ):
        value = self.visit(node.expression)
        print(value)

    @visitor.when(NumberNode)
    def visit(self, node: NumberNode, scope: Scope = None, Context: Context = None):
        return node.value

    @visitor.when(StringNode)
    def visit(self, node: StringNode, scope: Scope = None, Context: Context = None):
        return node.value

    @visitor.when(TypeDefinitionNode)
    def visit(
        self, node: TypeDefinitionNode, scope: Scope = None, context: Context = None
    ):
        context = Context()
        self.currentType = context.create_type(node.id)
        for method in node.methods:
            self.visit(method)
        self.currentType = None

    @visitor.when(FunctionDefinitionNode)
    def visit(
        self, node: FunctionDefinitionNode, scope: Scope = None, Context: Context = None
    ):
        if self.currentType:
            try:
                self.scope.node[self.currentType.name].append(node)
            except:
                self.scope.node[self.currentType.name] = [node]
        else:
            try:
                self.scope.node[None].append(node)
            except:
                self.scope.node[None] = [node]

    @visitor.when(FunctionCallNode)
    def visit(
        self, node: FunctionCallNode, scope: Scope = None, Context: Context = None
    ):
        function = list(
            filter(
                lambda x: len(x.parameters) == len(node.args), self.scope.node[node.id]
            )
        )[0]

        for statment in function.body:
            self.visit(statment)

    @visitor.when(IfStructureNode)
    def visit(
        self, node: IfStructureNode, scope: Scope = None, Context: Context = None
    ):
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
    def visit(
        self, node: WhileStructureNode, scope: Scope = None, Context: Context = None
    ):
        while self.visit(node.condition):
            self.visit(node.body)

    @visitor.when(ForStructureNode)
    def visit(
        self, node: ForStructureNode, scope: Scope = None, Context: Context = None
    ):
        for init_assignment in node.init_assigments:
            self.visit(init_assignment)
        while self.visit(node.condition):
            self.visit(node.body)
            for increment_assignment in node.increment_condition:
                self.visit(increment_assignment)
        # NO LO TENGO CLARO

    @visitor.when(BoolIsTypeNode)
    def visit(self, node: BoolIsTypeNode, scope: Scope = None, Context: Context = None):
        value = self.visit(node.expression)
        return isinstance(value, node.type)

    @visitor.when(BoolAndNode)
    def visit(self, node: BoolAndNode, scope: Scope = None, Context: Context = None):
        left_value = self.visit(node.expression_1)
        right_value = self.visit(node.expression_2)
        return left_value and right_value

    @visitor.when(BoolOrNode)
    def visit(self, node: BoolOrNode, scope: Scope = None, Context: Context = None):
        left_value = self.visit(node.expression_1)
        right_value = self.visit(node.expression_2)
        return left_value or right_value

    @visitor.when(BoolNotNode)
    def visit(self, node: BoolNotNode):
        value = self.visit(node.expression)
        return not value

    @visitor.when(BoolCompLessNode)
    def visit(self, node: BoolCompLessNode):
        left_value = self.visit(node.expression_1)
        right_value = self.visit(node.expression_2)
        return left_value < right_value

    @visitor.when(BoolCompGreaterNode)
    def visit(self, node: BoolCompGreaterNode):
        left_value = self.visit(node.expression_1)
        right_value = self.visit(node.expression_2)
        return left_value > right_value

    @visitor.when(BoolCompLessEqualNode)
    def visit(self, node: BoolCompLessEqualNode):
        left_value = self.visit(node.expression_1)
        right_value = self.visit(node.expression_2)
        return left_value <= right_value

    @visitor.when(BoolCompGreaterEqualNode)
    def visit(self, node: BoolCompGreaterEqualNode):
        left_value = self.visit(node.expression_1)
        right_value = self.visit(node.expression_2)
        return left_value >= right_value

    @visitor.when(BoolCompEqualNode)
    def visit(self, node: BoolCompEqualNode):
        left_value = self.visit(node.expression_1)
        right_value = self.visit(node.expression_2)
        return left_value == right_value

    @visitor.when(BoolCompNotEqualNode)
    def visit(self, node: BoolCompNotEqualNode):
        left_value = self.visit(node.expression_1)
        right_value = self.visit(node.expression_2)
        return left_value != right_value

    @visitor.when(PlusExpressionNode)
    def visit(self, node: PlusExpressionNode):
        left_value = self.visit(node.expression_1)
        right_value = self.visit(node.expression_2)
        return left_value + right_value

    @visitor.when(SubsExpressionNode)
    def visit(self, node: SubsExpressionNode):
        left_value = self.visit(node.expression_1)
        right_value = self.visit(node.expression_2)
        return left_value - right_value

    @visitor.when(DivExpressionNode)
    def visit(self, node: DivExpressionNode):
        left_value = self.visit(node.expression_1)
        right_value = self.visit(node.expression_2)
        return left_value / right_value

    @visitor.when(MultExpressionNode)
    def visit(self, node: MultExpressionNode):
        left_value = self.visit(node.expression_1)
        right_value = self.visit(node.expression_2)
        return left_value * right_value

    @visitor.when(ModExpressionNode)
    def visit(self, node: ModExpressionNode):
        left_value = self.visit(node.expression_1)
        right_value = self.visit(node.expression_2)
        return left_value % right_value

    @visitor.when(PowExpressionNode)
    def visit(self, node: PowExpressionNode):
        left_value = self.visit(node.expression_1)
        right_value = self.visit(node.expression_2)
        return left_value**right_value

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
        return math.log(expression_value, base_value)

    @visitor.when(StringConcatNode)
    def visit(self, node: StringConcatNode):
        left_value = self.visit(node.expression_1)
        right_value = self.visit(node.expression_2)
        return str(left_value) + str(right_value)

    @visitor.when(StringConcatWithSpaceNode)
    def visit(self, node: StringConcatWithSpaceNode):
        left_value = self.visit(node.expression_1)
        right_value = self.visit(node.expression_2)
        return str(left_value) + " " + str(right_value)
