from gramm import grammHulk
from LL1 import compute_firsts,compute_follows,build_parsing_table,metodo_predictivo_no_recursivo


gramatica = grammHulk()
firsts = compute_firsts(gramatica)
follows = compute_follows(gramatica, firsts)
M = build_parsing_table(gramatica, firsts, follows)
parser = metodo_predictivo_no_recursivo(gramatica, M)
print(M)