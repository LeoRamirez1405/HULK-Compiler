import visitor
from AST import *
from semantic import *

class TypeBuilderVisitor():
    def __init__(self,context:Context, scope: Scope, errors) -> None:
        self.context = context
        self.scope = scope
        self.errors: List[str] = errors
        self.currentType: Type
        self.args = dict
        
    @visitor.on('node')
    def visit(self, node, tabs):
        pass
    
    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode):
        for classDef in node.statments:
            self.visit(classDef)

    @visitor.when(TypeDefinitionNode)
    def visit(self, node: TypeDefinitionNode):
        self.currentType = self.context.get_type(node.id) 
        arg_types = [self.context.get_type(t[0].value) for t in node.parameters]
        
        arg_names = [self.context.get_type(t[0].key) for t in node.parameters]
        
        for i in range(arg_names):
            self.currentType.define_attribute(arg_names[i],arg_types[i])        
            self.args.update(self.currentType.name, self.currentType)       
            
        
       # self.currentType.attributes(arg_types)
        for attrDef in node.attribute:
            self.visit(attrDef)
        for methodDef in node.methods:
            self.visit(methodDef)
            
        # Se actualiza el tipo para cuando vea luego algun metodo
        self.currentType = None
    
    @visitor.when(KernAssigmentNode)
    def visit(self, node: KernAssigmentNode):
        if node.id in self.args:    
            self.currentType.define_attribute(node.id,self.args[node.id])
        else:
            attr_type = self.context.get_type(node.id)
            if self.currentType.get_attribute(node.id,attr_type) is not None: 
                self.currentType.define_attribute(node.id,attr_type)
            else:
                self.currentType.define_attribute(node.id,Type('object'))    
        
    @visitor.when(FunctionDefinitionNode)
    def visit(self, node: FunctionDefinitionNode):
        return_type = self.context.get_type(node.type_annotation)
        arg_types = [self.context.get_type(t[0].value)  if t[0].value in self.context else Type('object') for t in node.parameters]
        arg_names = [t[0].key for t in node.parameters]
        if self.currentType:
            try:
                self.currentType.define_method(node.id, arg_names, arg_types, return_type)
            except:
                self.errors.append(f'La funcion {node.id} ya existe en el contexto de {self.currentType.name}.')
        else:
            exist = True
            for func in self.scope.functions[node.id]:
                if len(arg_names) == len(func.param_names):
                    exist = True
                    break
            if exist:
                self.errors.append(f'La funcion {node.id} ya existe en este scope con {len(arg_names)} cantidad de parametros')
            else:
                method = Method(node.id, [name for name, type in node.parameters], [type for name, type in node.parameters], return_type)
                self.scope.functions[node.id].append(method)
                

  