from semantic_checking.semantic import *
import semantic_checking.visitor as visitor
from semantic_checking.AST import *
# from AST import *

class TypeBuilderVisitor():
    def __init__(self,context:Context, scope: Scope, errors) -> None:
        self.context: Context = context
        self.scope: Scope = scope
        self.errors: List[str] = errors
        self.currentType: Type = None
        
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
            name: IdentifierNode = list(arg.items())[0][0]
            type = list(arg.items())[0][1]
            
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
        if self.currentType:
            self.currentType.define_attribute(node.id.id, self.context.get_type('object'))    
        
    @visitor.when(FunctionDefinitionNode)
    def visit(self, node: FunctionDefinitionNode):
        try: 
            type_annotation: TypeNode = node.type_annotation
            return_type = self.context.get_type(type_annotation.type)
        except:
            self.errors.append(f'El tipo de retorno {node.type_annotation.type} no esta definido')
            return_type = self.context.get_type('object')
        
        arg_names: List[IdentifierNode] = [list(parama.items())[0] for parama in node.parameters]
        arg_names = [name[0].id for name in arg_names]
        print(arg_names)
        arg_types = []
        
        aux = [list(parama.items())[0] for parama in node.parameters]
        aux = [name for name in aux]
        print(aux)
        for parama in aux:
            try:
                arg_types.append(self.context.get_type(parama[1].type))
            except:
                self.errors.append(f'El tipo del parametro {parama[0].id} que se le pasa a la funcion {node.id.id} no esta definido')
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
                

  