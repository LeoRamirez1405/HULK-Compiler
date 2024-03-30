import visitor
from AST import *
from semantic import *

class TypeBuilderVisitor():
    def __init__(self,context:Context, scope: Scope, errors) -> None:
        self.context: Context = context
        self.scope: Scope = scope
        self.errors: List[str] = errors
        self.currentType: Type
        
    @visitor.on('node')
    def visit(self, node, tabs):
        pass
    
    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode):
        for statment in node.statments:
            self.visit(statment)

    @visitor.when(TypeDefinitionNode)
    def visit(self, node: TypeDefinitionNode):
        self.currentType: Type = self.context.get_type(node.id) 
        
        for arg in node.parameters:
            name = arg[0].key 
            type = arg[0].value
            
            type =  self.context.get_type(type)
            try:
                self.currentType.define_arg(name, type)      
            except:
                self.errors.append(f'Existenten dos argumentos con el nombre {name}')
                
        for attrDef in node.attributes:
            self.visit(attrDef)
            
        for methodDef in node.methods:
            self.visit(methodDef)
            
        # Se actualiza el tipo para cuando vea luego algun metodo
        self.currentType = None
    
    @visitor.when(KernAssigmentNode)
    def visit(self, node: KernAssigmentNode):
        #TODO Ponerle type_annotation al kernassigmentnode
        self.currentType.define_attribute(node.id, self.context.get_type('object'))    
        
    @visitor.when(FunctionDefinitionNode)
    def visit(self, node: FunctionDefinitionNode):
        try: 
            return_type = self.context.get_type(node.type_annotation)
        except:
            self.errors.append(f'El tipo de retorno {node.type_annotation} no esta definido')
            return_type = self.context.get_type('object')
        
        arg_names = [parama.items[0].key for parama in node.parameters]
        arg_types = []
        
        for parama in node.parameters:
            try:
                arg_types.append(self.context.get_type(parama.items[0].value))
            except:
                self.errors.append(f'El tipo del parametro {parama.items[0].key} que se le pasa a la funcion {node.id} no esta definido')
                arg_types.append(self.context.get_type('object'))
        
        if self.currentType:
            try:
                self.currentType.define_method(node.id, arg_names, arg_types, return_type)
            except:
                self.errors.append(f'La funcion {node.id} ya existe en el contexto de {self.currentType.name}.')
        else:
            exist = False
            #Esto nnunca va a lanzar excepcion xq solo entraria a este nodo si es un metodo de un typo o si ya esta node.id en el scope
            for func in self.scope.functions[node.id]:
                if len(arg_names) == len(func.param_names):
                    exist = True
                    break
            if exist:
                self.errors.append(f'La funcion {node.id} ya existe en este scope con {len(arg_names)} cantidad de parametros')
            else:
                method = Method(node.id, arg_names, arg_types, return_type)
                self.scope.functions[node.id].append(method)
                

  