from AST import *
import visitor
from semantic import Context, Scope, SemanticError, Method, Type
from type_collector import TypeCollectorVisitor
from type_builder import TypeBuilderVisitor

class SemanticCheckingVisitor:
    def __init__(self) -> None:
        #------------------Inicializando tipos por defecto---------------------------------------------------#
        self.context = Context()
        default_types = ['object', 'number', 'string', 'bool']
        for type in default_types:
            self.context.create_type(type)
            
        #------------------Inicializando funciones por defecto-----------------------------------------------#
        self.scope = Scope()
        self.default_functions = ['print', 'sen', 'cos', 'sqrt', 'exp']
        for func in self.default_functions:
            self.scope.functions.update(func, [1])
            
        self.default_functions.extend(['rand', 'log'])
        self.scope.functions.update('rand',[0])
        self.scope.functions.update('log',[2])
        
        #----------------------------------------------------------------------------------------------------#
        
        self.errors = []
        print('inicializando checker visitor') #* ✔ 
    
    @visitor.on('node')
    def visit(self, node, scope):
        pass
    
    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode, scope=None):
        
        type_collector = TypeCollectorVisitor(self.context, self.errors)
        type_collector.visit(node)
        
        type_builder = TypeBuilderVisitor
        type_builder.visit(node)
        
        for statment in node.statments:
            self.visit(statment, self.scope)  
                      
    @visitor.when(PrintStatmentNode)
    def visit(self, node: PrintStatmentNode, scope):
        self.visit(node.expression, scope)
    
    @visitor.when(DestroyNode)
    def visit(self, node: DestroyNode, scope: Scope):
        if not scope.is_defined(node.id):
            self.errors.append(SemanticError(f'La variable {node.id} no esta definida en este scope'))
            
        self.visit(node.expression, scope)
        
    @visitor.when(LetNode)
    def visit(self, node: LetNode, scope: Scope):
        if scope.is_local(node.id) or scope.is_defined(node.id):
            self.errors.append(SemanticError(f'La variable {node.id} ya esta definida.'))
        else:
            scope.define_variable(node.id, self.context.get_type('object'))
            self.visit(node.expression, scope)
        
    # #TODO Revisar esto y ver si se modifica la gramatica y donde quiera que se cree un TypeNode podemos crear un Type(type_anotation)
    # @visitor.when(TypeNode)
    # def visit(self, node: TypeNode, scope):
    #     try:
    #         self.context.types[node.type]
    #     except:
    #         self.errors.append(SemanticError(f'Tipo no definido'))
            
    @visitor.when(FunctionDefinitionNode)
    def visit(self, node: FunctionCallNode, scope: Scope):
        if node.id in self.default_functions:
            self.errors.append(SemanticError(f'Esta redefiniendo una funcion {node.id} que esta definida por defecto en el lenguaje y no se puede sobreescribir'))
            return
        try:
            args_len_list = scope.functions[id]
            if  len(node.args) in args_len_list:
                self.errors.append(SemanticError(f'La funcion {node.id} ya esta definida con {len(node.args)} cantidad de parametros.'))
        except:
            #TODO Se puede instanciar la clase Method de semantic~seria algo similar a scope.functions[node.id] = nodmethod(node. ...)
            #* Por el momento en el diccionario tengo el id de la funcion con su cantidad de parametros
            scope.functions[node.id].append(len(node.args))
            
    @visitor.when(IfStructureNode)
    def visit(self, node: IfStructureNode, scope: Scope):
        self.visit(node.condition)
        inner_scope = scope.create_child(scope)
        for statment in node.body:
            self.visit(statment, inner_scope)
        
        for _elif in node._elif:        
            self.visit(_elif, scope)
        
        self.visit(node._else, scope)
        
    @visitor.when(ElifStructureNode)
    def visit(self, node: ElifStructureNode, scope: Scope):
        self.visit(node.condition)
        inner_scope = scope.create_child(scope)
        for statment in node.body:
            self.visit(statment, inner_scope)
        
    @visitor.when(ElseStructureNode)
    def visit(self, node: ElseStructureNode, scope: Scope):
        inner_scope = scope.create_child(scope)
        for statment in node.body:
            self.visit(statment, inner_scope)
        
    @visitor.when(WhileStructureNode)
    def visit(self, node: WhileStructureNode, scope: Scope):
        self.visit(node.condition, scope)
        inner_scope = scope.create_child(scope)
        for statment in node.body:
            self.visit(statment, inner_scope)
            
    @visitor.when(ForStructureNode)
    def visit(self, node: ForStructureNode, scope: Scope):
        inners_scope: Scope = scope.create_child(scope)
        for id, expr in node.init_assigments:
            if scope.is_defined(node.id):
                self.errors.append(SemanticError(f'La variable {id} ya esta definida en este scope.'))
            inners_scope.define_variable(id, Type('object'))
            
        self.visit(node.body, inners_scope)
        
        for increment_assigment in node.increment_condition:
            self.visit(increment_assigment, inners_scope)
            
    @visitor.when(TypeDefinitionNode)
    def visit(self, node: TypeDefinitionNode, scope: Scope):
        inner_scope: Scope = scope.create_child(scope)
        for arg, type_att in node.parameters:
            inner_scope.define_variable(arg, type_att)
            
        for att in node.attribute:
            inner_scope.define_variable(att, Type('object'))
            
        for method in node.methods:
            self.visit(method, inner_scope)
            
    @visitor.when(InstanceCreationNode)
    def visit(self, node: InstanceCreationNode, scope: Scope):
        if scope.is_local(node.id) or scope.is_defined(node.id):
            self.errors.append(SemanticError(f'El nombre de varible {node.id} ya ha sido tomado.'))
        
        #TODO Verificar la correctitud 
        for arg in node.arguments:
            self.visit(arg, scope)
            
    @visitor.when(KernInstanceCreationNode)
    def visit(self, node: KernInstanceCreationNode, scope: Scope):
        for arg in node.args:
            self.visit(arg, scope)
            
    @visitor.when(MemberAccesNode)
    def visit(self, node: MemberAccesNode, scope: Scope):
        self.visit(node.base_object)
        for args in node.args:
            self.visit(args)
            
    @visitor.when(BooleanExpression)
    def visit(self, node: BooleanExpression, scope: Scope):
        self.visit(node.expression_1)
        self.visit(node.expressiin_2)
        
    @visitor.when(AritmeticExpression)
    def visit(self, node: AritmeticExpression, scope: Scope):
        self.visit(node.expression_1)
        self.visit(node.expression_2)
        
    @visitor.when(MathOperationNode)
    def visit(self, node: SqrtMathNode, scope: Scope):
        self.visit(node.expression)
        
    @visitor.when(LogCallNode)
    def visit(self, node: LogCallNode, scope: Scope):
        self.visit(node.base, scope)
        self.visit(node.expression, scope)
        
    @visitor.when(LetInNode)
    def visit(self, node: LetInNode, scope: Scope):
        inner_scope = scope.create_child(scope)
        for assign in node.assigments:
            self.visit(assign, inner_scope)
            
        self.visit(node.body, inner_scope)
            
    @visitor.when(FunctionCallNode)
    def visit(self, node: FunctionCallNode, scope: Scope):
        try: 
            args_len = scope.functions[id]
            if args_len != len(node.args):
                self.errors.append(f'La funcion {id} requiere {args_len} cantidad de parametros pero solo {len(node.args)} fueron dados')
        except:
            self.errors.append(f'La funcion {node.id} no esta definida.')
            
    @visitor.when(StringConcatWithSpaceNode)
    def visit(self, node: StringConcatWithSpaceNode, scope: Scope):
        self.visit(node.left, scope)
        self.visit(node.right, scope)
        
    @visitor.when(BoolCompAritNode)
    def visit(self, node: BoolCompAritNode, scope: Scope):
        self.visit(node.left, scope)
        self.visit(node.right, scope)
        
    @visitor.when(BoolNotNode)
    def visit(self, node: BoolNotNode, scope: Scope):
        self.visit(node.node)
    
    
            
    