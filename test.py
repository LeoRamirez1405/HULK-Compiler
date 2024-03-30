from semantic_checking.AST import *
#from semantic_checking.semantic_checking import SemanticCheckingVisitor
#from semantic_checking.evaluation import evaluate_reverse_parse
from grammLR1 import gramm_Hulk_LR1
from LR1 import LR1Parser

gramatica, lexer = gramm_Hulk_LR1()

# Abrir el archivo en modo lectura
with open('prueba.txt', 'r') as prueba:
    contenido = prueba.read()

    # contenido = "if (x is Bird) \"It's bird!\""
    
    # Reemplazar saltos de línea por espacios en blano
    contenido = contenido.replace('\n', ' ')

    # Reemplazar tabulaciones por espacios en blanco
    contenido = contenido.replace('\t', '')
    contenido = contenido.replace('"', '\"')


text = '''3 + (let text = 4 in 2);'''
# text = "Hello World"
tokens = lexer(text)
tokentypes = [token.token_type for token in tokens if token.token_type != 'space']
parser = LR1Parser(gramatica,False)
output,operations = parser(tokentypes)
print(tokentypes)
parser = LR1Parser(gramatica,True)

derivation = parser(tokentypes)
print(derivation)



