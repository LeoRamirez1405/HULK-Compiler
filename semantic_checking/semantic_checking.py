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
            
        # print(f'Context: {[item for item in self.context.types.keys()]}') 
    
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
                      
ast0 = ProgramNode([NumberNode(42)])
ast1 = ProgramNode([PrintStatmentNode(NumberNode(42))])
ast2 = ProgramNode([PrintStatmentNode(DivExpressionNode(MultExpressionNode(PowExpressionNode(PlusExpressionNode(NumberNode(1), NumberNode(2)), NumberNode(3)), NumberNode(4)), NumberNode(5)))])
ast3 = ProgramNode([PrintStatmentNode(StringNode('Hello World'))])
ast4 = ProgramNode([PrintStatmentNode(StringNode(StringConcatWithSpaceNode(StringNode('The meaning of life is'), NumberNode(42))))])
ast5 = ProgramNode([
            PrintStatmentNode(
                PlusExpressionNode(
                    PowExpressionNode(
                        SinMathNode(
                            MultExpressionNode(
                                NumberNode(2), 
                                PINode()
                                )
                            ), 
                        NumberNode(2)
                        ), 
                    CosMathNode(
                        DivExpressionNode(
                            MultExpressionNode(
                                NumberNode(3), 
                                PINode()
                                ), 
                            LogCallNode(
                                NumberNode(4), 
                                NumberNode(64)
                                )
                            )
                        )
                    )
                )
            ])
ast6 = ProgramNode([
    PrintStatmentNode(NumberNode(45)),
    TypeDefinitionNode(
        id=IdentifierNode('Point'), 
        parameters=[],
        inheritance=TypeNode('object'),
        attributes=[
            KernAssigmentNode(IdentifierNode('x'), TypeNode('number')),
            ],
        methods=[
            FunctionDefinitionNode(
                IdentifierNode('setX'),
                TypeNode('number'),
                [],
                PlusExpressionNode(NumberNode(4), NumberNode(5))
            )]
        ),
    FunctionDefinitionNode(
                id=IdentifierNode('global_func'),
                type_annotation=TypeNode('Point'),
                parameters=[],
                body=PlusExpressionNode(NumberNode(4), NumberNode(5))
            ),
    SqrtMathNode(StringNode('arbol'))
    ])
ast7 = ProgramNode([
    KernAssigmentNode(IdentifierNode('x'), NumberNode(5)),
    KernAssigmentNode(IdentifierNode('y'), PlusExpressionNode(NumberNode(9), IdentifierNode('x'))),
])

# print_aritmetic_tests = [ast0, ast1, ast2, ast3, ast4, ast5, ast6]
# for index_test in range(len(print_aritmetic_tests)):
#     print(f'Test - {index_test}')
#     checker = SemanticCheckingVisitor()
#     if index_test != 7:
#         continue
#     errors = checker.semantic_checking(print_aritmetic_tests[index_test])
#     print(len(errors))
#     print(errors)

checker = SemanticCheckingVisitor()  
errors = checker.semantic_checking(ast7)
