import cmp.visitor as visitor
from semantic_checking.AST import *

def get_formatter():

    class PrintVisitor(object):
        @visitor.on('node')
        def visit(self, node):
            pass

        @visitor.when(ProgramNode)
        def visit(self, node:ProgramNode):
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
            
            return f'if ({condition}):\n\t{body}\n\n{_elif}\n\n{_else}\n'

        @visitor.when(ElifStructureNode)
        def visit(self, node:ElifStructureNode):
            condition = self.visit(node.condition) 
            body = '\n\t'.join(self.visit(x) for x in node.body)
            return f'elif({condition}):\n\t{body}'

        @visitor.when(WhileStructureNode)
        def visit(self, node:WhileStructureNode):
            condition = self.visit(node.condition) 
            body = '\n\t'.join(self.visit(x) for x in node.body)
            return f'while({condition}):\n\t{body}'

        @visitor.when(ForStructureNode)
        def visit(self, node:ForStructureNode):
            condition = self.visit(node.condition)
            body = '\n\t'.join(self.visit(x) for x in node.body)
            init = self.visit(node.init_assigments)
            increment = self.visit(node.increment_condition)
            
            return f'for ({init} ; {condition} ; {increment}):\n\t{body}\n'        

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
        
         
        @visitor.when(SqrtMathNode)
        def visit(self, node:SqrtMathNode):
            return f'sqrt({self.visit(node.expression)})'
        
        @visitor.when(SinMathNode)
        def visit(self, node:SinMathNode):
            return f'sin({self.visit(node.expression)})'
        
        @visitor.when(CosMathNode)
        def visit(self, node:CosMathNode):
            return f'cos({self.visit(node.expression)})'

        @visitor.when(TanMathNode)
        def visit(self, node:TanMathNode):
            return f'tan({self.visit(node.expression)})'

        @visitor.when(ExpMathNode)
        def visit(self, node:ExpMathNode):
            return f'exp({self.visit(node.expression)})'

        @visitor.when(RandomCallNode)
        def visit(self, node:RandomCallNode):
            return f'rand()'

        @visitor.when(LogCallNode)
        def visit(self, node:LogCallNode):
            return f'log({self.visit(node.base)},{self.visit(node.expression)})'
        
        
        
        
        @visitor.when(BoolAndNode)
        def visit(self, node:BoolAndNode):
            return f'{self.visit(node.left)} and {self.visit(node.right)}'
        
        @visitor.when(BoolOrNode)
        def visit(self, node:BoolOrNode):
            return f'{self.visit(node.left)} or {self.visit(node.right)}'
        
        
        @visitor.when(BoolNotNode)
        def visit(self, node:BoolNotNode):
            return f'not {self.visit(node.node)}'
        
        @visitor.when(BoolCompEqualNode)
        def visit(self, node: BoolCompEqualNode):
            return f'{self.visit(node.left)} == {self.visit(node.right)}'

        @visitor.when(BoolCompNotEqualNode)
        def visit(self, node: BoolCompNotEqualNode):
            return f'{self.visit(node.left)} != {self.visit(node.right)}'


        @visitor.when(BoolCompGreaterEqualNode)
        def visit(self, node: BoolCompGreaterEqualNode):
            return f'{self.visit(node.left)} >= {self.visit(node.right)}'


        @visitor.when(BoolCompGreaterNode)
        def visit(self, node: BoolCompGreaterNode):
            return f'{self.visit(node.left)} > {self.visit(node.right)}'

        @visitor.when(BoolCompLessEqualNode)
        def visit(self, node: BoolCompLessEqualNode):
            return f'{self.visit(node.left)} <= {self.visit(node.right)}'

        @visitor.when(BoolCompLessNode)
        def visit(self, node: BoolCompLessNode):
            return f'{self.visit(node.left)} < {self.visit(node.right)}'
        
        
        @visitor.when(NumberNode)
        def visit(self, node:NumberNode):
            return f'{node.value}'
        
        @visitor.when(PINode)
        def visit(self, node:PINode):
            return f'{node.value}'

        @visitor.when(LetInExpressionNode)
        def visit(self, node: LetInExpressionNode):
            body = '\n\t'.join(self.visit(x) for x in node.body)
            return f'let {self.visit(node.assigments)} in {body}'
        
        @visitor.when(LetInNode)
        def visit(self, node: LetInNode):
            body = '\n\t'.join(self.visit(x) for x in node.body)
            return f'let {self.visit(node.assigments)} in {body}'
        
        @visitor.when(FunctionCallNode)
        def visit(self, node: FunctionCallNode):
            args = ','.join(self.visit(x) for x in node.args)
            return f'{self.visit(node.id)}({args})'
        
        @visitor.when(BooleanNode)
        def visit(self, node: BooleanNode):
            return f'{node.value}'
        
        
        @visitor.when(StringNode)
        def visit(self, node: StringNode):
            return f'{node.value}'
        
 
        @visitor.when(IdentifierNode)
        def visit(self, node: IdentifierNode):
            return f'{node.id}'
        
        @visitor.when(StringConcatNode)
        def visit(self, node: StringConcatNode):
            return f'{self.visit(node.left)} @ {self.visit(node.right)}'
        
        @visitor.when(StringConcatWithSpaceNode)
        def visit(self, node: StringConcatWithSpaceNode):
            return f'{self.visit(node.left)} @@ {self.visit(node.right)}'
        
        @visitor.when(BoolIsTypeNode)
        def visit(self, node: BoolIsTypeNode):
            return f'{self.visit(node.expression)} is {self.visit(node.type)}'
        
    printer = PrintVisitor()
    return (lambda ast: printer.visit(ast))