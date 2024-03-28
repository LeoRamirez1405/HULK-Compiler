from grammLR1 import gramm_Hulk_LR1
from LR1 import LR1Parser

gramatica = gramm_Hulk_LR1()
parser = LR1Parser(gramatica,True)
print(parser)


