from semantic_checking.AST import *
#from semantic_checking.semantic_checking import SemanticCheckingVisitor
#from semantic_checking.evaluation import evaluate_reverse_parse
from grammLR1 import gramm_Hulk_LR1
from LR1 import LR1Parser

gramatica, lexer = gramm_Hulk_LR1()

# with open('./prueba.txt', "r", encoding="utf-8") as archivo:
#     content = archivo.read()
#     text = content

text = '''let b = a in { print(a);};'''
#text = '{print(text @ number);}'
print(text)
#text = 'type call(x){ x = 3; }'
tokens = lexer(text)
tokentypes = [token.token_type for token in tokens if token.token_type != 'space']
parser = LR1Parser(gramatica,False)
output,operations = parser(tokentypes)
print(tokentypes)
#print(output)
#ast = evaluate_reverse_parse(output, operations, tokens)
#print(ast)
#checker = SemanticCheckingVisitor()
#errors = checker.semantic_checking(ast)
# print(checker.scope.define_variable)
