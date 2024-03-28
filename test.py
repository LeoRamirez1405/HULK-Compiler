from grammLR1 import gramm_Hulk_LR1
from LR1 import LR1Parser
from lexer import Lexer


gramatica, lexer = gramm_Hulk_LR1()
gramatica, lexer = gramm_Hulk_LR1()



# print(gramatica.Terminals)

# Print, oPar, cPar, oBrace, cBrace, Semi, Equal, Plus, Minus, Mult, Div, Arrow, Mod = G.Terminals('print ( ) { } ; = + - * / => %')
# And, Or, Not, Less, Greater, Equal, LessEqual, GreaterEqual, NotEqual, Is, In, _True, _False = G.Terminals('and or not < > == <= >= != is in True False')
# Comma, Dot, If, Else, While, For, Let, Function, Colon = G.Terminals(', . if else while for let function :')
# identifier, number, string, Elif, Type, Inherits, New, In, def_Type   = G.Terminals('identifier number string elif type inherits new in def_Type') 
# sComil, dComill = G.Terminals('\' \"')
# sqrt, sin, cos, tan, exp, log, rand = G.Terminals('sqrt sin cos tan exp log rand')

# nonzero_digits = '|'.join(str(n) for n in range(1,10))
# zero_digits = '|'.join(str(n) for n in range(0,10))
# minletters = '|'.join(chr(n) for n in range(ord('a'),ord('z')+1)) 
# capletters = '|'.join(chr(n) for n in range(ord('A'),ord('Z')+1)) 
# all_characters = f"{minletters}| |{capletters}"


# lexer = Lexer([
#     ('number', f'({nonzero_digits})({zero_digits})*'),
#     ('string', f'\'({all_characters}|{zero_digits})*\'|\"({all_characters}|{zero_digits})*\"'),
#     ('Print', 'print'),
#     ('oPar', "\("),
#     ('cPar', "\)"),
#     ('oBrace', '{'),
#     ('cBrace', '}'),
#     ('Semi', ';'),
#     ('Equal', '='),
#     ('Plus', '+'),
#     ('Minus', '-'),
#     ('Mult', "\*"),
#     ('Div', '/'),
#     ('Arrow', '=>'),
#     ('Mod', '%'),
#     ('And', 'and'),
#     ('Or', 'or'),
#     ('Not', 'not'),
#     ('Less', '<'),
#     ('Greater', '>'),
#     ('CompEqual', '=='),
#     ('LessEqual', '<='),
#     ('GreaterEqual', '>='),
#     ('NotEqual', '!='),
#     ('Is', 'is'),
#     ('In', 'in'),
#     ('_True', 'True'),
#     ('_False', 'False'),
#     ('Comma', ','),
#     ('Dot', '.'),
#     ('If', 'if'),
#     ('Else', 'else'),
#     ('While', 'while'),
#     ('For', 'for'),
#     ('Let', 'let'),
#     ('space', '  *'),
#     ('Function', 'function'),
#     ('Colon', ':'),
#     ('Elif', 'elif'),
#     ('Type', 'type'),
#     ('Inherits', 'inherits'),
#     ('New', 'new'),
#     ('In', 'in'),
#     ('def_Type', 'def_Type'),
#     ('sComil', '\''),
#     ('dComill', '\"'),
#     ('sqrt', 'sqrt'),
#     ('sin', 'sin'),
#     ('cos', 'cos'),
#     ('tan', 'tan'),
#     ('exp', 'exp'),
#     ('log', 'log'),
#     ('rand', 'rand'),
#     ('identifier', f'({minletters})({minletters}|{zero_digits})*')
# ], 'eof')
# nonzero_digits = '|'.join(str(n) for n in range(1,10))
# zero_digits = '|'.join(str(n) for n in range(0,10))
# minletters = '|'.join(chr(n) for n in range(ord('a'),ord('z')+1)) 
# capletters = '|'.join(chr(n) for n in range(ord('A'),ord('Z')+1)) 
# all_characters = f"{minletters}| |{capletters}"


# lexer = Lexer([
#     ('number', f'({nonzero_digits})({zero_digits})*'),
#     ('string', f'\'({all_characters}|{zero_digits})*\'|\"({all_characters}|{zero_digits})*\"'),
#     ('Print', 'print'),
#     ('oPar', "\("),
#     ('cPar', "\)"),
#     ('oBrace', '{'),
#     ('cBrace', '}'),
#     ('Semi', ';'),
#     ('Equal', '='),
#     ('Plus', '+'),
#     ('Minus', '-'),
#     ('Mult', "\*"),
#     ('Div', '/'),
#     ('Arrow', '=>'),
#     ('Mod', '%'),
#     ('And', 'and'),
#     ('Or', 'or'),
#     ('Not', 'not'),
#     ('Less', '<'),
#     ('Greater', '>'),
#     ('CompEqual', '=='),
#     ('LessEqual', '<='),
#     ('GreaterEqual', '>='),
#     ('NotEqual', '!='),
#     ('Is', 'is'),
#     ('In', 'in'),
#     ('_True', 'True'),
#     ('_False', 'False'),
#     ('Comma', ','),
#     ('Dot', '.'),
#     ('If', 'if'),
#     ('Else', 'else'),
#     ('While', 'while'),
#     ('For', 'for'),
#     ('Let', 'let'),
#     ('space', '  *'),
#     ('Function', 'function'),
#     ('Colon', ':'),
#     ('Elif', 'elif'),
#     ('Type', 'type'),
#     ('Inherits', 'inherits'),
#     ('New', 'new'),
#     ('In', 'in'),
#     ('def_Type', 'def_Type'),
#     ('sComil', '\''),
#     ('dComill', '\"'),
#     ('sqrt', 'sqrt'),
#     ('sin', 'sin'),
#     ('cos', 'cos'),
#     ('tan', 'tan'),
#     ('exp', 'exp'),
#     ('log', 'log'),
#     ('rand', 'rand'),
#     ('identifier', f'({minletters})({minletters}|{zero_digits})*')
# ], 'eof')

# text = 'let msg = \"Hello World\" in print(msg);'
# text = 'let number = 42, text = \"The meaning of life is\" in print(text @ number);'
# text = 'let number = 42 in let text = \"The meaning of life is\" in print(text @ number);'
# text = 'let number = 42 in {let text = \"The meaning of life is\" in {print(text @ number)}};
# text = 'let a = 5, b = 10, c = 20 in {print(a+b);print(b*c);print(c/a);}'
# text = 'let a = (let b = 6 in b * 7) in print(a);'

# text = '42;'
# text = 'print(42);'
# text = 'print((((1 + 2) ^ 3) * 4) / 5);'
# text = 'print(\"Hello World\");'
# text = 'print(\"The meaning of life is \" @ 42);'
# text = 'print(sin(2 * PI) ^ 2 + cos(3 * PI / log(4, 64)));'
text = '{print(42);print(sin(PI/2));print("Hello World");}'
tokens = lexer(text)
print(tokens)

# Extraer las propiedades "tokentype" de cada token
tokentypes = [token.token_type for token in tokens if token.token_type != 'space']

print(tokentypes)
parser = LR1Parser(gramatica,False)

derivation = parser(tokentypes)
print(derivation)



