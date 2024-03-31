import visitor
from semantic import *
# from semantic_checking.AST import *
from AST import *

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
        #print('TypeBuilder')
        # print(f'Context in Builder: {[item for item in self.context.types.keys()]}')
        for classDef in node.statments:
            self.visit(classDef)

    @visitor.when(TypeDefinitionNode)
    def visit(self, node: TypeDefinitionNode):
        self.currentType: Type = self.context.get_type(node.id.id) 
        try:
            inheritance = self.context.get_type(inheritance.type)
        except:
            self.errors.append(SemanticError(f'El tipo  {node.inheritance} del que se hereda no esta definido'))
            inheritance = self.context.get_type('object')
        
        self.currentType.inhertance = inheritance
        
        for arg in node.parameters:
            name: IdentifierNode = arg.items[0].key 
            type = arg.items[0].value
            
            type =  self.context.get_type(type)
            try:
                self.currentType.define_arg(name.id, type)      
            except:
                self.errors.append(f'Existenten dos argumentos con el nombre {name.id}')
                
        for attrDef in node.attributes:
            self.visit(attrDef)
            
        for methodDef in node.methods:
            self.visit(methodDef)
            
        # Se actualiza el tipo para cuando vea luego algun metodo
        self.currentType = None
    
    @visitor.when(KernAssigmentNode)
    def visit(self, node: KernAssigmentNode):
        #TODO Ponerle type_annotation al kernassigmentnode
        #node_id: IdentifierNode = node.id
        self.currentType.define_attribute(node.id.id, self.context.get_type('object'))    
        
    @visitor.when(FunctionDefinitionNode)
    def visit(self, node: FunctionDefinitionNode):
        try: 
            type_annotation: TypeNode = node.type_annotation
            return_type = self.context.get_type(type_annotation.type)
        except:
            self.errors.append(f'El tipo de retorno {node.type_annotation.type} no esta definido')
            return_type = self.context.get_type('object')
        
        arg_names: List[IdentifierNode] = [parama.items[0].key for parama in node.parameters]
        arg_names = [name.id for name in arg_names]
        arg_types = []
        
        for parama in node.parameters:
            try:
                arg_types.append(self.context.get_type(parama.items[0].value))
            except:
                self.errors.append(f'El tipo del parametro {parama.items[0].key} que se le pasa a la funcion {node.id.id} no esta definido')
                arg_types.append(self.context.get_type('object'))
        
        #node_id: IdentifierNode = node.id
        if self.currentType:
            try:
                self.currentType.define_method(node.id.id, arg_names, arg_types, return_type)
            except:
                self.errors.append(f'La funcion {node.id.id} ya existe en el contexto de {self.currentType.name}.')
        else:
            exist = False
            #Esto nnunca va a lanzar excepcion xq solo entraria a este nodo si es un metodo de un typo o si ya esta node.id en el scope
            for func in self.scope.functions[node.id.id]:
                if len(arg_names) == len(func.param_names):
                    exist = True
                    break
            if exist:
                self.errors.append(f'La funcion {node.id.id} ya existe en este scope con {len(arg_names)} cantidad de parametros')
            else:
                method = Method(node.id.id, arg_names, arg_types, return_type)
                self.scope.functions[node.id.id].append(method)
                

  