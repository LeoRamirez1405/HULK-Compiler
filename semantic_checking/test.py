import sys
import os
current_dir = os.getcwd()
sys.path.insert(0, current_dir)
from semantic_checking.ast_nodes import *
from semantic_checking.semantic_checking import SemanticCheckingVisitor

checker = SemanticCheckingVisitor()
# # ast = ProgramNode([IfStructureNode(BooleanNode(True, Token('True', 'Boolean', (0, 0))), None, None, None) , NumberNode(Token('5', int, (0,0)), 5)])

ast = ProgramNode([
    TypeDefinitionNode(
        token=Token(lex='if', token_type='.', location=(0,0)),
        identifier='A', 
        inheritance=None,
        attribute_definition=[], 
        method_definition=[
            FunctionDefinitionNode(
                token=Token(lex='func', token_type='.', location=(0,0)),
                identifier='f', 
                type_anotation='int',
                parameters=ArgNode(Token(lex='x', token_type='.', location=(0,0)),'x', 'type'),
                statement_list=[]
                )]
        )])
checker.visit(ast)

# def func():
#     def child_func(x):
#         print(f'child_func: {x}')
#     return child_func
    
# child_func = func()
# child_func(5)
    