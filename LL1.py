from cmp.utils import ContainerSet
# Computes First(alpha), given First(Vt) and First(Vn) 
# alpha in (Vt U Vn)*


def build_parsing_table(G, firsts, follows):
    # init parsing table
    M = {}
    
    # P: X -> alpha
    for production in G.Productions:
        X = production.Left
        alpha = production.Right
        
        ###################################################
        # working with symbols on First(alpha) ...
        ###################################################
        for first in firsts[alpha]:
            if (X, first) in M:
                raise Exception(f'La gramatica no es LL(1), ya q el no terminal {X} tiene asociada la produccion {M[X, first]} y se le quiere asignar la produccion {production}')
            M[X, first] = production
        ###################################################    
        
        ###################################################
        # working with epsilon...
        ###################################################
        if alpha.IsEpsilon:
            for follow in follows[X]:
                if (X, follow) in M:
                    raise Exception('La gramatica no es LL(1)')
                M[X, follow] = G.Epsilon
        ###################################################
    
    # parsing table is ready!!!
    return M        

def metodo_predictivo_no_recursivo(G, M=None, firsts=None, follows=None):
    
    # checking table...
    if M is None:
        if firsts is None:
            firsts = compute_firsts(G)
        if follows is None:
            follows = compute_follows(G, firsts)
        M = build_parsing_table(G, firsts, follows)
    
    
    # parser construction...
    def parser(w):
        
        ###################################################
        # w ends with $ (G.EOF)
        ###################################################
        # init:
        ### stack =  ????
        ### cursor = ????
        ### output = ????
        ###################################################
        cursor = 0
        stack = [G.startSymbol]
        output = []
        # parsing w...
        while stack and cursor < len(w):
        # while True:
            top = stack.pop()
            actual = w[cursor]
            
            ###################################################
            if top.IsTerminal:
                if top != actual:
                    raise Exception(f'Token inexperado: {actual}')
                cursor += 1
            else:
                try:
                    production = M[top, actual]
                    if production == G.Epsilon:
                        output.append(Production(top, G.Epsilon))
                        continue
                    for i in range(len(production.Right) -1, -1, -1):
                        stack.append(production.Right[i])
                    output.append(production)
                except:
                    raise Exception(f'No existe la produccion para el no terminal {top} y el simbolo {actual}')
            ###################################################

        # left parse is ready!!!
        return output
    
    # parser is ready!!!
    return parser
    
