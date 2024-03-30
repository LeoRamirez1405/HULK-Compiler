from grammLR1Leo import gramm_Hulk_LR1
from LR1 import LR1Parser
from lexer import Lexer



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


text = "Hello World"
tokens = lexer(text)

# # Extraer las propiedades "tokentype" de cada token
tokentypes = [token.token_type for token in tokens if token.token_type != 'space']

print(tokentypes)
# parser = LR1Parser(gramatica,False)

# derivation = parser(tokentypes)
# print(derivation)



