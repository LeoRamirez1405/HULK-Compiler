from cmp.utils import ContainerSet
# Computes First(alpha), given First(Vt) and First(Vn) 
# alpha in (Vt U Vn)*
def compute_local_first(firsts, alpha):
    first_alpha = ContainerSet()
    
    try:
        alpha_is_epsilon = alpha.IsEpsilon
    except:
        alpha_is_epsilon = False
    
    ###################################################
    # alpha == epsilon ? First(alpha) = { epsilon }
    ###################################################
    if alpha_is_epsilon:
        first_alpha.set_epsilon()
    ###################################################
    # alpha = X1 ... XN
    # First(Xi) subconjunto First(alpha)
    # epsilon pertenece a First(X1)...First(Xi) ? First(Xi+1) subconjunto de First(X) y First(alpha)
    # epsilon pertenece a First(X1)...First(XN) ? epsilon pertence a First(X) y al First(alpha)
    ###################################################
    else:
        for x in alpha:
            first_alpha.update(firsts[x])
            if not firsts[x].contains_epsilon:
                break
        else:
            first_alpha.set_epsilon()
    ###################################################
    
    # First(alpha)
    return first_alpha

# Computes First(Vt) U First(Vn) U First(alpha)
# P: X -> alpha
def compute_firsts(G):
    firsts = {}
    change = True
    
    # init First(Vt)
    for terminal in G.terminals:
        firsts[terminal] = ContainerSet(terminal)
        
    # init First(Vn)
    for nonterminal in G.nonTerminals:
        firsts[nonterminal] = ContainerSet()
    
    while change:
        change = False
        
        # P: X -> alpha
        for production in G.Productions:
            X = production.Left
            alpha = production.Right
            
            # get current First(X)
            first_X = firsts[X]
                
            # init First(alpha)
            try:
                first_alpha = firsts[alpha]
            except KeyError:
                first_alpha = firsts[alpha] = ContainerSet()
            
            # CurrentFirst(alpha)???
            local_first = compute_local_first(firsts, alpha)
            
            # update First(X) and First(alpha) from CurrentFirst(alpha)
            change |= first_alpha.hard_update(local_first)
            change |= first_X.hard_update(local_first)
                    
    # First(Vt) + First(Vt) + First(RightSides)
    return firsts

from itertools import islice

def compute_follows(G, firsts):
    follows = { }
    change = True
    
    local_firsts = {}
    
    # init Follow(Vn)
    for nonterminal in G.nonTerminals:
        follows[nonterminal] = ContainerSet()
    follows[G.startSymbol] = ContainerSet(G.EOF)
    
    while change:
        change = False
        
        # P: X -> alpha
        for production in G.Productions:
            X = production.Left
            alpha = production.Right
            
            follow_X = follows[X]
            
            ###################################################
            # X -> zeta Y beta
            # First(beta) - { epsilon } subset of Follow(Y)
            # beta ->* epsilon or X -> zeta Y ? Follow(X) subset of Follow(Y)
            ###################################################
            for (index, symbol) in enumerate(alpha):
                if symbol.IsNonTerminal:
                    local_firsts = compute_local_first(firsts, alpha[index + 1:])
                    change |= follows[symbol].update(local_firsts)
                    if local_firsts.contains_epsilon:
                        change |= follows[symbol].update(follow_X)
            ###################################################

    # Follow(Vn)
    return follows

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
    
