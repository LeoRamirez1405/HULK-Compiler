from semantic import Context, Scope, Method
from type_collector import TypeCollectorVisitor
from type_builder import TypeBuilderVisitor
from type_checker import TypeCheckerVisitor
from AST import *

class SemanticCheckingVisitor:
    def __init__(self) -> None:
    #------------------Inicializando tipos por defecto---------------------------------------------------#
        self.context = Context()
        default_types = ['object', 'number', 'string', 'bool', 'void']
        for type in default_types:
            self.context.create_type(type)  
            
        print(f'Context: {[item for item in self.context.types.keys()]}') 
    
    #------------------Inicializando funciones por defecto-----------------------------------------------#
        self.scope = Scope(parent=None)
        
        #TODO Se puedo no poner estas funciones como definidas y desde la gramatica crear un SqrNode() y luego acceder a el
        self.default_functions = ['sen', 'cos', 'sqrt', 'exp']
        # for func in self.default_functions:
        #     self.scope.functions[func] = Method(func, ['expression'], [self.context.get_type('number')], self.context.get_type('number'))
            
        self.default_functions.extend(['rand', 'log', 'print'])
        # self.scope.functions['rand'] = [Method(func, [], [], self.context.get_type('number'))]
        # self.scope.functions['log'] = [Method(func, ['base', 'expression'], [self.context.get_type('number'), self.context.get_type('number')], self.context.get_type('number'))]
        # self.scope.functions['print'] = [Method(func, ['expression'], [self.context.get_type('object')], self.context.get_type('string'))]

    #----------------------------------------------------------------------------------------------------# 
        self.errors = []

        
    #TODO Pasar a los collectors copias de context scope y errors
    def semantic_checking(self, ast):
        type_collector = TypeCollectorVisitor(self.context, self.scope, self.errors)
        type_collector.visit(ast)
        
        type_builder = TypeBuilderVisitor(self.context, self.scope, self.errors)
        type_builder.visit(ast)
        
        type_checker = TypeCheckerVisitor(self.context, self.scope, self.errors, self.default_functions)
        type_checker.visit(ast)
        
        # print('Context')
        # for name, type in self.context.types.items():
        #     print(f'Type: {name}')
        #     print(f'attributes: {type.attributes}')
        #     print(f'attributes: {type.methods}')
            
    
        return self.errors
                      
ast0 = NumberNode(42)
ast1 = PrintStatmentNode(NumberNode(42))
ast2 = PrintStatmentNode(DivExpressionNode(MultExpressionNode(PowExpressionNode(PlusExpressionNode(NumberNode(1), NumberNode(2)), NumberNode(3)), NumberNode(4)), NumberNode(5)))
ast3 = PrintStatmentNode(StringNode('Hello World'))
ast4 = PrintStatmentNode(StringNode(StringConcatWithSpaceNode(StringNode('The meaning of life is'), NumberNode(42))))
ast5 = PrintStatmentNode(PlusExpressionNode(PowExpressionNode(SinMathNode(MultExpressionNode(NumberNode(2), PINode())), NumberNode(2)), CosMathNode(DivExpressionNode(MultExpressionNode(NumberNode(3), PINode()), LogCallNode(NumberNode(4), NumberNode(64))))))
ast = ProgramNode([
    PrintStatmentNode(NumberNode(45)),
    TypeDefinitionNode(
        id='Point', 
        parameters=[],
        inheritance=TypeNode('object'),
        attributes=[
            KernAssigmentNode('x', TypeNode('number')),
            ],
        methods=[
            FunctionDefinitionNode(
                'setX',
                TypeNode('number'),
                [],
                PlusExpressionNode(NumberNode(4), NumberNode(5))
            )]
        ),
    FunctionDefinitionNode(
                'global_func',
                TypeNode('Point'),
                [],
                PlusExpressionNode(NumberNode(4), NumberNode(5))
            ),
    SqrtMathNode(StringNode('arbol'))
    ])

print_aritmetic_tests = [ast0, ast1, ast2, ast3, ast4, ast5]
for index_test in range(len(print_aritmetic_tests)):
    print(f'Test - {index_test}')
    checker = SemanticCheckingVisitor()
    errors = checker.semantic_checking(print_aritmetic_tests[index_test])
    print(len(errors))
    print(errors)


#TODO OJO Los inhertance y los type_annotation son de tipo TypeNode