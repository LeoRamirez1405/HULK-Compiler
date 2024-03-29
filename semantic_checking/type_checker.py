import visitor
from AST import *
from semantic import Context, Scope, SemanticError, Type

#! Hay que ver que se hace con las funciones que no son metodos de alguna clase   OJO

class TypeCheckerVisitor:
    def __init__(self, context: Context, scope: Scope, errors, default_functions) -> None:
        self.context: Context = context
        self.errors: List[str] = errors
        self.scope: Scope = scope
        self.default_functions = default_functions
        
    @visitor.on('node')
    def visit(self, node, scope):
        pass
    
    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode):
        for statment in node.statments:
            self.visit(statment, self.scope) 
            
    @visitor.when(PrintStatmentNode)
    def visit(self, node: PrintStatmentNode, scope):
        print('visitor en PrintNode')
        self.visit(node.expression, scope)
            
    @visitor.when(DestroyNode)
    def visit(self, node: DestroyNode, scope: Scope):
        if not scope.is_defined(node.id):
            self.errors.append(SemanticError(f'La variable {node.id} no esta definida en este scope'))
            
        return self.visit(node.expression, scope)
        
    @visitor.when(LetNode)
    def visit(self, node: LetNode, scope: Scope):
        if scope.is_local(node.id) or scope.is_defined(node.id):
            self.errors.append(SemanticError(f'La variable {node.id} ya esta definida.'))
        else:
            scope.define_variable(node.id, self.visit(node.expression, scope)) #* Aqui en el 2do parametro de la funcion se infiere el tipo de la expresion que se le va a asignar a la variable
            
        return self.context.get_type('object')
    
    #* Esto se usa a la hora de definir los parametros de una funcion que se esta creando
    @visitor.when(TypeNode)
    def visit(self, node: TypeNode, scope: Scope):
        try:
            self.context.types[node.type]
            return self.context.types[node.type]
        except:
            self.errors.append(SemanticError(f'Tipo {node.type} no esta definido'))
            return self.context.get_type('object')
            
    @visitor.when(FunctionDefinitionNode)
    def visit(self, node: FunctionDefinitionNode, scope: Scope):
        if node.id in self.default_functions:
            self.errors.append(SemanticError(f'Esta redefiniendo una funcion {node.id} que esta definida por defecto en el lenguaje y no se puede sobreescribir'))
            
            #* En los nodos que no son expresiones aritmeticas o booleanas o concatenacion dberia ponerle qu etiene typo object?
            return self.context.get_type('object')
        
        try:
            args_len_list = scope.functions[node.id]
            if  len(node.parameters) in args_len_list:
                self.errors.append(SemanticError(f'La funcion {node.id} ya esta definida con {len(node.args)} cantidad de parametros.'))
            else:
                scope.functions[node.id].append(len(node.parameters))
        except:
            #TODO Se puede instanciar la clase Method de semantic~seria algo similar a scope.functions[node.id] = nodmethod(node. ...)
            #* Por el momento en el diccionario tengo el id de la funcion con su cantidad de parametros
            scope.functions[node.id].append(len(node.args))
            

#----------------------------------------Checkeo de tipos--------------------------------------------------------------------------------------------------------------#
            inner_scope: Scope = scope.create_child()            
            for arg, type in node.parameters:
                inner_scope.define_variable(arg, self.visit(type, inner_scope))
                
            self.visit(node.body, inner_scope)
#----------------------------------------Checkeo de tipos--------------------------------------------------------------------------------------------------------------#
            return self.context.get_type('object')
            
    @visitor.when(IfStructureNode)
    def visit(self, node: IfStructureNode, scope: Scope):
        # verifico el tipo de la condicion y a la vez veo si las variables que estan dentro de ella estan ya definidas 
        if self.visit(node.condition).name != 'bool':
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
        if self.visit(node.condition) != 'bool':
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
        if self.visit(node.condition, scope) != 'bool':
            self.errors.append(SemanticError(f'La condicion del while debe ser de tipo bool'))
            
        inner_scope = scope.create_child()
        for statment in node.body:
            self.visit(statment, inner_scope)
            
        return self.context.get_type('object')
            
    @visitor.when(ForStructureNode)
    def visit(self, node: ForStructureNode, scope: Scope):
        inners_scope: Scope = scope.create_child()
        for id, expr in node.init_assigments:
            if scope.is_defined(node.id):
                self.errors.append(SemanticError(f'La variable {id} ya esta definida en este scope.'))
            else:
                inners_scope.define_variable(id, self.visit(expr, inners_scope)) #* Aqui en el 2do parametro de la funcion se infiere el tipo de la expresion que se le va a asignar a la variable
            
        self.visit(node.body, inners_scope)
        
        for increment_assigment in node.increment_condition:
            self.visit(increment_assigment, inners_scope)
            
        return self.context.get_type('object')
            
    @visitor.when(TypeDefinitionNode)
    def visit(self, node: TypeDefinitionNode, scope: Scope):
        inner_scope: Scope = scope.create_child()
        
        #TODO Ver que se hace con los argumentos porque fuera del 'constructor' ya no tienen sentido
        for arg, type_att in node.parameters:
            inner_scope.define_variable(arg, type_att)
            
        for att in node.attribute:
            inner_scope.define_variable(att.id, self.visit(att.expression, inner_scope)) #* Aqui en el 2do parametro de la funcion se infiere el tipo de la expresion que se le va a asignar a la variable
            
        for method in node.methods:
            self.visit(method, inner_scope)
            
        return self.context.get_type('object')
            
    @visitor.when(InstanceCreationNode)
    def visit(self, node: InstanceCreationNode, scope: Scope):
        if scope.is_local(node.id) or scope.is_defined(node.id):
            self.errors.append(SemanticError(f'El nombre de varible {node.id} ya ha sido tomado.'))
        else:
            try:
                # for arg in node.arguments:
                #     self.visit(arg, scope)
                class_type: Type = self.context.types[node.type]
                if len[class_type.attributes] != len(node.arguments):
                    self.errors.append(SemanticError(f'La cantidad de argumentos no coincide con la cantidad de atributos de la clase {node.type}.'))
                else:
                    correct = True
                    for i in range(len(node.arguments)):
                        #! Hay que crear una jerarquia de tipos por causa de la herencia de clases
                        if class_type.attributes[i].type != self.visit(node.arguments[i], scope):
                            self.errors.append(SemanticError(f'El tipo del argumento {i} no coincide con el tipo del atributo {i} de la clase {node.type}.'))
                        else: correct = False
                            
                    if correct: 
                        scope.define_variable(node.id, self.context.types[node.type])
            except:
                self.errors.append(SemanticError(f'El tipo {node.type} no esta definido.')) 
            
    @visitor.when(KernInstanceCreationNode)
    def visit(self, node: KernInstanceCreationNode, scope: Scope):
        try:
            # for arg in node.arguments:
            #     self.visit(arg, scope)
            class_type: Type = self.context.types[node.type]
            if len[class_type.attributes] != len(node.arguments):
                self.errors.append(SemanticError(f'La cantidad de argumentos no coincide con la cantidad de atributos de la clase {node.type}.'))
            else:
                correct = True
                for i in range(len(node.arguments)):
                    #! Hay que crear una jerarquia de tipos por causa de la herencia de clases
                    if class_type.attributes[i].type != self.visit(node.arguments[i], scope):
                        self.errors.append(SemanticError(f'El tipo del argumento {i} no coincide con el tipo del atributo {i} de la clase {node.type}.'))
                    else: correct = False
                        
                if correct: 
                    scope.define_variable(node.id, self.context.types[node.type])
        except:
            self.errors.append(SemanticError(f'El tipo {node.type} no esta definido.')) 
            
    @visitor.when(MemberAccesNode)
    def visit(self, node: MemberAccesNode, scope: Scope):
        #! Hay que hacer la diferenciacion de casos entre una variable y otro tipo de factor
        base_object_type: Type = self.visit(node.base_object, scope)
        try:
            #Verifico si se quiere acceder a un atributo del tipo en cuestion
            if node.object_property_to_acces in base_object_type.attributes:
                #Si se quiere acceder a un atributo pero fueron asignados parametros entonces se lanza un error
                if len(node.args) != 0:
                    self.errors.append(SemanticError(f'El objeto {node.base_object} no tiene un metodo {node.object_property_to_acces}.'))
                else:
                    #En otro caso el acceso es correcto
                    index = base_object_type.attributes.index(node.object_property_to_acces)
                    #El tipo del member_acces es el tipo del tributo al que se accedio
                    return base_object_type.attributes[index].type
            #Si el id suministrado no es un atributo entonces se verifica si es un metodo
            elif node.object_property_to_acces in base_object_type.methods:
                #En caso de ser un metodo se verifica si la cantidad de parametros suministrados es correcta
                index = base_object_type.methods.index(node.object_property_to_acces)
                if len(node.args) != len(base_object_type.methods[index].param_names):
                    #Si la cantidad de parametros no es correcta se lanza un error
                    self.errors.append(SemanticError(f'La funcion {node.object_property_to_acces} requiere {len(base_object_type.methods[index].param_names)} cantidad de parametros pero {len(node.args)} fueron dados'))
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
        type_1: Type = self.visit(node.left, scope)
        type_2: Type = self.visit(node.right, scope)
        
        if not type_1.name == type_2.name == 'bool':
            self.errors.append(SemanticError(f'Solo se pueden emplear aritmeticos booleanos entre expresiones aritmeticas.'))
            return self.context.get_type('object')
        
        return type_1
        
    @visitor.when(MathOperationNode)
    def visit(self, node: MathOperationNode, scope: Scope):
        if self.visit(node.expression) != 'number':
            self.errors.append(SemanticError(f'Esta funcion solo puede ser aplicada a numeros.'))
            return self.context.get_type('object')
        
        return self.context.get_type('number')
        
    @visitor.when(LogCallNode)
    def visit(self, node: LogCallNode, scope: Scope):
        if self.visit(node.base, scope) != 'number' or self.visit(node.expression, scope) != 'number':
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
            args_len = scope.functions[node.id]
            if args_len != len(node.args):
                self.errors.append(f'La funcion {id} requiere {args_len} cantidad de parametros pero solo {len(node.args)} fueron dados')
        except:
            self.errors.append(f'La funcion {node.id} no esta definida.')
            
        
            
    @visitor.when(StringConcatWithSpaceNode)
    def visit(self, node: StringConcatWithSpaceNode, scope: Scope):
        if self.visit(node.left, scope) != 'string' or self.visit(node.right, scope) != 'string':
            self.errors.append(SemanticError(f'Esta operacion solo puede ser aplicada a strings.'))
            return self.context.get_type('object')
        
        return self.context.get_type('string')
        
    @visitor.when(BoolCompAritNode)
    def visit(self, node: BoolCompAritNode, scope: Scope):
        if self.visit(node.left, scope) != 'number' or self.visit(node.right, scope) != 'number':
            self.errors.append(SemanticError(f'Esta operacion solo puede ser aplicada a numeros.'))
            return self.context.get_type('object')
        
        return self.context.get_type('bool')
        
    @visitor.when(BoolNotNode)
    def visit(self, node: BoolNotNode, scope: Scope):
        if self.visit(node.node) != 'bool':
            self.errors.append(SemanticError(f'Esta operacion solo puede ser aplicada a booleanos.'))
            return self.context.get_type('object')
        
        return self.context.get_type('bool')

            
    