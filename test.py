from semantic_checking.AST import *
from semantic_checking.semantic_checking import SemanticCheckingVisitor
from format_visitor import FormatVisitor
#from semantic_checking.semantic_checking import SemanticCheckingVisitor
#from semantic_checking.evaluation import evaluate_reverse_parse
from grammLR1 import gramm_Hulk_LR1
from LR1 import LR1Parser,evaluate_reverse_parse

gramatica, lexer = gramm_Hulk_LR1()

with open('./prueba.txt', "r", encoding="utf-8") as archivo:
    content = archivo.read()

    contenido = content.replace('\n', ' ')

    # Reemplazar tabulaciones por espacios en blanco
    contenido = contenido.replace('\t', '')
    contenido = contenido.replace('"', '\"')
    text = content

print(text)
tokens = lexer(text)
tokentypes = [token.token_type for token in tokens if token.token_type != 'space']
parser = LR1Parser(gramatica,False)
output,operations = parser(tokentypes)
tokensAST = [token for token in tokens if token.token_type != 'space']

ast = evaluate_reverse_parse(output,operations,tokensAST)

checker = SemanticCheckingVisitor()
print(checker.semantic_checking(ast))

formatter = FormatVisitor()
tree = formatter.visit(ast)
print(tree)



