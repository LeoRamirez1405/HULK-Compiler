import visitor
from semantic import Context, Scope, SemanticError, Type, VariableInfo
# from semantic_checking.AST import *
from AST import *

#! Hay que ver que se hace con las funciones que no son metodos de alguna clase   OJO

class TypeCheckerVisitor:
    def __init__(self, context: Context, scope: Scope, errors, default_functions) -> None:
        self.context: Context = context
        self.errors: List[str] = errors
        self.scope: Scope = scope
        self.default_functions = default_functions
        self.current_type: Type = None
        
    @visitor.on('node')
    def visit(self, node, scope):
        pass
    
    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode):
        #print('TypeChecker')
        # print(f'Context in Checker: {[item for item in self.context.types.keys()]}')
        for statment in node.statments:
            self.visit(statment, self.scope) 
            
    @visitor.when(PrintStatmentNode)
    def visit(self, node: PrintStatmentNode, scope):
        #print('visitor en PrintNode')
        self.visit(node.expression, scope)
        
        return self.context.get_type('void')
            
    @visitor.when(DestroyNode)
    def visit(self, node: DestroyNode, scope: Scope):
        # node_id: IdentifierNode = node.id
        if not scope.is_defined(node.id.id):
            self.errors.append(SemanticError(f'La variable {node.id.id} no esta definida en este scope'))
            
        return self.visit(node.expression, scope)
        
    @visitor.when(KernAssigmentNode)
    def visit(self, node: KernAssigmentNode, scope: Scope):
        if scope.parent == None:
            try:
                var: VariableInfo = self.scope.find_variable(node.id.id)
                var.type = self.visit(node.expression, scope)
            except:
                self.errors.append(SemanticError(f'La variable {node.id.id} ya esta definida.'))
            return self.context.get_type('object')
    
        if scope.is_local(node.id.id) or scope.is_defined(node.id.id):
            self.errors.append(SemanticError(f'La variable {node.id.id} ya esta definida.'))
        else:
            scope.define_variable(node.id.id, self.visit(node.expression, scope)) #* Aqui en el 2do parametro de la funcion se infiere el tipo de la expresion que se le va a asignar a la variable
            
        return self.context.get_type('object')
    
    #* Esto se usa a la hora de definir los parametros de una funcion que se esta creando
    @visitor.when(TypeNode)
    def visit(self, node: TypeNode, scope: Scope):
        try:
            return self.context.get_type(node.type)
        except:
            self.errors.append(SemanticError(f'Tipo {node.type} no esta definido'))
            return self.context.get_type('object')
            
    @visitor.when(FunctionDefinitionNode)
    def visit(self, node: FunctionDefinitionNode, scope: Scope):
        # if node.id in self.default_functions:
        #     self.errors.append(SemanticError(f'Esta redefiniendo una funcion {node.id} que esta definida por defecto en el lenguaje y no se puede sobreescribir'))
            
        #     #* En los nodos que no son expresiones aritmeticas o booleanas o concatenacion o llamados a funciones deberia ponerle que tiene typo object?
        #     return self.context.get_type('object')
        
        # node_id: IdentifierNode = node.id
        if self.current_type:
            method = self.current_type.get_method(node.id.id)
        else:
            method = list(filter(lambda x: len(x.param_names) == len(node.parameters), self.scope.functions[node.id.id]))[0]  
                   
        inner_scope: Scope = scope.create_child()            
        for i in method.param_names:
            inner_scope.define_variable(method.param_names[i], method.param_types[i])
            
        self.visit(node.body, inner_scope)
    
        return self.context.get_type('object')
            
    @visitor.when(IfStructureNode)
    def visit(self, node: IfStructureNode, scope: Scope):
        # verifico el tipo de la condicion y a la vez veo si las variables que estan dentro de ella estan ya definidas 
        if self.visit(node.condition, scope).name != 'bool':
            self.errors.append(SemanticError(f'La condicion del if debe ser de tipo bool'))
            
        inner_scope = scope.create_child()
        for statment in node.body:
            self.visit(statment, inner_scope)
        
        for _elif in node._elif:        
            self.visit(_elif, scope)
        
        self.visit(node._else, scope)
        
        #* En los nodos que no son expresiones aritmeticas o booleanas o concatenacion dberia ponerle qu etiene typo object?
        return self.context.get_type('object')
        
    @visitor.when(ElifStructureNode)
    def visit(self, node: ElifStructureNode, scope: Scope):
        if self.visit(node.condition, scope).name != 'bool':
            self.errors.append(SemanticError(f'La condicion del if debe ser de tipo bool'))
            
        inner_scope = scope.create_child()
        for statment in node.body:
            self.visit(statment, inner_scope)
            
        return self.context.get_type('object')
        
    @visitor.when(ElseStructureNode)
    def visit(self, node: ElseStructureNode, scope: Scope):
        inner_scope = scope.create_child()
        for statment in node.body:
            self.visit(statment, inner_scope)
            
        return self.context.get_type('object')
        
    @visitor.when(WhileStructureNode)
    def visit(self, node: WhileStructureNode, scope: Scope):
        if self.visit(node.condition, scope).name != 'bool':
            self.errors.append(SemanticError(f'La condicion del while debe ser de tipo bool'))
            
        inner_scope = scope.create_child()
        for statment in node.body:
            self.visit(statment, inner_scope)
            
        return self.context.get_type('object')
            
    @visitor.when(ForStructureNode)
    def visit(self, node: ForStructureNode, scope: Scope):
        inner_scope: Scope = scope.create_child()
        for assin in node.init_assigments:
            id, expr = assin.id.id, assin.expression
            
            if scope.is_defined(id):
                self.errors.append(SemanticError(f'La variable {id} ya esta definida en este scope.'))
            else:
                inner_scope.define_variable(id, self.visit(expr, inner_scope)) #* Aqui en el 2do parametro de la funcion se infiere el tipo de la expresion que se le va a asignar a la variable
            
        self.visit(node.body, inner_scope)
        
        for increment_assigment in node.increment_condition:
            self.visit(increment_assigment, inner_scope)
            
        return self.context.get_type('object')
            
    @visitor.when(TypeDefinitionNode)
    def visit(self, node: TypeDefinitionNode, scope: Scope):
        #node_id: IdentifierNode = node.id
        
        self.current_type = self.context.get_type(node.id.id)
        
        inner_scope: Scope = scope.create_child()
        
        #TODO Ver que se hace con los argumentos porque fuera del 'constructor' ya no tienen sentido
        for param in node.parameters:
            arg, type_att = param.items[0].key, param.items[0].value
            inner_scope.define_variable(arg, type_att)
            
        for att in node.attributes:
            inner_scope.define_variable(att.id.id, self.visit(att.expression, inner_scope)) #* Aqui en el 2do parametro de la funcion se infiere el tipo de la expresion que se le va a asignar a la variable
            
        for method in node.methods:
            self.visit(method, inner_scope)
            
        self.current_type = None
        
        return self.context.get_type('object')
            
    # @visitor.when(InstanceCreationNode)
    # def visit(self, node: InstanceCreationNode, scope: Scope):
    #     if scope.is_local(node.id) or scope.is_defined(node.id):
    #         self.errors.append(SemanticError(f'El nombre de varible {node.id} ya ha sido tomado.'))
    #     else:
    #         try:
    #             # for arg in node.arguments:
    #             #     self.visit(arg, scope)
    #             class_type: Type = self.context.types[node.type]
    #             if len[class_type.attributes] != len(node.arguments):
    #                 self.errors.append(SemanticError(f'La cantidad de argumentos no coincide con la cantidad de atributos de la clase {node.type}.'))
    #             else:
    #                 correct = True
    #                 for i in range(len(node.arguments)):
    #                     # Hay que crear una jerarquia de tipos por causa de la herencia de clases
    #                     if class_type.attributes[i].type != self.visit(node.arguments[i], scope):
    #                         self.errors.append(SemanticError(f'El tipo del argumento {i} no coincide con el tipo del atributo {i} de la clase {node.type}.'))
    #                     else: correct = False
                            
    #                 if correct: 
    #                     scope.define_variable(node.id, self.context.types[node.type])
    #         except:
    #             self.errors.append(SemanticError(f'El tipo {node.type} no esta definido.')) 
            
    @visitor.when(KernInstanceCreationNode)
    def visit(self, node: KernInstanceCreationNode, scope: Scope):
        try:
            class_type: Type = self.context.types[node.type.id]
            if len[class_type.attributes] != len(node.args):
                self.errors.append(SemanticError(f'La cantidad de argumentos no coincide con la cantidad de atributos de la clase {node.type}.'))
            else:
                correct = True
                for i in range(len(node.args)):
                    #! Hay que crear una jerarquia de tipos por causa de la herencia de clases
                    if class_type.attributes[i].type != self.visit(node.args[i], scope):
                        self.errors.append(SemanticError(f'El tipo del argumento {i} no coincide con el tipo del atributo {class_type.attributes[i].name} de la clase {node.type.id}.'))
                        correct = False
                        
                if correct: 
                    return self.context.get_type(node.type.id)
        except:
            self.errors.append(SemanticError(f'El tipo {node.type.id} no esta definido.')) 
            
        return self.context.get_type('object')
            
    @visitor.when(MemberAccessNode)
    def visit(self, node: MemberAccessNode, scope: Scope):
        #! Hay que hacer la diferenciacion de casos entre una variable y otro tipo de factor
        base_object_type: Type = self.visit(node.base_object, scope)
        try:
            if node.object_property_to_acces in base_object_type.methods:
                #En caso de ser un metodo se verifica si la cantidaobject_property_to_accesd de parametros suministrados es correcta
                index = base_object_type.methods.index(node.object_property_to_acces)
                if len(node.args) != len(base_object_type.methods[index].param_names):
                    #Si la cantidad de parametros no es correcta se lanza un error
                    self.errors.append(SemanticError(f'La funcio        n {node.object_property_to_acces} requiere {len(base_object_type.methods[index].param_names)} cantidad de parametros pero {len(node.args)} fueron dados'))
                else:
                    #Si la cantidad de parametros es correcta se verifica si los tipos de los parametros suministrados son correctos
                    #! OJO aqui tambien hay que ver lo de la jeraquia de clases
                    #Luego por cada parametro suministrado se verifica si el tipo del parametro suministrado es igual al tipo del parametro de la funcion
                    for i in range(len(node.args)):
                        correct = True
                        if base_object_type.methods[index].param_types[i] != self.visit(node.args[i], scope):
                            self.errors.append(SemanticError(f'El tipo del parametro {i} no coincide con el tipo del parametro {i} de la funcion {node.object_property_to_acces}.'))
                            correct = False
                    #Si coinciden los tipos de los parametros entonces se retorna el tipo de retorno de la funcion en otro caso se retorna el tipo object
                    return base_object_type.methods[index].return_type if correct else self.context.get_type('object')
        except: 
            #Si el id suministrado no es ni un atributo ni un metodo entonces se lanza un error y se retorna el tipo object
            self.errors.append(SemanticError(f'El objeto no tiene un atributo o metod llamado {node.object_property_to_acces}.'))
            return self.context.get_type('object')
            
    @visitor.when(BooleanExpression)
    def visit(self, node: BooleanExpression, scope: Scope):
        type_1: Type = self.visit(node.left, scope)
        type_2: Type = self.visit(node.right, scope)
        
        if not type_1.name == type_2.name == 'bool':
            self.errors.append(SemanticError(f'Solo se pueden emplear operadores booleanos entre expresiones booleanas.'))
            return self.context.get_type('object')

        return type_1
        
    @visitor.when(AritmeticExpression)
    def visit(self, node: AritmeticExpression, scope: Scope):
        type_1: Type = self.visit(node.expression_1, scope)
        type_2: Type = self.visit(node.expression_2, scope)
        
        if type_1.name != 'number' or type_2.name != 'number':
            self.errors.append(SemanticError(f'Solo se pueden emplear aritmeticos entre expresiones aritmeticas.'))
            return self.context.get_type('object')
        
        return type_1
        
    @visitor.when(MathOperationNode)
    def visit(self, node: MathOperationNode, scope: Scope):
        if self.visit(node.expression, scope).name != 'number':
            self.errors.append(SemanticError(f'Esta funcion solo puede ser aplicada a numeros.'))
            return self.context.get_type('object')
        
        return self.context.get_type('number')
        
    @visitor.when(LogCallNode)
    def visit(self, node: LogCallNode, scope: Scope):
        if self.visit(node.base, scope).name != 'number' or self.visit(node.expression, scope).name != 'number':
            self.errors.append(SemanticError(f'Esta funcion solo puede ser aplicada a numeros.'))
            return self.context.get_type('object')
        
        return self.context.get_type('number')
        
    @visitor.when(LetInNode)
    def visit(self, node: LetInNode, scope: Scope):
        inner_scope = scope.create_child()
        for assign in node.assigments:
            self.visit(assign, inner_scope)
            
        self.visit(node.body, inner_scope)
        
        return self.context.get_type('object')
            
    #! Por este tipo de nodos es que es necesario crear un objeto de tipo Method cada vez que se cree una funcion
    #TODO Crear un objeto de tipo Method cada vez que se cree una funcion
    @visitor.when(FunctionCallNode)
    def visit(self, node: FunctionCallNode, scope: Scope):
        try: 
            args_len = scope.functions[node.id.id]
            if args_len != len(node.args):
                self.errors.append(f'La funcion {id} requiere {args_len} cantidad de parametros pero solo {len(node.args)} fueron dados')
        except:
            self.errors.append(f'La funcion {node.id.id} no esta definida.')
            
    @visitor.when(StringConcatNode)
    def visit(self, node: StringConcatNode, scope: Scope):
        if (self.visit(node.left, scope).name != 'string' and self.visit(node.left, scope).name != 'number') or (self.visit(node.right, scope).name != 'string' and self.visit(node.right, scope).name != 'number'):
            self.errors.append(SemanticError(f'Esta operacion solo puede ser aplicada a strings o entre una combinacion de string con number.'))
            return self.context.get_type('object')
        
        return self.context.get_type('string')
            
    @visitor.when(StringConcatWithSpaceNode)
    def visit(self, node: StringConcatWithSpaceNode, scope: Scope):
        if (self.visit(node.left, scope).name != 'string' and self.visit(node.left, scope).name != 'number') or (self.visit(node.right, scope).name != 'string' and self.visit(node.right, scope).name != 'number'):
            self.errors.append(SemanticError(f'Esta operacion solo puede ser aplicada a strings o entre una combinacion de string con number.'))
            return self.context.get_type('object')
        
        return self.context.get_type('string')
        
    @visitor.when(BoolCompAritNode)
    def visit(self, node: BoolCompAritNode, scope: Scope):
        if self.visit(node.left, scope).name != 'number' or self.visit(node.right, scope).name != 'number':
            self.errors.append(SemanticError(f'Esta operacion solo puede ser aplicada a numeros.'))
            return self.context.get_type('object')
        
        return self.context.get_type('bool')
        
    @visitor.when(BoolNotNode)
    def visit(self, node: BoolNotNode, scope: Scope):
        if self.visit(node.node, scope).name != 'bool':
            self.errors.append(SemanticError(f'Esta operacion solo puede ser aplicada a booleanos.'))
            return self.context.get_type('object')
        
        return self.context.get_type('bool')
    
    @visitor.when(NumberNode)
    def visit(self, node: NumberNode, scope):
        try:
            a: float = float(node.value)
            return self.context.get_type('number')
        except:
            self.errors.append(SemanticError(f'El elemento {node.value} no es un numero'))
            return self.context.get_type('object')
        
    @visitor.when(InheritanceNode)
    def visit(self, node: InheritanceNode, scope):
        try:
            return self.context.get_type(node.type)
        except:
            self.errors.append(SemanticError(f'El tipo {node.type} no esta definifo'))
            return self.context.get_type('object') 

    @visitor.when(StringNode)
    def visit(self, node: StringNode, scope):
        try:
            string = str(node.value)
            return self.context.get_type('string')
        except:
            return self.context.get_type('string')
        
    @visitor.when(BooleanNode)
    def visit(self, node: BooleanNode, scope):
        try:
            boolean = bool(node.value)
            return self.context.create_type('bool')
        except:
            return self.context.get_type('object')
        
    @visitor.when(IdentifierNode)
    def visit(self, node: IdentifierNode, scope: Scope):
        if self.scope.is_defined(node.id):
            return self.scope.find_variable(node.id).type
            
        self.errors.append(SemanticError(f'La variable {node.id} no esta deifinida'))
        return self.context.get_type('object')
        