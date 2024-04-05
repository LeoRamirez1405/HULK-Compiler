import random
from cmp.semantic import Method
import semantic_checking.visitor as visitor
from semantic_checking.AST import *
from semantic_checking.semantic import Scope, Context

class TreeWalkInterpreter:
    def __init__(self, context, scope):
        self.context = context
        self.scope = scope
        self.errors = []

    @visitor.on('node')
    def visit(self, node, scope=None):
        print(f"Pass {type(node)}")
        pass

    # Nodos de programa y declaraciones
    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode, scope=None):
        print(f"Scope: {scope}")
        result = None
        for statement in node.statments:
            result = self.visit(statement, scope)  # Utiliza el scope recibido

        return result
    
    @visitor.when(KernAssigmentNode)
    def visit(self, node: KernAssigmentNode, scope=None):
        # Evalúa la expresión del lado derecho
        value = self.visit(node.expression, scope)

        # Asigna el valor a la variable en el ámbito actual
        scope.define_variable(node.id.id, value)

        # Devuelve el valor asignado
        return value 

    @visitor.when(PrintStatmentNode)
    def visit(self, node: PrintStatmentNode, scope=None):
        # Evalúa la expresión
        value = self.visit(node.expression, scope)

        # Imprime el valor en la consola
        print(value)

        # Devuelve el valor impreso
        return value

    @visitor.when(IfStructureNode)
    def visit(self, node: IfStructureNode, scope=None):
        # Evalúa la condición
        condition_value = self.visit(node.condition, scope)

        # Crea un nuevo ámbito para el bloque if
        if_scope = Scope(parent=scope)

        # Ejecuta el bloque if si la condición es verdadera
        if condition_value:
            result = None
            for statement in node.body:
                result = self.visit(statement, if_scope)
            return result

        # Si la condición es falsa, verifica las ramas elif
        for elif_node in node._elif:
            elif_condition_value = self.visit(elif_node.condition, scope)
            if elif_condition_value:
                # Crea un nuevo ámbito para el bloque elif
                elif_scope = Scope(parent=scope)
                result = None
                for statement in elif_node.body:
                    result = self.visit(statement, elif_scope)
                return result

        # Si ninguna condición es verdadera, ejecuta el bloque else (si existe)
        if node._else:
            # Crea un nuevo ámbito para el bloque else
            else_scope = Scope(parent=scope)
            result = None
            for statement in node._else.body:
                result = self.visit(statement, else_scope)
            return result

        # Si ninguna condición es verdadera y no hay bloque else, devuelve None
        return None

    @visitor.when(WhileStructureNode)
    def visit(self, node: WhileStructureNode, scope=None):
        # Crea un nuevo ámbito para el bloque while
        while_scope = Scope(parent=scope) 

        # Ejecuta el bloque while mientras la condición sea verdadera
        result = None
        while self.visit(node.condition, while_scope):
            for statement in node.body:
                result = self.visit(statement, while_scope) 

        # Devuelve el resultado de la última expresión ejecutada en el bloque while
        return result

    @visitor.when(ForStructureNode)
    def visit(self, node: ForStructureNode, scope=None):
        # Crea un nuevo ámbito para el bloque for
        for_scope = Scope(parent=scope)

        # Ejecuta las asignaciones de inicialización
        self.visit(node.init_assigments, for_scope)

        # Ejecuta el bloque for mientras la condición sea verdadera
        result = None
        while self.visit(node.condition, for_scope):
            for statement in node.body:
                result = self.visit(statement, for_scope)
            # Ejecuta las asignaciones de incremento
            self.visit(node.increment_condition, for_scope) 

        # Devuelve el resultado de la última expresión ejecutada en el bloque for
        return result

    @visitor.when(LetInNode)
    def visit(self, node: LetInNode, scope=None):
        # Crea un nuevo ámbito para el bloque let
        let_scope = Scope(parent=scope)

        # Ejecuta las asignaciones dentro del bloque let
        for assignment in node.assigments:
            self.visit(assignment, let_scope)

        # Ejecuta el cuerpo del bloque in y devuelve el resultado de la última expresión
        result = None
        for statement in node.body:
            result = self.visit(statement, let_scope)
        return result 

    # Nodos de valores
    @visitor.when(NumberNode)
    def visit(self, node: NumberNode, scope=None):
        # Devuelve el valor numérico del nodo
        return float(node.value)

    @visitor.when(StringNode)
    def visit(self, node: StringNode, scope=None):
        # Devuelve el valor de la cadena (sin las comillas)
        return node.value[1:-1]

    @visitor.when(BooleanNode)
    def visit(self, node: BooleanNode, scope=None):
        # Devuelve el valor booleano del nodo
        return node.value  

    @visitor.when(DestroyNode)
    def visit(self, node: DestroyNode, scope=None):
        # Evalúa la expresión del lado derecho
        value = self.visit(node.expression, scope)

        # Asigna el nuevo valor a la variable en el ámbito actual
        scope.define_variable(node.id.id, value)

        # Devuelve el nuevo valor asignado
        return value

    @visitor.when(IdentifierNode)
    def visit(self, node: IdentifierNode, scope=None):
        # Busca la variable en el ámbito actual
        variable = scope.find_variable(node.id) 

        # Devuelve el valor de la variable
        return variable.type

    @visitor.when(KernInstanceCreationNode)
    def visit(self, node: KernInstanceCreationNode, scope=None):
        # Obtiene el tipo de la clase
        class_type = self.context.get_type(node.type.id)

        # Crea un nuevo ámbito para la instancia
        instance_scope = Scope(parent=scope) 

        # Asigna los argumentos a los atributos de la instancia
        for arg_name, arg_value in zip(class_type.args, node.args):
            value = self.visit(arg_value, scope) 
            instance_scope.define_variable(arg_name.name, value)

        # Devuelve el ámbito de la instancia
        return instance_scope

    @visitor.when(MemberAccessNode)
    def visit(self, node: MemberAccessNode, scope=None):
        # Evalúa el objeto base
        base_object = self.visit(node.base_object, scope)

        # Obtiene el atributo o método
        if isinstance(base_object, Scope):  # Si el objeto base es un ámbito (instancia)
            member = base_object.find_variable(node.object_property_to_acces.id)
        else:  # Si el objeto base es un tipo
            member = base_object.get_attribute(node.object_property_to_acces.id)

        # Si es un método, evalúa los argumentos y llama al método
        if isinstance(member, Method):
            # Crea un nuevo ámbito para la llamada al método
            method_scope = Scope(parent=scope) 

            # Asigna los argumentos a los parámetros del método
            for param_name, arg_value in zip(member.param_names, node.args):
                value = self.visit(arg_value, scope)
                method_scope.define_variable(param_name, value)

            # Ejecuta el cuerpo del método y devuelve el resultado
            result = None
            for statement in member.return_type:
                result = self.visit(statement, method_scope)
            return result

        # Si es un atributo, devuelve su valor
        else:
            return member.type

    @visitor.when(FunctionCallNode)
    def visit(self, node: FunctionCallNode, scope : Scope=None):
        # Obtiene la función del ámbito
        function = scope.find_functions(node.id.id)[0] 

        # Crea un nuevo ámbito para la llamada a la función
        function_scope = Scope(parent=scope) 

        # Asigna los argumentos a los parámetros de la función 
        for param_name, arg_value in zip(function.param_names, node.args):
            value = self.visit(arg_value, scope)  
            function_scope.define_variable(param_name, value) 

        # Ejecuta el cuerpo de la función y devuelve el resultado
        result = None 
        for statement in function.return_type: #TODO
            result = self.visit(statement, function_scope)  
        return result

    @visitor.when(BoolIsTypeNode)
    def visit(self, node: BoolIsTypeNode, scope=None):
        # Evalúa la expresión
        value = self.visit(node.left, scope) 
        # Obtiene el tipo
        type_ = self.visit(node.right, scope)  

        # Verifica si el valor es del tipo especificado
        return type_.conforms_to(value.name)  

    @visitor.when(BoolAndNode)
    def visit(self, node: BoolAndNode, scope=None):
        # Evalúa la expresión izquierda
        left_value = self.visit(node.left, scope) 
        # Evalúa la expresión derecha
        right_value = self.visit(node.right, scope)  

        # Realiza la operación AND y devuelve el resultado
        return left_value and right_value

    @visitor.when(BoolOrNode)
    def visit(self, node: BoolOrNode, scope=None):
        # Evalúa la expresión izquierda
        left_value = self.visit(node.left, scope) 
        # Evalúa la expresión derecha
        right_value = self.visit(node.right, scope)  

        # Realiza la operación OR y devuelve el resultado
        return left_value or right_value

    @visitor.when(BoolNotNode)
    def visit(self, node: BoolNotNode, scope=None):
        # Evalúa la expresión
        value = self.visit(node.node, scope) 

        # Realiza la operación NOT y devuelve el resultado
        return not value  
    
    @visitor.when(BoolCompAritNode)
    def visit(self, node: BoolCompAritNode, scope=None):
        # Evalúa la expresión izquierda
        left_value = self.visit(node.left, scope) 
        # Evalúa la expresión derecha 
        right_value = self.visit(node.right, scope) 

        # Realiza la comparación y devuelve el resultado
        return self.compare(node, left_value, right_value)  

    def compare(self, node, left_value, right_value):
        if isinstance(node, BoolCompLessNode):
            return left_value < right_value
        elif isinstance(node, BoolCompGreaterNode):
            return left_value > right_value
        elif isinstance(node, BoolCompEqualNode):
            return left_value == right_value
        elif isinstance(node, BoolCompLessEqualNode):
            return left_value <= right_value
        elif isinstance(node, BoolCompGreaterEqualNode):
            return left_value >= right_value
        elif isinstance(node, BoolCompNotEqualNode):
            return left_value != right_value

    @visitor.when(PlusExpressionNode)
    def visit(self, node: PlusExpressionNode, scope=None):
        # Evalúa la expresión izquierda
        left_value = self.visit(node.expression_1, scope)
        # Evalúa la expresión derecha 
        right_value = self.visit(node.expression_2, scope) 

        # Realiza la suma y devuelve el resultado
        return left_value + right_value
    
    @visitor.when(SubsExpressionNode)
    def visit(self, node: SubsExpressionNode, scope=None):
        # Evalúa la expresión izquierda
        left_value = self.visit(node.expression_1, scope)
        # Evalúa la expresión derecha 
        right_value = self.visit(node.expression_2, scope) 

        # Realiza la suma y devuelve el resultado
        return left_value - right_value

    @visitor.when(DivExpressionNode)
    def visit(self, node: DivExpressionNode, scope=None):
        # Evalúa la expresión izquierda
        left_value = self.visit(node.expression_1, scope)
        # Evalúa la expresión derecha 
        right_value = self.visit(node.expression_2, scope) 

        # Realiza la suma y devuelve el resultado
        return left_value / right_value

    @visitor.when(MultExpressionNode)
    def visit(self, node: MultExpressionNode, scope=None):
        # Evalúa la expresión izquierda
        left_value = self.visit(node.expression_1, scope)
        # Evalúa la expresión derecha 
        right_value = self.visit(node.expression_2, scope) 

        # Realiza la suma y devuelve el resultado
        return left_value * right_value

    @visitor.when(ModExpressionNode)
    def visit(self, node: ModExpressionNode, scope=None):
        # Evalúa la expresión izquierda
        left_value = self.visit(node.expression_1, scope)
        # Evalúa la expresión derecha 
        right_value = self.visit(node.expression_2, scope) 

        # Realiza la suma y devuelve el resultado
        return left_value % right_value

    @visitor.when(PowExpressionNode)
    def visit(self, node: PowExpressionNode, scope=None):
        # Evalúa la expresión izquierda
        left_value = self.visit(node.expression_1, scope)
        # Evalúa la expresión derecha 
        right_value = self.visit(node.expression_2, scope) 

        # Realiza la suma y devuelve el resultado
        return left_value ^ right_value

    @visitor.when(SqrtMathNode)
    def visit(self, node: SqrtMathNode, scope=None):
        # Evalúa la expresión
        value = self.visit(node.node, scope)

        # Calcula la raíz cuadrada y devuelve el resultado
        return math.sqrt(value) 

    @visitor.when(SinMathNode)
    def visit(self, node: SinMathNode, scope=None):
        # Evalúa la expresión
        value = self.visit(node.node, scope)

        # Calcula el seno y devuelve el resultado 
        return math.sin(value)

    @visitor.when(CosMathNode)
    def visit(self, node: CosMathNode, scope=None):
        # Evalúa la expresión
        value = self.visit(node.node, scope)

        # Calcula el coseno y devuelve el resultado
        return math.cos(value)

    @visitor.when(TanMathNode)
    def visit(self, node: TanMathNode, scope=None):
        # Evalúa la expresión
        value = self.visit(node.node, scope)

        # Calcula la tangente y devuelve el resultado
        return math.tan(value)

    @visitor.when(ExpMathNode)
    def visit(self, node: ExpMathNode, scope=None):
        # Evalúa la expresión
        value = self.visit(node.node, scope) 

        # Calcula la exponencial y devuelve el resultado
        return math.exp(value)

    @visitor.when(RandomFunctionCallNode)
    def visit(self, node: RandomFunctionCallNode, scope=None):
        # Genera un número aleatorio entre 0 y 1
        return random.random()

    @visitor.when(LogFunctionCallNode)
    def visit(self, node: LogFunctionCallNode, scope=None):
        # Evalúa la base del logaritmo
        base = self.visit(node.base, scope)
        # Evalúa la expresión del logaritmo
        value = self.visit(node.expression, scope)

        # Calcula el logaritmo y devuelve el resultado 
        return math.log(value, base)

    @visitor.when(StringConcatNode)
    def visit(self, node: StringConcatNode, scope=None):
        # Evalúa la expresión izquierda
        left_value = self.visit(node.left, scope) 
        # Evalúa la expresión derecha
        right_value = self.visit(node.right, scope) 

        # Concatena las cadenas y devuelve el resultado
        return str(left_value) + str(right_value)

    @visitor.when(StringConcatWithSpaceNode)
    def visit(self, node: StringConcatWithSpaceNode, scope=None):
        # Evalúa la expresión izquierda
        left_value = self.visit(node.left, scope)
        # Evalúa la expresión derecha
        right_value = self.visit(node.right, scope)

        # Concatena las cadenas con un espacio en medio y devuelve el resultado 
        return str(left_value) + " " + str(right_value)

    @visitor.when(CollectionNode)
    def visit(self, node: CollectionNode, scope=None):
        # Crea un nuevo ámbito para la colección
        collection_scope = Scope(parent=scope) 

        # Evalúa cada elemento de la colección
        result = None 
        for element in node.collection:
            result = self.visit(element, collection_scope) 

        # Devuelve el resultado de la última expresión
        return result  

    @visitor.when(SelfNode)
    def visit(self, node: SelfNode, scope=None):
        # Obtiene el tipo actual del ámbito
        current_type = scope.find_variable("self").type  

        # Busca el atributo en el tipo actual
        attribute = current_type.get_attribute(node.identifier.id) 

        # Devuelve el valor del atributo
        return attribute.type  

    @visitor.when(LetInExpressionNode)
    def visit(self, node: LetInExpressionNode, scope=None):
        # Crea un nuevo ámbito para el bloque let
        let_scope = Scope(parent=scope) 

        # Ejecuta las asignaciones dentro del bloque let
        for assignment in node.assigments:
            self.visit(assignment, let_scope) 

        # Evalúa el cuerpo del bloque in y devuelve el resultado
        return self.visit(node.body, let_scope)  

        