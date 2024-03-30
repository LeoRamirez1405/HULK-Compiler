import sys
import os
current_dir = os.getcwd()
sys.path.insert(0, current_dir)

from AST import *
from semantic_checking.semantic_checking import SemanticCheckingVisitor
from evaluation import evaluate_reverse_parse
#from grammLR1 import gramm_Hulk_LR1
from grammLR1 import gramm_Hulk_LR1
from LR1 import LR1Parser

#gramatica, lexer = gramm_Hulk_LR1()
gramatica, lexer = gramm_Hulk_LR1()
text = 'print(42);print(sin(4/2));print("Hello World");'
#text = 'print(42);'
tokens = lexer(text)
tokentypes = [token.token_type for token in tokens if token.token_type != 'space']
parser = LR1Parser(gramatica, False)
output,operations = parser(tokentypes)
print(type(operations))
ast = evaluate_reverse_parse(output, operations, tokens)
print(ast)
checker = SemanticCheckingVisitor()
errors = checker.semantic_checking(ast)
# print(checker.scope.define_variable)
