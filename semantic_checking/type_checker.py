from semantic_checking.semantic import *
import semantic_checking.visitor as visitor
from semantic_checking.AST import *
# from AST import *

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
            return self.context.get_type('any')
    
        if scope.is_local(node.id.id) or scope.is_defined(node.id.id):
            self.errors.append(SemanticError(f'La variable {node.id.id} ya esta definida.'))
        else:
            scope.define_variable(node.id.id, self.visit(node.expression, scope)) #* Aqui en el 2do parametro de la funcion se infiere el tipo de la expresion que se le va a asignar a la variable
            
        return self.context.get_type('any')
    
    #* Esto se usa a la hora de definir los parametros de una funcion que se esta creando
    @visitor.when(TypeNode)
    def visit(self, node: TypeNode, scope: Scope):
        try:
            return self.context.get_type(node.type)
        except:
            self.errors.append(SemanticError(f'Tipo {node.type} no esta definido'))
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
            method = list(filter(lambda x: len(x.param_names) == len(node.parameters), self.scope.functions[node.id.id]))[0]  
                   
        inner_scope: Scope = scope.create_child()            
        for i in range(len(method.param_names)):
            inner_scope.define_variable(method.param_names[i], method.param_types[i])
           
        # Visitar el cuerpo de la instruccion
        for statment in node.body: 
            self.visit(statment, inner_scope)
    
        return self.context.get_type('any')
            
    @visitor.when(IfStructureNode)
    def visit(self, node: IfStructureNode, scope: Scope):
        # verifico el tipo de la condicion y a la vez veo si las variables que estan dentro de ella estan ya definidas 
        if not self.visit(node.condition, scope).conforms_to('bool'):
            self.errors.append(SemanticError(f'La condicion del if debe ser de tipo bool'))
            
        inner_scope = scope.create_child()
        # Visitar el cuerpo de la instruccion
        for statment in node.body: 
            self.visit(statment, inner_scope)
        
        for _elif in node._elif:        
            self.visit(_elif, scope)
        
        self.visit(node._else, scope)
        
        #* En los nodos que no son expresiones aritmeticas o booleanas o concatenacion dberia ponerle qu etiene typo any?
        return self.context.get_type('any')
        
    @visitor.when(ElifStructureNode)
    def visit(self, node: ElifStructureNode, scope: Scope):
        if not self.visit(node.condition, scope).conforms_to('bool'):
            self.errors.append(SemanticError(f'La condicion del if debe ser de tipo bool'))
            
        inner_scope = scope.create_child()
        for statment in node.body:
            self.visit(statment, inner_scope)
            
        return self.context.get_type('any')
        
    @visitor.when(ElseStructureNode)
    def visit(self, node: ElseStructureNode, scope: Scope):
        inner_scope = scope.create_child()
        for statment in node.body:
            self.visit(statment, inner_scope)
            
        return self.context.get_type('any')
        
    @visitor.when(WhileStructureNode)
    def visit(self, node: WhileStructureNode, scope: Scope):
        if not self.visit(node.condition, scope).conforms_to('bool'):
            self.errors.append(SemanticError(f'La condicion del while debe ser de tipo bool'))
            
        inner_scope = scope.create_child()
        for statment in node.body:
            self.visit(statment, inner_scope)
            
        return self.context.get_type('any')
            
    @visitor.when(ForStructureNode)
    def visit(self, node: ForStructureNode, scope: Scope):
        inner_scope: Scope = scope.create_child()
        for assin in node.init_assigments:
            id, expr = assin.id.id, assin.expression
            
            if scope.is_defined(id):
                self.errors.append(SemanticError(f'La variable {id} ya esta definida en este scope.'))
            else:
                inner_scope.define_variable(id, self.visit(expr, inner_scope)) #* Aqui en el 2do parametro de la funcion se infiere el tipo de la expresion que se le va a asignar a la variable
            
        # Visitar el cuerpo de la instruccion
        for statment in node.body: 
            self.visit(statment, inner_scope)
        
        for increment_assigment in node.increment_condition:
            self.visit(increment_assigment, inner_scope)
            
        return self.context.get_type('any')
            
    @visitor.when(TypeDefinitionNode)
    def visit(self, node: TypeDefinitionNode, scope: Scope):
        self.current_type = self.context.get_type(node.id.id)
        temp_scope: Scope = scope.create_child()
        
        #* Creando un temp_scope me aseguro de que los argumentos del 'constructor' solo sean utiles a la hora de inicializar los atributos
        for param in node.parameters:
            arg, type_att = list(param.items())[0][0], list(param.items())[0][1]
            temp_scope.define_variable(arg, type_att)
            
        inner_scope = self.scope.create_child()
        for att in node.attributes:
            inner_scope.define_variable(att.id.id, self.visit(att.expression, temp_scope)) #* Aqui en el 2do parametro de la funcion se infiere el tipo de la expresion que se le va a asignar a la variable
            
        for method in node.methods:
            self.visit(method, inner_scope)
            
        self.current_type = None
        
        return self.context.get_type('any')
            
    @visitor.when(KernInstanceCreationNode)
    def visit(self, node: KernInstanceCreationNode, scope: Scope):
        correct = True
        try:
            class_type: Type = self.context.types[node.type.id]
            if len[class_type.attributes] != len(node.args):
                self.errors.append(SemanticError(f'La cantidad de argumentos no coincide con la cantidad de atributos de la clase {node.type}.'))
                correct = False
            else:
                for i in range(len(node.args)):
                    if not self.visit(node.args[i], scope).conforms_to(class_type.attributes[i].type):
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
            method = base_object_type.get_method(node.object_property_to_acces)
            #En caso de ser un metodo se verifica si la cantidad de parametros suministrados es correcta
            if len(node.args) != len(method.param_names):
                #Si la cantidad de parametros no es correcta se lanza un error
                self.errors.append(SemanticError(f'La funcion {method.name} requiere {len(method.param_names)} cantidad de parametros pero {len(node.args)} fueron dados'))
                return self.context.get_type('any')
            
            #Si la cantidad de parametros es correcta se verifica si los tipos de los parametros suministrados son correctos
            #Luego por cada parametro suministrado se verifica si el tipo del parametro suministrado es igual al tipo del parametro de la funcion
            for i in range(len(node.args)):
                correct = True
                if not self.visit(node.args[i], scope).conforms_to(method.param_types[i]):
                    self.errors.append(SemanticError(f'El tipo del parametro {i} no coincide con el tipo del parametro {i} de la funcion {node.object_property_to_acces}.'))
                    correct = False
            #Si coinciden los tipos de los parametros entonces se retorna el tipo de retorno de la funcion en otro caso se retorna el tipo object
            return method.return_type if correct else self.context.get_type('any')
        except: 
            #Si el id suministrado no es ni un atributo ni un metodo entonces se lanza un error y se retorna el tipo object
            self.errors.append(SemanticError(f'El objeto no tiene el metod llamado {node.object_property_to_acces}.'))
            return self.context.get_type('any')
            
    @visitor.when(BooleanExpression)
    def visit(self, node: BooleanExpression, scope: Scope):
        type_1: Type = self.visit(node.left, scope)
        type_2: Type = self.visit(node.right, scope)
        
        if not type_1.conforms_to(self.context.get_type('bool')) or not type_2.conforms_to(self.context.get_type('bool')):
            self.errors.append(SemanticError(f'Solo se pueden emplear operadores booleanos entre expresiones booleanas.'))
            return self.context.get_type('any')

        return type_1
        
    @visitor.when(AritmeticExpression)
    def visit(self, node: AritmeticExpression, scope: Scope):
        type_1: Type = self.visit(node.expression_1, scope)
        type_2: Type = self.visit(node.expression_2, scope)
        print('Operacion aritmetica')
        if not type_1.conforms_to('number') or not type_2.conforms_to('number'):
            print("Alguno no es un numero")
            self.errors.append(SemanticError(f'Solo se pueden emplear aritmeticos entre expresiones aritmeticas.'))
            return self.context.get_type('any')
        
        return type_1
        
    @visitor.when(MathOperationNode)
    def visit(self, node: MathOperationNode, scope: Scope):
        if not self.visit(node.expression, scope).conforms_to('number'):
            self.errors.append(SemanticError(f'Esta funcion solo puede ser aplicada a numeros.'))
            return self.context.get_type('any')
        
        return self.context.get_type('number')
        
    @visitor.when(LogCallNode)
    def visit(self, node: LogCallNode, scope: Scope):
        if not self.visit(node.base, scope).conforms_to('number') or not self.visit(node.expression, scope).conforms_to('number'):
            self.errors.append(SemanticError(f'Esta funcion solo puede ser aplicada a numeros.'))
            return self.context.get_type('any')
        
        return self.context.get_type('number')
        
    @visitor.when(LetInNode)
    def visit(self, node: LetInNode, scope: Scope):
        inner_scope = scope.create_child()
        for assign in node.assigments:
            self.visit(assign, inner_scope)
            
        self.visit(node.body, inner_scope)
        
        return self.context.get_type('any')
            
    @visitor.when(FunctionCallNode)
    def visit(self, node: FunctionCallNode, scope: Scope):
        try: 
            args = [func for func in scope.functions[node.id.id] if len(func.param_names) == len(node.args)]
            if len(args) == 0:
                self.errors.append(f'La funcion {node.id.id} requiere otra cantidad de parametros pero {len(node.args)} fueron suministrados')
                return args[0].return_type
        except:
            self.errors.append(f'La funcion {node.id.id} no esta definida.')
            return self.context.get_type('any')
            
    @visitor.when(StringConcatNode)
    def visit(self, node: StringConcatNode, scope: Scope):
        if (not self.visit(node.left, scope).conforms_to('string') and not self.visit(node.left, scope).conforms_to('number')) or ( not self.visit(node.right, scope).conforms_to('string') and not self.visit(node.right, scope).conforms_to('number')):
            self.errors.append(SemanticError(f'Esta operacion solo puede ser aplicada a strings o entre una combinacion de string con number.'))
            return self.context.get_type('any')
        
        return self.context.get_type('string')
            
    @visitor.when(StringConcatWithSpaceNode)
    def visit(self, node: StringConcatWithSpaceNode, scope: Scope):
        if (not self.visit(node.left, scope).conforms_to('string') and not self.visit(node.left, scope).conforms_to('number')) or (not self.visit(node.right, scope).conforms_to('string') and not self.visit(node.right, scope).conforms_to('number')):
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
        try:
            a: float = float(node.value)
            return self.context.get_type('number')
        except:
            self.errors.append(SemanticError(f'El elemento {node.value} no es un numero'))
            return self.context.get_type('any')
        
    @visitor.when(InheritanceNode)
    def visit(self, node: InheritanceNode, scope):
        try:
            return self.context.get_type(node.type)
        except:
            self.errors.append(SemanticError(f'El tipo {node.type} no esta definifo'))
            return self.context.get_type('any') 

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
            return self.context.get_type('any')
        
    @visitor.when(BoolIsTypeNode)
    def visit(self, node: BoolIsTypeNode, scope: Scope):
        return self.visit(node.left, scope).conforms_to(self.visit(node.right, scope))
        
    @visitor.when(IdentifierNode)
    def visit(self, node: IdentifierNode, scope: Scope):
        if self.scope.is_defined(node.id):
            return self.scope.find_variable(node.id).type
            
        self.errors.append(SemanticError(f'La variable {node.id} no esta deifinida'))
        return self.context.get_type('any')
        