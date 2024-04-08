from semantic_checking.semantic import *
import semantic_checking.visitor as visitor
from semantic_checking.AST import *
# from AST import *
class TypeCheckerVisitor:
    def __init__(self, context: Context, scope: Scope, errors, default_functions) -> None:
        self.context: Context = context
        self.errors: List[str] = errors
        self.scope: Scope = scope
        self.default_functions = default_functions
        self.current_type: Type = None
        self.current_method: Method = None
        
    @visitor.on('node')
    def visit(self, node, scope):
        print(f"OnGeneric: {type(node)}")
        pass
    
    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode):
        #print("OnProgram (Checker)")
        for statment in node.statments:
            #print(f"Statement (Checker): {statment}")
            self.visit(statment, self.scope) 
            
    @visitor.when(PrintStatmentNode)
    def visit(self, node: PrintStatmentNode, scope):
        return self.visit(node.expression, scope)
            
    @visitor.when(DestroyNode)
    def visit(self, node: DestroyNode, scope: Scope):
        
        if type(node.id) == SelfNode:
            self.visit(node.id,scope)
        else:    
            if not scope.is_defined(node.id.id):
                self.errors.append(SemanticError(f'La variable {node.id.id} no esta definida en este scope'))
            
        return self.visit(node.expression, scope)
        
    @visitor.when(KernAssigmentNode)
    def visit(self, node: KernAssigmentNode, scope: Scope):
        # if scope.parent == None:
        #     try:
        #         var: VariableInfo = self.scope.find_variable(node.id.id)
        #         var.type = self.visit(node.expression, scope)
        #     except:
        #         self.errors.append(SemanticError(f'La variable {node.id.id} ya esta definida.'))
        #     return self.context.get_type('any')
        if scope.is_local(node.id.id):
            self.errors.append(SemanticError(f'La variable {node.id.id} ya esta definida.'))
            return scope.find_variable(node.id.id).type
        else:
            type = self.visit(node.expression, scope)
            scope.define_variable(node.id.id, type) #* Aqui en el 2do parametro de la funcion se infiere el tipo de la expresion que se le va a asignar a la variable
            
        return type
    
    #* Esto se usa a la hora de definir los parametros de una funcion que se esta creando
    @visitor.when(TypeNode)
    def visit(self, node: TypeNode, scope: Scope):
        try:
            return self.context.get_type(node.type)
        except:
            self.errors.append(SemanticError(f'Tipo {node.type} no esta definido [L:{node.location[0]}, C:{node.location[1]}]'))
            return self.context.get_type('any')
            
    @visitor.when(FunctionDefinitionNode)
    def visit(self, node: FunctionDefinitionNode, scope: Scope):
        if node.id.id in self.default_functions:
            self.errors.append(SemanticError(f'Esta redefiniendo una funcion {node.id.id} que esta definida por defecto en el lenguaje y no se puede sobreescribir'))
            
            #* En los nodos que no son expresiones aritmeticas o booleanas o concatenacion o llamados a funciones deberia ponerle que tiene typo any?
            return self.context.get_type('any')
        
        if self.current_type:
            method = self.current_type.get_method(node.id.id)
        else:
            # try:
            #     self.scope.functions[node.id.id]
            #     self.errors.append(SemanticError(f'Esta redefiniendo una funcion {node.id.id} que esta definida en el lenguaje y no se puede sobreescribir'))
            
            #     #* En los nodos que no son expresiones aritmeticas o booleanas o concatenacion o llamados a funciones deberia ponerle que tiene typo any?
            #     return self.context.get_type('any')
            # except:
            try: 
                type_annotation: TypeNode = node.type_annotation
                return_type = self.context.get_type(type_annotation.type)
            except:
                self.errors.append(f'El tipo de retorno {node.type_annotation.type} no esta definido')
                return_type = self.context.get_type('object')
                
            # print(node.parameters)
            arg_names: List[IdentifierNode] = [list(parama.items())[0] for parama in node.parameters]
            arg_names = [name[0].id for name in arg_names]
            # print(arg_names)
            arg_types = []
            aux = [list(parama.items())[0] for parama in node.parameters]
            # print(aux)
            for parama in aux:
                try:
                    arg_types.append(self.context.get_type(parama[1].type))
                except:
                    self.errors.append(SemanticError(f'El tipo del parametro {parama[0].id} que se le pasa a la funcion {node.id.id} no esta definido'))
                    arg_types.append(self.context.get_type('object'))
            
            try:
                if scope.method_is_define(node.id.id, len(node.parameters)):
                    method = scope.get_method(node.id.id, len(node.parameters))
                    self.errors.append(f'La funcion {node.id.id} ya existe en este scope con {len(arg_names)} cantidad de parametros')
                    # return method.return_type
                else:
                    method = Method(node.id.id, arg_names, arg_types, return_type)
                    scope.functions[node.id.id].append(method)
                    
            except:
                method = Method(node.id.id, arg_names, arg_types, return_type)
                scope.functions[node.id.id] = [method]
               
        inner_scope: Scope = scope.create_child()            
        for i in range(len(method.param_names)):
            inner_scope.define_variable(method.param_names[i], method.param_types[i])
            
        
        # Visitar el cuerpo de la instruccion
        final_type = self.context.get_type('object')
        if type(node.body) == list:
            for statment in node.body: 
                final_type = self.visit(statment, inner_scope)
        else:
            final_type = self.visit(node.body, inner_scope)
          
        return method.return_type if final_type.conforms_to(method.return_type.name) else self.context.get_type('any')
            
    @visitor.when(IfStructureNode)
    def visit(self, node: IfStructureNode, scope: Scope):
        # verifico el tipo de la condicion y a la vez veo si las variables que estan dentro de ella estan ya definidas 
        if not self.visit(node.condition, scope).conforms_to('bool'):
            self.errors.append(SemanticError(f'La condicion del if debe ser de tipo bool'))
            
        type = self.context.get_type('object')    
            
        inner_scope = scope.create_child()
        aux_type = self.context.get_type('object')
        if node.body:
            for statment in node.body:
                aux_type = self.visit(statment, inner_scope)
            type = aux_type
        
        inner_scope = scope.create_child()
        if len(node._elif) != 0:
            aux_type = self.context.get_type('object')
            for item in node._elif:
                aux_type = self.visit(item, inner_scope)
                if not aux_type.conforms_to(type.name):
                    self.errors.append(SemanticError(f'Los distintos bloques del if no retornan el mismo tipo.'))
                    type = self.context.get_type('any')
                    break
        
        inner_scope = scope.create_child()
        if len(node._else) != 0:
            if not self.visit(node._else, inner_scope).conforms_to(type.name):
                self.errors.append(SemanticError(f'Los distintos bloques del if no retornan el mismo tipo.'))
                type = self.context.get_type('any')
        
        return type
        
    @visitor.when(ElifStructureNode)
    def visit(self, node: ElifStructureNode, scope: Scope):
        if not self.visit(node.condition, scope).conforms_to('bool'):
            self.errors.append(SemanticError(f'La condicion del if debe ser de tipo bool'))
            
        inner_scope = scope.create_child()
        final_type = self.context.get_type('object')
        for statment in node.body:
            final_type = self.visit(statment, inner_scope)
            
        return final_type
        
    @visitor.when(ElseStructureNode)
    def visit(self, node: ElseStructureNode, scope: Scope):
        inner_scope = scope.create_child()
        type = self.context.get_type('any')
        for statment in node.body:
            type = self.visit(statment, inner_scope)
            
        return type
        
    @visitor.when(WhileStructureNode)
    def visit(self, node: WhileStructureNode, scope: Scope):
        if not self.visit(node.condition, scope).conforms_to('bool'):
            self.errors.append(SemanticError(f'La condicion del while debe ser de tipo bool'))
            
        inner_scope = scope.create_child()
        type = self.context.get_type('object') 
        for statment in node.body:   
            type = self.visit(statment, inner_scope)
          
        return type
            
    @visitor.when(ForStructureNode)
    def visit(self, node: ForStructureNode, scope: Scope):
        inner_scope: Scope = scope.create_child()
      
        self.visit(node.init_assigments, inner_scope) 
         
        self.visit(node.increment_condition, inner_scope)
        final_type = self.context.get_type('object') 
        if type(node.body) == list:
            for statment in node.body:   
                final_type = self.visit(statment, inner_scope)
        else:
            final_type = self.visit(node.body, inner_scope)
          
        return final_type
            
    @visitor.when(TypeDefinitionNode)
    def visit(self, node: TypeDefinitionNode, scope: Scope):
        self.current_type = self.context.get_type(node.id.id)
        
        temp_scope: Scope = scope.create_child()
        
        #* Creando un temp_scope me aseguro de que los argumentos del 'constructor' solo sean utiles a la hora de inicializar los atributos
        for param in node.parameters:
            try:
                arg, type_att = list(param.items())[0][0], self.context.get_type(list(param.items())[0][1].type)
            except:
                arg, type_att = list(param.items())[0][0], self.context.get_type('object')
                self.errors.append(SemanticError(f"El tipo {list(param.items())[0][1].type} del argumento {arg.id} no esta definido"))
            temp_scope.define_variable(arg.id, type_att)
            
        self.visit(node.inheritance, temp_scope)
        
        inner_scope = self.scope.create_child()
        for att in node.attributes:
            typ = self.visit(att.expression, temp_scope)
            type_att = self.current_type.get_attribute(att.id.id)
            type_att.type = typ
            # inner_scope.define_variable(att.id.id, typ) #* Aqui en el 2do parametro de la funcion se infiere el tipo de la expresion que se le va a asignar a la variable
            
        for method in node.methods:
            self.current_metod = method
            self.visit(method, inner_scope)
            
        self.current_method = None
        self.current_type = None
        
        return self.context.get_type('any')
            
    @visitor.when(KernInstanceCreationNode)
    def visit(self, node: KernInstanceCreationNode, scope: Scope):
        correct = True
        try:
            class_type: Type = self.context.types[node.type.id]
            if len(class_type.args) != len(node.args):
                self.errors.append(SemanticError(f'La cantidad de argumentos no coincide con la cantidad de atributos de la clase {node.type.name}.'))
                correct = False
            else:
                for i in range(len(node.args)):
                    if not self.visit(node.args[i], scope).conforms_to(class_type.args[i].type.name):
                        self.errors.append(SemanticError(f'El tipo del argumento {i} no coincide con el tipo del atributo {class_type.attributes[i].name} de la clase {node.type.id}.'))
                        correct = False
                
            return self.context.get_type(node.type.id) if correct else self.context.get_type('any')
        except:
            self.errors.append(SemanticError(f'El tipo {node.type.id} no esta definido.')) 
            
        return self.context.get_type('any')
            
    @visitor.when(MemberAccessNode)
    def visit(self, node: MemberAccessNode, scope: Scope):
        base_object_type: Type = self.visit(node.base_object, scope)
        try:
            method = base_object_type.get_method(node.object_property_to_acces.id)
            #En caso de ser un metodo se verifica si la cantidad de parametros suministrados es correcta
            if method :
                if len(node.args) != len(method.param_names):
                    #Si la cantidad de parametros no es correcta se lanza un error
                    self.errors.append(SemanticError(f'La funcion {node.object_property_to_acces.id} de la clase {base_object_type.name} recibe {len(method.param_names)} parametros y {len(node.args)} fueron suministrados'))
                    return self.context.get_type('any')
            else:
                self.errors.append(SemanticError(f'El metodo {node.object_property_to_acces.id} no existe en la clase {base_object_type.name}'))
                return self.context.get_type('any')
            
            correct = True
            #Si la cantidad de parametros es correcta se verifica si los tipos de los parametros suministrados son correctos
            #Luego por cada parametro suministrado se verifica si el tipo del parametro suministrado es igual al tipo del parametro de la funcion
            for i in range(len(node.args)):
                if not self.visit(node.args[i], scope).conforms_to(method.param_types[i].name):
                    self.errors.append(SemanticError(f'El tipo del parametro {i} no coincide con el tipo del parametro {i} de la funcion {node.object_property_to_acces.id}.'))
                    correct = False
            #Si coinciden los tipos de los parametros entonces se retorna el tipo de retorno de la funcion en otro caso se retorna el tipo object
            return method.return_type if correct else self.context.get_type('any')
        except: 
            #Si el id suministrado no es ni un atributo ni un metodo entonces se lanza un error y se retorna el tipo object
            self.errors.append(SemanticError(f'El objeto de tipo {base_object_type.name} no tiene el metod llamado {node.object_property_to_acces.id}.'))
            return self.context.get_type('any')
            
    @visitor.when(BooleanExpression)
    def visit(self, node: BooleanExpression, scope: Scope):
        type_1: Type = self.visit(node.left, scope)
        type_2: Type = self.visit(node.right, scope)
        
        if not type_1.conforms_to('bool') or not type_2.conforms_to('bool'):
            self.errors.append(SemanticError(f'Solo se pueden emplear operadores booleanos entre expresiones booleanas.'))
            return self.context.get_type('any')

        return type_1
        
    @visitor.when(AritmeticExpression)
    def visit(self, node: AritmeticExpression, scope: Scope):
        # print("OnAritmeticExpressionNode")
        type_1: Type = self.visit(node.expression_1, scope)
        # print(f"type 1: {type_1}")
        type_2: Type = self.visit(node.expression_2, scope)
        # print(f"type 2: {type_2}")
        
        if not type_1.conforms_to('number') or not type_2.conforms_to('number'):
            self.errors.append(SemanticError(f'Solo se pueden emplear aritmeticos entre expresiones aritmeticas. On: L: {node.location[0]} C: {node.location[1]}')) #TODO
            return self.context.get_type('any')
        
        return type_1
    
    @visitor.when(MathOperationNode)
    def visit(self, node: MathOperationNode, scope: Scope):
        if not self.visit(node.node, scope).conforms_to('number'):
            self.errors.append(SemanticError(f'Esta funcion solo puede ser aplicada a numeros.'))
            return self.context.get_type('any')
        
        return self.context.get_type('number')
        
    @visitor.when(LogFunctionCallNode)
    def visit(self, node: LogFunctionCallNode, scope: Scope):
        if not self.visit(node.base, scope).conforms_to('number') or not self.visit(node.expression, scope).conforms_to('number'):
            self.errors.append(SemanticError(f'Esta funcion solo puede ser aplicada a numeros.'))
            return self.context.get_type('any')
        
        return self.context.get_type('number')
    
    @visitor.when(RandomFunctionCallNode)
    def visit(self, node: RandomFunctionCallNode, scope: Scope):
        return self.context.get_type('number')
    
    @visitor.when(LetInExpressionNode)
    def visit(self, node: LetInExpressionNode, scope: Scope):
        inner_scope = scope.create_child()
        # for assign in node.assigments:
        #     self.visit(assign, inner_scope)
        self.visit(node.assigments, inner_scope)
        
        final_type = self.context.get_type('object')
        if type(node.body) == list:
            for statment in node.body:    
                final_type = self.visit(statment, inner_scope)
        else:
            final_type = self.visit(node.body, inner_scope)
            
        return final_type
            
    @visitor.when(FunctionCallNode)
    def visit(self, node: FunctionCallNode, scope: Scope):
        try: 
            if self.current_type:
                if self.current_method and node.id.id == "base":
                    inheritance_methods = self.current_type.inhertance.methods
                    try:
                        method = list(
                            filter(
                                lambda x: x.name == self.current_method.id.id,
                                inheritance_methods,
                            )
                        )[0]
                    except:
                        self.errors.append(
                            SemanticError(
                                f"El tipo {self.current_type.name} no posee ningún ancestro con el método {self.current_method.id.id}. Linea:{node.location[0]} , Columna:{node.location[1]} "
                            )
                        )
                else:
                    method = self.current_type.get_method(node.id.id)
                # En caso de ser un metodo se verifica si la cantidad de parametros suministrados es correcta

                
                #method = self.current_type.get_method(node.id.id)
                #En caso de ser un metodo se verifica si la cantidad de parametros suministrados es correcta
                if method :
                    if len(node.args) != len(method.param_names):
                        #Si la cantidad de parametros no es correcta se lanza un error
                        self.errors.append(SemanticError(f'La funcion {method.name} requiere {len(method.param_names)} cantidad de parametros pero {len(node.args)} fueron dados'))
                        return self.context.get_type('any')
                else:
                    self.errors.append(SemanticError(f'La funcion {node.id.id} no existe en este scope'))
                    return self.context.get_type('any')
            
                correct = True
                #Si la cantidad de parametros es correcta se verifica si los tipos de los parametros suministrados son correctos
                #Luego por cada parametro suministrado se verifica si el tipo del parametro suministrado es igual al tipo del parametro de la funcion
                for i in range(len(node.args)):
                    if not self.visit(node.args[i], scope).conforms_to(method.param_types[i].name):
                        self.errors.append(SemanticError(f'El tipo del parametro {i} no coincide con el tipo del parametro {i} de la funcion {node.id.id}.'))
                        correct = False
                #Si coinciden los tipos de los parametros entonces se retorna el tipo de retorno de la funcion en otro caso se retorna el tipo object
                return method.return_type if correct else self.context.get_type('any')
            else:
                
                args = [func for func in scope.find_functions(node.id.id) if len(func.param_names) == len(node.args)]
                if len(args) == 0:
                    self.errors.append(f'La funcion {node.id.id} requiere otra cantidad de parametros pero {len(node.args)} fueron suministrados')
                    return self.context.get_type('any')
                    #return args[0].return_type
                
                correct = True
                for i in range(len(node.args)):
                    if not self.visit(node.args[i], scope).conforms_to(args[0].param_types[i].name):
                        self.errors.append(SemanticError(f'El tipo del parametro {args[0].param_names[i]} no coincide con el tipo del parametro numero {i} de la funcion {node.id.id}.'))
                        correct = False
                #Si coinciden los tipos de los parametros entonces se retorna el tipo de retorno de la funcion en otro caso se retorna el tipo object
                return args[0].return_type if correct else self.context.get_type('any')
        except:
            self.errors.append(f'La funcion {node.id.id} no esta definida.')
            return self.context.get_type('any')
            
    @visitor.when(StringConcatNode)
    def visit(self, node: StringConcatNode, scope: Scope):
        typeLeft = self.visit(node.left, scope)
        typeRight = self.visit(node.right, scope)
        
        cfLeft = typeLeft.conforms_to('string')
        cfRight = typeRight.conforms_to('string')
        if (not cfLeft and not typeLeft.conforms_to('number')) or (not cfRight and not typeRight.conforms_to('number')):
            self.errors.append(SemanticError(f'Esta operacion solo puede ser aplicada a strings o entre una combinacion de string con number.'))
            return self.context.get_type('any')
        
        return self.context.get_type('string')
            
    @visitor.when(StringConcatWithSpaceNode)
    def visit(self, node: StringConcatWithSpaceNode, scope: Scope):
        typeLeft = self.visit(node.left, scope)
        typeRight = self.visit(node.right, scope)
        
        cfLeft = typeLeft.conforms_to('string')
        cfRight = typeRight.conforms_to('string')
        if (not cfLeft and not typeLeft.conforms_to('number')) or (not cfRight and not typeRight.conforms_to('number')):
            self.errors.append(SemanticError(f'Esta operacion solo puede ser aplicada a strings o entre una combinacion de string con number.'))
            return self.context.get_type('any')
        
        return self.context.get_type('string')
        
    @visitor.when(BoolCompAritNode)
    def visit(self, node: BoolCompAritNode, scope: Scope):
        if not self.visit(node.left, scope).conforms_to('number') or not self.visit(node.right, scope).conforms_to('number'):
            self.errors.append(SemanticError(f'Esta operacion solo puede ser aplicada a numeros.'))
            return self.context.get_type('any')
        
        return self.context.get_type('bool')
        
    @visitor.when(BoolNotNode)
    def visit(self, node: BoolNotNode, scope: Scope):
        if not self.visit(node.node, scope).conforms_to('bool'):
            self.errors.append(SemanticError(f'Esta operacion solo puede ser aplicada a booleanos.'))
            return self.context.get_type('any')
        
        return self.context.get_type('bool')
    
    @visitor.when(NumberNode)
    def visit(self, node: NumberNode, scope):
        # print("OnNumberNode")
        try:
            a: float = float(node.value)
            return self.context.get_type('number')
        except:
            self.errors.append(SemanticError(f'El elemento {node.value} no es un numero'))
            return self.context.get_type('any')
    
    @visitor.when(BlockNode)
    def visit(self, node: BlockNode, scope: Scope):
        inner_scope = scope.create_child()
        inner_type = self.context.get_type('any')
        
        for expression in node.list_non_create_statemnet:
            inner_type = self.visit(expression,inner_scope)
            
        return inner_type
        
    @visitor.when(InheritanceNode)
    def visit(self, node: InheritanceNode, scope: Scope):
        try:
            ret_type = self.context.get_type(node.type.id)
            if len(ret_type.args) != len(node.args):
                self.errors.append(SemanticError(f"El tipo {node.id} recibe {len(ret_type.args)} parametros para instanciarse"))
                return self.context.get_type("any")

            correct = True
            
            arg_types = [parama.type for parama in ret_type.args]
            arg_names = [parama.name for parama in ret_type.args]
            for i, arg in enumerate(arg_types):
                try:
                    temp_type = self.visit(node.args[i], scope)
                except:
                    self.errors.append(SemanticError(f"El tipo del argumento {arg_names[i]} es incorrecto a la hora de heredar de {ret_type.name}. Linea:{node.location[0]}"))
                    temp_type = self.context.get_type("any")
                    correct = False

                if not temp_type.conforms_to(ret_type.args[i].type.name):
                    self.errors.append(SemanticError(f"El tipo del argumento {arg_names[i]} es incorrecto a la hora de heredar de {ret_type.name}"))
                    correct = False
            return ret_type if correct else self.context.get_type("any")
        except:
            self.errors.append(SemanticError(f"El tipo {node.type.id} no esta definido. Linea:{node.location[0]} , Columna:{node.location[1]}"))
            return self.context.get_type("any")


    @visitor.when(StringNode)
    def visit(self, node: StringNode, scope):
        #print("OnStringNode")
        try:
            string = str(node.value)
            return self.context.get_type('string')
        except:
            return self.context.get_type('string')
        
    @visitor.when(BooleanNode)
    def visit(self, node: BooleanNode, scope):
        try:
            eval(node.value)
            return self.context.get_type('bool')
        except:
            return self.context.get_type('any')
        
    @visitor.when(BoolIsTypeNode)
    def visit(self, node: BoolIsTypeNode, scope: Scope):
        self.visit(node.left, scope)
        self.visit(node.right, scope)
        return self.context.get_type('bool')
        
    @visitor.when(IdentifierNode)
    def visit(self, node: IdentifierNode, scope: Scope):
        if scope.is_defined(node.id):
            return scope.find_variable(node.id).type
            
        self.errors.append(SemanticError(f'La variable {node.id} no esta definida'))
        return self.context.get_type('any')
    
    @visitor.when(CollectionNode)
    def visit(self, node: CollectionNode, scope):
        value = self.context.get_type('any')
        for item in node.collection:
            value = self.visit(item, scope)
            
        return value
        
    @visitor.when(SelfNode)
    def visit(self, node: SelfNode, scope: Scope):
        if not self.current_type:
            self.errors.append(SemanticError(f'La palabra self solo se puede usar dentro de clases'))
            return self.context.get_type('any')
        
        try: 
            return self.current_type.get_attribute(node.id.id).type
        except:
            self.errors.append(SemanticError(f'No existe un atributo {node.id.id} en la clase {self.current_type.name}'))
            return self.context.get_type('any')
        
    @visitor.when(PINode)
    def visit(self, node: PINode, scope: Scope):
        return self.context.get_type('number')