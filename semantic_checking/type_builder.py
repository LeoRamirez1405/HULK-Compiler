import visitor
from AST import *
from semantic import *

class TypeBuilderVisitor():
    def __init__(self,context:Context) -> None:
        self.context = context
        self.currentType: Type
        
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
            
        
       # self.currentType.attributes(arg_types)
        for attrDef in node.attribute:
            self.visit(attrDef)
        for methodDef in node.methods:
            self.visit(methodDef)
    
    @visitor.when(KernAssigmentNode)
    def visit(self, node: KernAssigmentNode):
        attr_type = self.context.get_type(node.id)
        if self.currentType.get_attribute(node.id,attr_type) is not None: 
            self.currentType.define_attribute(node.id,attr_type)
            
    @visitor.when(FunctionDefinitionNode)
    def visit(self, node: FunctionDefinitionNode):
        return_type = self.context.get_type(node.type_annotation)
        arg_types = [self.context.get_type(t[0].value) for t in node.parameters]
        arg_names = [t[0].key for t in node.parameters]
        self.currentType.define_method(node.id, arg_names, arg_types, return_type)
        