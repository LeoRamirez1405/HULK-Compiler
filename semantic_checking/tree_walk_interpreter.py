import random
import math
from semantic_checking.semantic import *
from semantic_checking.AST import *
import semantic_checking.visitor as visitor

class AttributeInstance:
    def __init__(self, name, type, value) -> None:
        self.name = name
        self.type = type
        self.value = value
    
class InstanceType:
    def __init__(self, type, attrs, parent = None) -> None:
        self.type = type
        self.attrs : dict[str, object] = attrs
        self.parent = parent
        
    def get_attribute_value(self, name):
        for k, v in self.attrs.items():
            if k == name:
                return v.type, v.value
        return self.parent.get_attribute_value(name) if self.parent is not None else None
    
    def set_attribute_value(self, name, value):
        try:
            self.attrs[name] = value
        except:
            return self.parent.set_attribute_value(name, value) if self.parent is not None else None
        
    def __str__(self):
        return f'{self.type}({", ".join([f"{k}: {v.value}" for k, v in self.attrs.items()])})'
    
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
        for x in self.local_variables:
            if x.name == vname:
                return x, self.var_values[x.name]
        
        return self.parent.find_variable_value(vname, self.index) if not self.parent is None else None
        
    def set_variable_value(self, vname, value, index=0):
        for x in self.local_variables:
            if x.name == vname:
                self.var_values[x.name] = value
                return
        
        return self.parent.set_variable_value(vname, value, self.index) if not self.parent is None else None
    
class TreeInterpreter:

    def __init__(self, context):
        self.context: Context = context
        self.scope = InterpreterScope()
        self.errors = []
        self.currentInstance: InstanceType = None
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
        _, value = self.visit_body(node.expression, scope)
        print(value)
        return self.context.get_type('string'), value
    
    #TODO Pendiente
    @visitor.when(IdentifierNode)
    def visit(self, node: IdentifierNode, scope: InterpreterScope):
        try:
            var, value = scope.find_variable_value(node.id)
            return var.type, value
        except:
            raise Exception(f'La variable no esta definida. location: {node.location}')

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
            raise Exception(f'El valor no es booleno. location: {node.location}')
    
    @visitor.when(KernAssigmentNode)
    def visit(self, node: KernAssigmentNode, scope: InterpreterScope):
        type, value = self.visit(node.expression, scope)
        scope.define_variable(node.id.id, type, value)
        
        return type, value
    
    @visitor.when(DestroyNode)
    def visit(self, node: DestroyNode, scope: InterpreterScope):
        type, value =  self.visit(node.expression, scope)
        scope.set_variable_value(node.id.id, value)
        
        if isinstance(node.id, SelfNode):
            self_current= AttributeInstance(node.id.id.id,type,value)
            self.currentInstance.set_attribute_value(node.id.id.id, self_current)
            
        return type, value
    
    @visitor.when(TypeNode)
    def visit(self, node: TypeNode, scope: InterpreterScope):
        try:
            type = self.context.types[node.type]
            return type, type
        except:
            raise Exception(f'El tipo {node.type} no existe')

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
        #elif len(node._else) != 0:
        return self.visit_body(node._else.body, scope)
        
        #return self.context.get_type('any'), None
            
    def visit_body(self, node, scope):
        result = self.context.get_type('any'), None
        if type(node) == list:
            for statement in node:
                aux = self.visit(statement, scope)
                result = aux if aux[1] != None else result
            return result
        return self.visit(node, scope)
            

    @visitor.when(WhileStructureNode)
    def visit(self, node: WhileStructureNode, scope: InterpreterScope):
        result = self.context.get_type('any'), None
        inner_scope = scope.create_child()
        _, condition_value = self.visit(node.condition, scope)
        while condition_value:
            result = self.visit_body(node.body, inner_scope)
            _, condition_value = self.visit(node.condition, scope)
        return result

    @visitor.when(ForStructureNode)
    def visit(self, node: ForStructureNode, scope: InterpreterScope):
        result = self.context.get_type('any'), None
        inner_scope = scope.create_child()
        self.visit(node.init_assigments, inner_scope)
        _, condition_value = self.visit(node.condition, inner_scope)
        while condition_value:
            result = self.visit_body(node.body, inner_scope)
            self.visit(node.increment_condition, inner_scope)
            _, condition_value = self.visit(node.condition, inner_scope)
        
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
        try:
            return self.context.get_type('bool'), not value
        except:
            raise Exception(f'El valor debe ser booleano. location {node.location}')

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
        try:
            return self.context.get_type('number'), left_value + right_value
        except:
            raise Exception(f'Solo se puede realizar la operacion entre numeros.')

    @visitor.when(SubsExpressionNode)
    def visit(self, node: SubsExpressionNode, scope: InterpreterScope):
        _, left_value = self.visit(node.expression_1, scope)
        _, right_value = self.visit(node.expression_2, scope)
        try:
            return self.context.get_type('number'), left_value - right_value
        except:
            raise Exception(f'Solo se puede realizar la operacion entre numeros.')

    @visitor.when(DivExpressionNode)
    def visit(self, node: DivExpressionNode, scope: InterpreterScope):
        _, left_value = self.visit(node.expression_1, scope)
        _, right_value = self.visit(node.expression_2, scope)
        if right_value == 0:
            raise Exception(f'Se esta realizando una division entre 0. {node.location}')
        try:
            return self.context.get_type('number'), left_value / right_value
        except:
            raise Exception(f'Solo se puede realizar la operacion entre numeros.')

    @visitor.when(MultExpressionNode)
    def visit(self, node: MultExpressionNode, scope: InterpreterScope):
        _, left_value = self.visit(node.expression_1, scope)
        _, right_value = self.visit(node.expression_2, scope)
        try:
            return self.context.get_type('number'), left_value * right_value
        except:
            raise Exception(f'Solo se puede realizar la operacion entre numeros.')

    @visitor.when(ModExpressionNode)
    def visit(self, node: ModExpressionNode, scope: InterpreterScope):
        _, left_value = self.visit(node.expression_1, scope)
        _, right_value = self.visit(node.expression_2, scope)
        if right_value == 0:
            raise Exception(f'Se esta realizando una division entre 0. {node.location}')
        try:
            return self.context.get_type('number'), left_value % right_value
        except:
            raise Exception(f'Solo se puede realizar la operacion entre numeros.')

    @visitor.when(PowExpressionNode)
    def visit(self, node: PowExpressionNode, scope: InterpreterScope):
        _, left_value = self.visit(node.expression_1, scope)
        _, right_value = self.visit(node.expression_2, scope)
        try:
            return self.context.get_type('number'), left_value ** right_value
        except:
            raise Exception(f'Solo se puede realizar la operacion entre numeros.')

    @visitor.when(SqrtMathNode)
    def visit(self, node: SqrtMathNode, scope: InterpreterScope):
        _, expression_value = self.visit(node.node, scope)
        if expression_value < 0:
            raise Exception(f'Esta tratando de calcular la raiz cuadrada de unnumero negativo. {node.location}')
        return self.context.get_type('number'), math.sqrt(expression_value)

    @visitor.when(SinMathNode)
    def visit(self, node: SinMathNode, scope: InterpreterScope):
        _, expression_value = self.visit(node.node,scope)
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

    @visitor.when(PINode)
    def visit(self, node: PINode, scope: InterpreterScope):
        return self.context.get_type('number'), math.pi
        
    @visitor.when(ExpMathNode)
    def visit(self, node: ExpMathNode, scope: InterpreterScope):
        _, expression_value = self.visit(node.node, scope)
        try:
            return self.context.get_type('number'), math.exp(expression_value)
        except:
            raise Exception(f'La operacion solo se aplica a numeros. location: {node.location}')

    @visitor.when(RandomFunctionCallNode)
    def visit(self, node: RandomFunctionCallNode, scope: InterpreterScope):
        return self.context.get_type('number'), random.random()

    @visitor.when(LogFunctionCallNode)
    def visit(self, node: LogFunctionCallNode, scope: InterpreterScope):
        _, base_value = self.visit(node.base, scope)
        _, expression_value = self.visit(node.expression, scope)
        if expression_value <= 0:
            raise Exception(f'El logaritmo no esta definido para numeros menores o iguales a 0. {node.location}')
        return self.context.get_type('number'), math.log(expression_value, base_value)

    @visitor.when(StringConcatNode)
    def visit(self, node: StringConcatNode, scope: InterpreterScope):
        _, left_value = self.visit(node.left, scope)
        _, right_value = self.visit(node.right, scope)
        try:
            return self.context.get_type('string'), str(left_value) + str(right_value)
        except:
            raise Exception(f'No es posible concatenar los elementos. location : {node.location}')

    @visitor.when(StringConcatWithSpaceNode)
    def visit(self, node: StringConcatWithSpaceNode, scope: InterpreterScope):
        _, left_value = self.visit(node.left, scope)
        _, right_value = self.visit(node.right, scope)
        try:
            return self.context.get_type('string'), str(left_value) + " " + str(right_value)
        except:
            raise Exception(f'No es posible concatenar los elementos. location : {node.location}')

#_______Bloque-3________________________________________________________________________________________________________________________________________________________________________

    @visitor.when(LetInExpressionNode)
    def visit(self, node: LetInExpressionNode, scope: InterpreterScope):
        inner_scope = scope.create_child()
        self.visit(node.assigments, inner_scope)
        return self.visit_body(node.body, inner_scope)

#_______Bloque-4__________________________________________________________________________________________________________________________________________________________________//
    
    @visitor.when(FunctionDefinitionNode)
    def visit(self, node: FunctionDefinitionNode, scope: InterpreterScope):
        if self.currentType:
            try:
                type: Type = self.context.get_type(self.currentType.name)
                method_1: Method = type.get_method(node.id.id, len(node.parameters))
                method_1.body = node.body
            except:
                pass
                # self.scope.node[self.currentType.name] = [node]
        else:
            method = Method(node.id.id, [list(param.items())[0][0] for param in node.parameters], [self.context.get_type(list(param.items())[0][1].type) for param in node.parameters], node.type_annotation)
            method.body = node.body
            try:
                scope.functions[node.id.id].append(method)
            except:
                scope.functions[node.id.id] = [method]
                
    @visitor.when(FunctionCallNode)
    def visit(self, node: FunctionCallNode, scope: InterpreterScope):
        try: 
            method: Method = self.currentType.get_method(node.id.id)
        except:
            #Como ya paso por el chequeo semantico solo llega aca cuando current type es None
            method: Method = scope.get_method(node.id.id, len(node.args))
            #[func for func in scope.functions[node.id.id] if len(func.param_names) == len(node.args)][0] 
            
        inner_scope = scope.create_child()    
        for i in range(len(node.args)):
            _, value = self.visit(node.args[i], inner_scope)
            inner_scope.define_variable(method.param_names[i].id, method.param_types[i], value)
        return self.visit_body(method.body, inner_scope)
            
    @visitor.when(TypeDefinitionNode)
    def visit(self, node: TypeDefinitionNode, scope: InterpreterScope):
        self.currentType = self.context.get_type(node.id.id)
        parent_type=self.currentType.inhertance
        for attr in node.attributes:
            self.currentType.set_attribute_expression(attr.id.id, attr.expression)
        if parent_type.name != 'object':
            for attr in parent_type.attrs_expression.items():
                if not attr[0] in list(map(lambda x : x.id.id,node.attributes)):
                # if not attr[0] in list(map(lambda x : x.name,node.attributes)):
                    self.currentType.set_attribute_expression(attr[0], attr[1])
            
            
        for method in node.methods:
            meth = self.currentType.get_method(method.id.id)#!agregar los metodos del padre por shsora
            meth.body = method.body
        if parent_type.name != 'object':
            for method in parent_type.methods:
                if not method.name in list(map(lambda x : x.id.id,node.methods)):
                    current_method = Method(method.name, method.param_names,method.param_types,method.return_type)
                    current_method.body=method.body
                    self.currentType.methods.append(current_method)
        
        self.currentType = None
        
    @visitor.when(KernInstanceCreationNode)
    def visit(self, node: KernInstanceCreationNode, scope: InterpreterScope):
        type: Type = self.context.get_type(node.type.id)
        type_parent:Type=type.inhertance
        instance = {}
        inner_scope = scope.create_child()
        
        #Construir los argumentos basando el los argumentos que tienen el nodo basandose en los valores de los argumentos
        for i, arg_node in enumerate(node.args):
            type_arg, value = self.visit(arg_node, inner_scope)
            #Ver si aqui type.attributes[i].name es un Identifier o es un string
            inner_scope.define_variable(type.args[i].name, type_arg, value)
            inner_scope.define_variable(type_parent.args[i].name,type_arg, value)
            
            
        #Le pone valor a cada uno d los atributos de la instancia
        for attr_name, expression in type.attrs_expression.items():
            type_attr, value = self.visit(expression, inner_scope)
            instance[attr_name] = AttributeInstance(attr_name, type_attr, value)
            
            
        return type, InstanceType(type.name, instance)
    
    @visitor.when(InstanceType)
    def visit(self, node: InstanceType, scope: IndentationError):
        return node.type, node.attrs
    
    @visitor.when(MemberAccessNode)
    def visit(self, node: MemberAccessNode, scope: InterpreterScope):
        type_base, value = self.visit(node.base_object, scope)
        self.currentType=type_base
        self.currentInstance = value
    
        method = type_base.get_method(node.object_property_to_acces.id)
        
        inner_scope = scope.create_child()    
        for i in range(len(node.args)):
            _, value = self.visit(node.args[i], inner_scope)
            inner_scope.define_variable(method.param_names[i], method.param_types[i] , value)
        
        type_result, value_result = self.visit(method.body, inner_scope)
        self.currentType=None
        self.currentInstance = None
        return type_result, value_result
        
    @visitor.when(SelfNode)
    def visit(self, node: SelfNode, scope: InterpreterScope):
        return self.currentInstance.get_attribute_value(node.id.id)
    
    @visitor.when(InheritanceNode)
    def visit(self, node: InheritanceNode, scope):
        pass
        
    @visitor.when(BlockNode)
    def visit(self, node: BlockNode, scope: InterpreterScope):
        inner_scope = scope.create_child()
        result = self.context.get_type('any'),None
        for expression in node.list_non_create_statemnet:
            result = self.visit(expression, inner_scope)
        
        return result

    
    @visitor.when(BoolAndNode)
    def visit(self, node: BoolAndNode, scope: InterpreterScope):
        _, left = self.visit(node.left, scope)
        _, right = self.visit(node.right, scope)
        try:
            return self.context.get_type('bool'), left and right
        except:
            raise Exception(f'Las operaciones logica se realizan solo entre elementos booleanos.')
        
    @visitor.when(BoolOrNode)
    def visit(self, node: BoolOrNode, scope: InterpreterScope):
        _, left = self.visit(node.left, scope)
        _, right = self.visit(node.right, scope)
        try:
            return self.context.get_type('bool'), left or right
        except:
            raise Exception(f'Las operaciones logica se realizan solo entre elementos booleanos.')
        
        