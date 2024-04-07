from semantic_checking.AST import *
from semantic_checking.semantic_checking import SemanticCheckingVisitor
from semantic_checking.tree_walk_interpreter import TreeInterpreter
# from format_visitor import TreeWalkInterpreter
#from semantic_checking.semantic_checking import SemanticCheckingVisitor
#from semantic_checking.evaluation import evaluate_reverse_parse
from grammLR1 import gramm_Hulk_LR1
from LR1 import LR1Parser,evaluate_reverse_parse
from joblib import dump, load


gramatica, lexer = gramm_Hulk_LR1()


# Leer el contenido del archivo y reemplazar los saltos de línea
with open('prueba.hulk', 'r') as archivo:
    contenido = archivo.read()

    contenido_modificado = contenido.replace('\n', '[LineJump]')

    # Reemplazar tabulaciones por espacios en blanco
    contenido_modificado = contenido_modificado.replace('"', '\"')
    text = contenido_modificado

#print(text)
tokens = lexer(text)
tokentypes = [token.token_type for token in tokens]
#print(tokentypes)

# parser = LR1Parser(gramatica, rebuild=False)

# output,operations = parser(tokens)
tokensAST = [token for token in tokens if token.token_type != 'space']
print(tokensAST)
# ast = evaluate_reverse_parse(output,operations,tokensAST)
# # ast = ProgramNode([PlusExpressionNode(NumberNode(5), StringNode('casa'))])
# checker = SemanticCheckingVisitor()
# print(checker.semantic_checking(ast))

# interpreter = TreeInterpreter(checker.context)
# interpreter.visit(ast)

# formatter = TreeWalkInterpreter()
# tree = formatter.visit(ast)
# print(tree)

# # formatter = FormatVisitor()
# # tree = formatter.visit(ast)
# # print(tree)



