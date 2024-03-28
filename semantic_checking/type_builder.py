import visitor
from AST import *
from cmp.semantic import *
class TypeBuilderVisitor():
    def __init__(self,context) -> None:
        self.context = context
        self.currentType: Type
        self.types_namesTypes = {}
    @visitor.on('node')
    def visit(self, node, tabs):
        pass
    
    def visit(self, node: ProgramNode):
        for classDef in node.classes:
            self.visit(classDef)

    @visitor.when(TypeDefinitionNode)
    def visit(self, node: TypeDefinitionNode):
        self.currentType = self.context.get_type(node.name) 
        for param in node.parameters:
            param = param[0]
            if param not in self.types_namesTypes.keys():
                self.types_namesTypes.update(param.key,param.value)
            else:
                if self.types_namesTypes[param.key] != param.value:
                    raise Exception(f'Param {param.key} already exists with another Type Definition')
                
        for attrDef in node.attributes:
            self.visit(attrDef)
        for methodDef in node.methods:
            self.visit(methodDef)
    
    @visitor.when(KernAssigmentNode)
    def visit(self, node: KernAssigmentNode):
        attr_type = self.context.get_type(node.type)
        self.current_type.define_attribute(node.name,attr_type)
      
    @visitor.when(FunctionDefinitionNode)
    def visit(self, node: FunctionDefinitionNode):
        return_type = self.context.get_type(node.return_type)
        arg_types = [self.context.get_type(t) for t in node.arg_types]
        self.current_type.defone_method( node.name, return_type, node.arg_names, arg_types)
