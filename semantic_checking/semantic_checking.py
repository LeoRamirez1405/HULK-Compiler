from semantic_checking.semantic import Context, Scope
from semantic_checking.type_collector import TypeCollectorVisitor
from semantic_checking.type_builder import TypeBuilderVisitor
from semantic_checking.type_checker import TypeCheckerVisitor
from semantic_checking.AST import *

class SemanticCheckingVisitor:
    def __init__(self) -> None:
    #------------------Inicializando tipos por defecto---------------------------------------------------#
        self.context = Context()
        self.context.create_type('object')
        default_types = ['number', 'string', 'bool', 'void', 'any']
        for type in default_types:
            self.context.create_type(type) 
            self.context.get_type(type).parent = self.context.get_type('object') 
    
    #------------------Inicializando funciones por defecto-----------------------------------------------#
        self.scope = Scope(parent=None)
        
        #TODO Se puedo no poner estas funciones como definidas y desde la gramatica crear un SqrNode() y luego acceder a el
        self.default_functions = ['sin', 'cos', 'sqrt', 'exp', 'tan', 'rand', 'log', 'print']
    
    #----------------------------------------------------------------------------------------------------# 
        self.errors = []

        
    #TODO Pasar a los collectors copias de context scope y errors
    def semantic_checking(self, ast):
        print()
        type_collector = TypeCollectorVisitor(self.context, self.errors)
        type_collector.visit(ast)
        
        type_builder = TypeBuilderVisitor(self.context, self.scope, self.errors)
        type_builder.visit(ast)
        
        type_checker = TypeCheckerVisitor(self.context, self.scope, self.errors, self.default_functions)
        type_checker.visit(ast)
        
        # print('Context')
        # for name, type in self.context.types.items():
        #     print(f'Type: {name}')
        #     if type.parent: print(f': {type.parent.name}')
        #     print(f'attributes: {[attr.name for attr in type.attributes]}')
        #     print(f'attributes: {[method.name for method in type.methods]}')
            
    
        return self.errors
                      
# ast0 = ProgramNode([NumberNode(42)])
# ast1 = ProgramNode([PrintStatmentNode(NumberNode(42))])
# ast2 = ProgramNode([PrintStatmentNode(DivExpressionNode(MultExpressionNode(PowExpressionNode(PlusExpressionNode(NumberNode(1), NumberNode(2)), NumberNode(3)), NumberNode(4)), NumberNode(5)))])
# ast3 = ProgramNode([PrintStatmentNode(StringNode('Hello World'))])
# ast4 = ProgramNode([PrintStatmentNode(StringNode(StringConcatWithSpaceNode(StringNode('The meaning of life is'), NumberNode(42))))])
# ast5 = ProgramNode([
#             PrintStatmentNode(
#                 PlusExpressionNode(
#                     PowExpressionNode(
#                         SinMathNode(
#                             MultExpressionNode(
#                                 NumberNode(2), 
#                                 PINode()
#                                 )
#                             ), 
#                         NumberNode(2)
#                         ), 
#                     CosMathNode(
#                         DivExpressionNode(
#                             MultExpressionNode(
#                                 NumberNode(3), 
#                                 PINode()
#                                 ), 
#                             LogCallNode(
#                                 NumberNode(4), 
#                                 NumberNode(64)
#                                 )
#                             )
#                         )
#                     )
#                 )
#             ])
# ast6 = ProgramNode([
#     PrintStatmentNode(NumberNode(45)),
#     TypeDefinitionNode(
#         id=IdentifierNode('Point'), 
#         parameters=[],
#         inheritance=TypeNode('object'),
#         attributes=[
#             KernAssigmentNode(IdentifierNode('x'), TypeNode('number')),
#             ],
#         methods=[
#             FunctionDefinitionNode(
#                 IdentifierNode('setX'),
#                 TypeNode('number'),
#                 [],
#                 PlusExpressionNode(NumberNode(4), NumberNode(5))
#             )]
#         ),
#     FunctionDefinitionNode(
#                 id=IdentifierNode('global_func'),
#                 type_annotation=TypeNode('Point'),
#                 parameters=[],
#                 body=PlusExpressionNode(NumberNode(4), NumberNode(5))
#             ),
#     SqrtMathNode(StringNode('arbol'))
#     ])
# ast7 = ProgramNode([
#     KernAssigmentNode(IdentifierNode('x'), NumberNode(5)),
#     KernAssigmentNode(IdentifierNode('y'), PlusExpressionNode(NumberNode(9), IdentifierNode('x'))),
# ])
# ast8 = ProgramNode([
    
# ])
# # Trata de definir una variable ya definifa
# ast9 = ProgramNode([
#     KernAssigmentNode(IdentifierNode('x'), NumberNode(5)),
#     KernAssigmentNode(IdentifierNode('x'), PlusExpressionNode(NumberNode(9), IdentifierNode('x'))),
# ])
# # Trata de utilizar una variable que no esta definida
# ast10 = ProgramNode([
#     KernAssigmentNode(IdentifierNode('x'), NumberNode(5)),
#     KernAssigmentNode(IdentifierNode('y'), PlusExpressionNode(NumberNode(9), IdentifierNode('z'))),
# ])
# ast11 = ProgramNode([
#     KernAssigmentNode(IdentifierNode('x'), NumberNode(5)),
#     KernAssigmentNode(IdentifierNode('y'), PlusExpressionNode(NumberNode(9), IdentifierNode('x'))),
#     FunctionDefinitionNode(
#         IdentifierNode('method'), 
#         TypeNode('number'), 
#         [{IdentifierNode('a'): TypeNode('number')}, {IdentifierNode('b'): TypeNode('number')}],
#         [PlusExpressionNode(IdentifierNode('x'), IdentifierNode('y'))]
#     )
# ])

# print_aritmetic_tests = [ast0, ast1, ast2, ast3, ast4, ast5, ast6]
# for index_test in range(len(print_aritmetic_tests)):
#     print(f'Test - {index_test}')
#     checker = SemanticCheckingVisitor()
#     if index_test != 7:
#         continue
#     errors = checker.semantic_checking(print_aritmetic_tests[index_test])
#     print(len(errors))
#     print(errors)


# checker = SemanticCheckingVisitor()  
# errors = checker.semantic_checking(ast)
# print(errors)