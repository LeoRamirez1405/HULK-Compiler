import cmp.visitor as visitor
from semantic_checking.AST import *

def get_formatter():

    class PrintVisitor(object):
        @visitor.on('node')
        def visit(self, node):
            pass

        @visitor.when(ProgramNode)
        def visit(self, node):
            statements = '\n\n'.join(self.visit(t) for t in node.statments)
            return f'{statements}'

        @visitor.when(PrintStatmentNode)
        def visit(self, node):
            expression = self.visit(node.expression)
            return f'print({expression})'

        @visitor.when(FunctionDefinitionNode)
        def visit(self, node):
            id = self.visit(node.id)
            type_annotation = self.visit(node.type_annotation)
            parameters = ','.join(self.visit(x) for x in node.parameters)
            body = '\n\t'.join(self.visit(x) for x in node.body)

            return f'function {id}:{type_annotation} ({parameters}){{\n\t{body}\n}}'
        
        @visitor.when(TypeNode)
        def visit(self, node:TypeNode):
            expression = self.visit(node.type)
            return f'{expression}'
        
        @visitor.when(IfStructureNode)
        def visit(self, node:IfStructureNode):
            condition = self.visit(node.condition)
            body = '\n\t'.join(self.visit(x) for x in node.body)
            _elif = self.visit(node._elif)
            _else = self.visit(node._else)
            
            return f'if {condition}:\n\t{body}\n\n elif: \n\t{_elif}\n\n else:\n\t {_else}\n'

        @visitor.when(ParamNode)
        def visit(self, node):
            return f'PARAM {node.name}'

        @visitor.when(LocalNode)
        def visit(self, node):
            return f'LOCAL {node.name}'

        @visitor.when(KernAssigmentNode)
        def visit(self, node:KernAssigmentNode):
            return f'{self.visit(node.id)} = {self.visit(node.expression)}'
        
        
        @visitor.when(DestroyNode)
        def visit(self, node:DestroyNode):
            return f'{self.visit(node.id)} = {self.visit(node.expression)}'

        @visitor.when(PlusExpressionNode)
        def visit(self, node):
            return f'{self.visit(node.id)} + {self.visit(node.expression)}'

        @visitor.when(SubsExpressionNode)
        def visit(self, node):  
            return f'{self.visit(node.id)} - {self.visit(node.expression)}'

        @visitor.when(MultExpressionNode)
        def visit(self, node):
            return f'{self.visit(node.id)} * {self.visit(node.expression)}'

        @visitor.when(DivExpressionNode)
        def visit(self, node):
            return f'{self.visit(node.id)} / {self.visit(node.expression)}'
        
        @visitor.when(ModExpressionNode)
        def visit(self, node):
            return f'{self.visit(node.id)} % {self.visit(node.expression)}'
        
        @visitor.when(PowExpressionNode)
        def visit(self, node):
            return f'{self.visit(node.id)} ^ {self.visit(node.expression)}'
        
        @visitor.when(BoolAndNode)
        def visit(self, node:BoolAndNode):
            return f'{self.visit(node.left)} and {self.visit(node.right)}'
        
        @visitor.when(BoolOrNode)
        def visit(self, node:BoolOrNode):
            return f'{self.visit(node.left)} or {self.visit(node.right)}'
        
        
        @visitor.when(BoolNotNode)
        def visit(self, node:BoolNotNode):
            return f'{self.visit(node.node)}'

        @visitor.when(StarNode)
        def visit(self, node):
            return f'{node.dest} = {node.left} * {node.right}'

        @visitor.when(DivNode)
        def visit(self, node):
            return f'{node.dest} = {node.left} / {node.right}'

        @visitor.when(AllocateNode)
        def visit(self, node):
            return f'{node.dest} = ALLOCATE {node.type}'

        @visitor.when(TypeOfNode)
        def visit(self, node):
            return f'{node.dest} = TYPEOF {node.type}'

        @visitor.when(StaticCallNode)
        def visit(self, node):
            return f'{node.dest} = CALL {node.function}'

        @visitor.when(DynamicCallNode)
        def visit(self, node):
            return f'{node.dest} = VCALL {node.type} {node.method}'

        @visitor.when(ArgNode)
        def visit(self, node):
            return f'ARG {node.name}'

        @visitor.when(ReturnNode)
        def visit(self, node):
            return f'RETURN {node.value if node.value is not None else ""}'

    printer = PrintVisitor()
    return (lambda ast: printer.visit(ast))