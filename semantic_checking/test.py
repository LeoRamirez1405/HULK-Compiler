import sys
import os
current_dir = os.getcwd()
sys.path.insert(0, current_dir)


from AST import *
from semantic_checking.semantic_checking import SemanticCheckingVisitor
from evaluation import evaluate_reverse_parse
from grammLR1 import gramm_Hulk_LR1
from LR1 import LR1Parser

gramatica, lexer = gramm_Hulk_LR1()
<<<<<<< HEAD
# text = 'print(42);print(sin(4/2));print("Hello World");'
# text_create_type = """type Point{x = 0;y = 0;getX() => x;getY() => y;setX(x) => x := x;setY(y) => y := y;}"""
# tokens = lexer(text_create_type)
# print(f'Tokens: {tokens}')
# tokentypes = [token.token_type for token in tokens if token.token_type != 'space']
# print(f'Tokentypes: {tokentypes}')
# parser = LR1Parser(gramatica, False)
# output,operations = parser(tokentypes)
# # print(type(operations))
# ast = evaluate_reverse_parse(output, operations, tokens)
# #print(ast)
# checker = SemanticCheckingVisitor()
# errors = checker.semantic_checking(ast)
# print(errors)


ast = Pro
=======

with open('./prueba.txt', "r", encoding="utf-8") as archivo:
    content = archivo.read()
    text = content

text = '''let text = 4 in 2;'''
#text = '''let text = 4;'''
#text = '{print(text @ number);}'
print(text)
#text = 'type call(x){ x = 3; }'
tokens = lexer(text)
tokentypes = [token.token_type for token in tokens if token.token_type != 'space']
parser = LR1Parser(gramatica,True)
output,operations = parser(tokentypes)
#print(type(operations))
ast = evaluate_reverse_parse(output, operations, tokens)
print(ast)
#checker = SemanticCheckingVisitor()
#errors = checker.semantic_checking(ast)
# print(checker.scope.define_variable)
>>>>>>> ed7b2040b333877fc2186a61f0bbb292af57427f
