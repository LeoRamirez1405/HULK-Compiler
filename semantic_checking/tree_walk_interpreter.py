import random
import math
from semantic_checking.semantic import *
from semantic_checking.AST import *
import semantic_checking.visitor as visitor

class InterpreterScope(Scope):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.var_values = dict()
        
    def create_child(self):
        child = InterpreterScope(self)
        self.children.append(child)
        return child

    def define_variable(self, vname, vtype, value):
        info = VariableInfo(vname, vtype)
        self.local_variables.add(info)
        self.var_values[vname] = value
        return info
    
    def find_variable_value(self, vname, index=None):
        locals = self.local_variables if index is None else itt.islice(self.local_variables, index)
        try:
            return next((x, self.var_values[x.name]) for x in locals if x.name == vname)
        except StopIteration:
            return self.parent.find_variable(vname, self.index) if not self.parent is None else None
        
    def set_variable_value(self, vname, value, index=0):
        locals = self.local_variables if index is None else itt.islice(self.local_variables, index)
        try:
            return next((x, self.var_values[x.name]) for x in locals if x.name == vname)
        except StopIteration:
            return self.parent.find_variable(vname, self.index) if not self.parent is None else None

class InterpreterMethod(Method):
    def __init__(self, name, param_names, params_types, return_type, body):
        super().__init__(name, param_names, params_types, return_type)
        self.body = body
        
class InterpreterAttribute(Attribute):
    def __init__(self, name, typex, value):
        super().__init__(name, typex)
        self.value = value
        
class TreeInterpreter:

    def __init__(self, context):
        self.context: Context = context
        self.scope = InterpreterScope()
        self.errors = []
        self.currentType: Type = None

    @visitor.on("node")
    def visit(self, node, scope):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode):
        for statement in node.statments:
            self.visit(statement, self.scope)

    @visitor.when(PrintStatmentNode)
    def visit(self, node: PrintStatmentNode, scope: InterpreterScope):
        _, value = self.visit(node.expression, scope)
        print(value)
        return self.context.get_type('string'), value
    
    #TODO Pendiente
    @visitor.when(IdentifierNode)
    def visit(self, node: IdentifierNode, scope: InterpreterScope):
        try:
            var, value = self.scope.find_variable(node.id)
            return var.type, value
        except:
            return self.context.get_type('any'), None

    @visitor.when(NumberNode)
    def visit(self, node: NumberNode, scope: InterpreterScope):
        return self.context.get_type('number'), float(node.value)

    @visitor.when(StringNode)
    def visit(self, node: StringNode, scope: InterpreterScope):
        word = node.value[1:len(node.value)-1]
        return self.context.get_type('string'), str(word)
    
    @visitor.when(BooleanNode)
    def visit(self, node: BooleanNode, scope: InterpreterScope):
        try:
            return self.context.get_type('bool'), eval(node.value)
        except:
            return self.context.get_type('any'), None
    
    @visitor.when(KernAssigmentNode)
    def visit(self, node: KernAssigmentNode, scope: InterpreterScope):
        type, value = self.visit(node.expression, scope)
        scope.define_variable(node.id.id, type, value)
        
        return type, value
    
    @visitor.when(DestroyNode)
    def visit(self, node: DestroyNode, scope: InterpreterScope):
        var, value = scope.find_variable(node.id.id)
        type, value =  self.visit(self, node.expression, scope)
        scope.var_values[var.name] = value
        
        return type, value

    @visitor.when(TypeDefinitionNode)
    def visit(self, node: TypeDefinitionNode, scope: InterpreterScope):
        pass

    @visitor.when(FunctionDefinitionNode)
    def visit(self, node: FunctionDefinitionNode, scope: InterpreterScope):
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
    def visit(self, node: FunctionCallNode, scope: InterpreterScope):
        function = list(
            filter(
                lambda x: len(x.parameters) == len(node.args), self.scope.node[node.id]
            )
        )[0]

        for statment in function.body:
            self.visit(statment)

    @visitor.when(IfStructureNode)
    def visit(self, node: IfStructureNode, scope: InterpreterScope):
        _, condition = self.visit(node.condition, scope)
        if condition:
            return self.visit_body(node.body, scope)
        elif len(node._elif) != 0:
            for elif_node in node._elif:
                _, elif_condition = self.visit(elif_node.condition, scope)
                if elif_condition:
                    return self.visit_body(elif_node.body, scope)
                
        return self.visit_body(node._else.body, scope)
            
    def visit_body(self, node, scope):
        result = self.context.get_type('any'), None
        if type(node) == list:
            for statement in node:
                result = self.visit(statement, scope)
            return result
        return self.visit(node, scope)
            

    @visitor.when(WhileStructureNode)
    def visit(self, node: WhileStructureNode, scope: InterpreterScope):
        result = self.context.get_type('any'), None
        inner_scope = scope.create_child()
        while self.visit(node.condition, scope):
            result = self.visit_body(node.body, inner_scope)
        return result

    @visitor.when(ForStructureNode)
    def visit(self, node: ForStructureNode, scope: InterpreterScope):
        result = self.context.get_type('any'), None
        inner_scope = scope.create_child()
        self.visit(node.init_assigments, inner_scope)
        while self.visit(node.condition, inner_scope):
            result = self.visit_body(node.body, inner_scope)
            self.visit(node.increment_condition, inner_scope)
        
        return result
        
    @visitor.when(CollectionNode)
    def visit(self, node: CollectionNode, scope):
        result = self.context.get_type('any'), None
        if len(node.collection) != 0:
            for statement in node.collection:
                result = self.visit(statement, scope)
        
        return result
            
    @visitor.when(BoolIsTypeNode)
    def visit(self, node: BoolIsTypeNode, scope: InterpreterScope):
        lef_type, _ = self.visit(node.left, scope)
        right_type, _ = self.visit(node.right, scope)
        return self.context.get_type('bool'), lef_type.conforms_to(right_type.name)

    @visitor.when(BoolAndNode)
    def visit(self, node: BoolAndNode, scope: InterpreterScope):
        _, left_value = self.visit(node.left, scope)
        _, right_value = self.visit(node.right, scope)
        return self.context.get_type('bool'), left_value and right_value

    @visitor.when(BoolOrNode)
    def visit(self, node: BoolOrNode, scope: InterpreterScope):
        _, left_value = self.visit(node.left, scope)
        _, right_value = self.visit(node.right, scope)
        return self.context.get_type('bool'), left_value or right_value

    @visitor.when(BoolNotNode)
    def visit(self, node: BoolNotNode, scope: InterpreterScope):
        _, value = self.visit(node.node, scope)
        return self.context.get_type('bool'), not value

    @visitor.when(BoolCompLessNode)
    def visit(self, node: BoolCompLessNode, scope: InterpreterScope):
        _, left_value = self.visit(node.left, scope)
        _, right_value = self.visit(node.right, scope)
        return self.context.get_type('bool'), left_value < right_value

    @visitor.when(BoolCompGreaterNode)
    def visit(self, node: BoolCompGreaterNode, scope: InterpreterScope):
        _, left_value = self.visit(node.left, scope)
        _, right_value = self.visit(node.right, scope)
        return self.context.get_type('bool'), left_value > right_value

    @visitor.when(BoolCompLessEqualNode)
    def visit(self, node: BoolCompLessEqualNode, scope: InterpreterScope):
        _, left_value = self.visit(node.left, scope)
        _, right_value = self.visit(node.right, scope)
        return self.context.get_type('bool'), left_value <= right_value

    @visitor.when(BoolCompGreaterEqualNode)
    def visit(self, node: BoolCompGreaterEqualNode, scope: InterpreterScope):
        _, left_value = self.visit(node.left, scope)
        _, right_value = self.visit(node.right, scope)
        return self.context.get_type('bool'), left_value >= right_value

    @visitor.when(BoolCompEqualNode)
    def visit(self, node: BoolCompEqualNode, scope: InterpreterScope):
        _, left_value = self.visit(node.left, scope)
        _, right_value = self.visit(node.right, scope)
        return self.context.get_type('bool'), left_value == right_value

    @visitor.when(BoolCompNotEqualNode)
    def visit(self, node: BoolCompNotEqualNode, scope: InterpreterScope):
        _, left_value = self.visit(node.left, scope)
        _, right_value = self.visit(node.right, scope)
        return self.context.get_type('bool'), left_value != right_value

    @visitor.when(PlusExpressionNode)
    def visit(self, node: PlusExpressionNode, scope: InterpreterScope):
        _, left_value = self.visit(node.expression_1, scope)
        _, right_value = self.visit(node.expression_2, scope)
        return self.context.get_type('number'), left_value + right_value

    @visitor.when(SubsExpressionNode)
    def visit(self, node: SubsExpressionNode, scope: InterpreterScope):
        _, left_value = self.visit(node.expression_1, scope)
        _, right_value = self.visit(node.expression_2, scope)
        return self.context.get_type('number'), left_value - right_value

    @visitor.when(DivExpressionNode)
    def visit(self, node: DivExpressionNode, scope: InterpreterScope):
        _, left_value = self.visit(node.expression_1, scope)
        _, right_value = self.visit(node.expression_2, scope)
        if right_value == 0:
            raise Exception(f'Se esta realizando una division entre 0. {node.location}')
        return self.context.get_type('number'), left_value / right_value

    @visitor.when(MultExpressionNode)
    def visit(self, node: MultExpressionNode, scope: InterpreterScope):
        _, left_value = self.visit(node.expression_1, scope)
        _, right_value = self.visit(node.expression_2, scope)
        return self.context.get_type('number'), left_value * right_value

    @visitor.when(ModExpressionNode)
    def visit(self, node: ModExpressionNode, scope: InterpreterScope):
        _, left_value = self.visit(node.expression_1, scope)
        _, right_value = self.visit(node.expression_2, scope)
        if right_value == 0:
            raise Exception(f'Se esta realizando una division entre 0. {node.location}')
        return self.context.get_type('number'), left_value % right_value

    @visitor.when(PowExpressionNode)
    def visit(self, node: PowExpressionNode, scope: InterpreterScope):
        _, left_value = self.visit(node.expression_1, scope)
        _, right_value = self.visit(node.expression_2, scope)
        return self.context.get_type('number'), left_value ** right_value

    @visitor.when(SqrtMathNode)
    def visit(self, node: SqrtMathNode, scope: InterpreterScope):
        _, expression_value = self.visit(node.node, scope)
        if expression_value < 0:
            raise Exception(f'Esta tratando de calcular la raiz cuadrada de unnumero negativo. {node.location}')
        return self.context.get_type('number'), math.sqrt(expression_value)

    @visitor.when(SinMathNode)
    def visit(self, node: SinMathNode):
        _, expression_value = self.visit(node.node)
        return self.context.get_type('number'), math.sin(expression_value)

    @visitor.when(CosMathNode)
    def visit(self, node: CosMathNode, scope: InterpreterScope):
        _, expression_value = self.visit(node.node, scope)
        return self.context.get_type('number'), math.cos(expression_value)

    @visitor.when(TanMathNode)
    def visit(self, node: TanMathNode, scope: InterpreterScope):
        _, expression_value = self.visit(node.node, scope)
        # Convert the expression value to radians if it's in degrees
        if isinstance(expression_value, (int, float)):
            expression_value = math.radians(expression_value)
        # Check if the value is within the range where tan is undefined
        if math.isclose(expression_value, math.pi / 2, rel_tol=1e-9) or math.isclose(expression_value, 3 * math.pi / 2, rel_tol=1e-9):
            raise Exception(f'La tangente no esta definida para 90 grados o multiplos de 180 grados. {node.location}')
        return self.context.get_type('number'), math.tan(expression_value)


    @visitor.when(ExpMathNode)
    def visit(self, node: ExpMathNode, scope: InterpreterScope):
        _, expression_value = self.visit(node.node, scope)
        return self.context.get_type('number'), math.exp(expression_value)

    @visitor.when(RandomFunctionCallNode)
    def visit(self, node: RandomFunctionCallNode, scope: InterpreterScope):
        return self.context.get_type('number'), random.random()

    @visitor.when(LogFunctionCallNode)
    def visit(self, node: LogFunctionCallNode, scope: InterpreterScope):
        _, base_value = self.visit(node.base)
        _, expression_value = self.visit(node.expression, scope)
        if expression_value <= 0:
            raise Exception(f'El logaritmo no esta definido para numeros menores o iguales a 0. {node.location}')
        return self.context.get_type('number'), math.log(expression_value, base_value)

    @visitor.when(StringConcatNode)
    def visit(self, node: StringConcatNode, scope: InterpreterScope):
        _, left_value = self.visit(node.left, scope)
        _, right_value = self.visit(node.right, scope)
        return self.context.get_type('string'), str(left_value) + str(right_value)

    @visitor.when(StringConcatWithSpaceNode)
    def visit(self, node: StringConcatWithSpaceNode, scope: InterpreterScope):
        _, left_value = self.visit(node.left, scope)
        _, right_value = self.visit(node.right, scope)
        return self.context.get_type('string'), str(left_value) + " " + str(right_value)
