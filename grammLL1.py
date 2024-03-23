from cmp.pycompiler import Grammar

def grammHulk():
    
    G = Grammar()

    Program = G.NonTerminal('Program', True)

    # Terminales

    num, str_, id_, sqrt, sin, cos, exp, log, rand, plus, minus, star, div, pow, mod = G.Terminals('num str id sqrt sin cos exp log rand + - * / ^ %')
    eq, neq, lt, gt, leq, geq, and_, or_, not_, assign, semicolon, comma, opar, cpar, obrace, cbrace, at, dot, true, false  = G.Terminals('== != < > <= >= && || ! = ; , ( ) { } @ . True False')
    newline = G.Terminal('\\n')
    tab = G.Terminal('\\t')
    eof = G.Terminal('EOF')

    if_,else_,while_,for_,in_,range_,next_,current_,print_,let_,function_,class_ = G.Terminals('if else while for in range next current print let function class')

    # Definición de los operadores de asignación aumentada
    plus_assign, minus_assign, star_assign, div_assign = G.Terminals('+= -= *= /=')

    # No terminales
    E, T, F, X, Y, S = G.NonTerminals('E T F X Y S')
    F0, F1, F2, F3 = G.NonTerminals('F0 F1 F2 F3')
    Func, Param, Body, Exp, Stmt, Decl, If, Else, While, For, Range, Iterable,ParE = G.NonTerminals('Func Param Body Exp Stmt Decl If Else While For Range Iterable ParE')
    auxExp, Exp1,Exp2 = G.NonTerminals('auxExp Exp1 Exp2')

    # Expresiones

    E %= T + X
    X %= plus + T + X | minus + T + X | G.Epsilon
    T %= F + Y
    Y %= star + F + Y | div + F + Y | mod + F + Y | pow + F + Y  | G.Epsilon
    #F %= num | id_ | sqrt + opar + E + cpar | sin + opar + E + cpar | cos + opar + E + cpar | exp + opar + E + cpar | log + opar + E + comma + E + cpar | rand + opar + cpar | opar + E + cpar 
    F %= num | sqrt + ParE | sin + ParE | cos + ParE | exp + ParE | log + opar + E + comma + E + cpar | rand + opar + cpar | ParE 
    ParE %= opar + E + cpar
    #F %= F + at + F | F + dot + id_ + opar + cpar | F + dot + id_ + opar + E + comma + E + cpar | F + dot + id_ + opar + E + cpar
    #F %= (F) + at + F 
    #         + (dot + id_ + opar) + cpar  
    #                              + (E) + cpar
    #                                    + comma + E + cpar 
    #F %= F + F0
    #F0 %= at + F | F1 
    #F1 %= dot + id_ + opar + F2
    #F2 %= cpar | E + F3 
    #F3 %= cpar | comma + E + cpar
    
    #P: Podría representar una lista de parámetros en la definición de funciones.
    #B: Podría representar un bloque de código, similar a S pero con un uso más específico.
    #V: Podría representar una variable o una expresión de asignación.
    #A: Podría ser un arreglo o una colección de elementos.
    #L: Podría ser una lista o un conjunto de elementos.
    #C: Podría ser una clase o una estructura de datos.
    #R: Podría representar un rango o un intervalo de valores.
    #I: Podría ser un índice o un contador en un bucle.
    #W: Podría ser un objeto o una instancia de una clase.
    
    P, V, A, L, C, R, I, W = G.NonTerminals('P V A L C R I W')
    P1,D1,I1,Param1,ExpId1,Bbody,BExp,auxX,Exp3,Exp4 = G.NonTerminals('P1 D1 I1 Param1 ExpId1 Bbody BExp, auxX Exp3 Exp4')
    
    #P %= id_ + comma + P | id_ | G.Epsilon  # Lista de parámetros
    P %= id_ + P1 | G.Epsilon  # Lista de parámetros
    P1 %= comma + P | G.Epsilon  
          
    #Decl %= let_ + id_ + assign + E + semicolon | let_ + id_ + assign + E + comma + Decl # Declaraciones
    Decl %= let_ + V + D1   # Declaraciones
    D1 %= semicolon | comma + Decl
    
    V %= id_ + assign + E  # Asignación de variable
    A %= id_ + ParE  # Acceso a arreglo o colección
    L %= id_ + opar + E + comma + E + cpar  # Listas o conjuntos
    C %= class_ + id_ + obrace + S + cbrace  # Definición de clase
    R %= range_ + opar + E + comma + E + cpar  # Rango de valores
    I %= id_ + plus_assign + E  # Incremento de índice
    W %= id_ + dot + id_  # Acceso a un miembro de un objeto


    # Ejemplo de modificación de la producción para Stmt, utilizando eof
    Program %= S | G.Epsilon | eof

    # Estructuras de control
    If %= if_ + ParE + obrace + newline + tab + S + newline + cbrace + Else
    Else %= else_ + obrace + newline + tab + S + newline + cbrace | G.Epsilon
    While %= while_ + ParE + obrace + newline + tab + S + newline + cbrace
    For %= for_ + opar + id_ + in_ + Range + cpar + obrace + newline + tab + S + newline + cbrace
    Range %= range_ + opar + E + comma + E + cpar | Iterable
    
    #Iterable %= id_ + dot + next_ + opar + cpar | id_ + dot + current_ + opar + cpar
    Iterable %= id_ + dot + I1
    I1 %= next_ + opar + cpar | current_ + opar + cpar
    
    # Bloques de código
    S %= Stmt + S | G.Epsilon
    Stmt %= Decl | Exp + semicolon | If | While | For | print_ + ParE + semicolon | function_ + id_ + opar + Param + cpar + Bbody
    Body %= Stmt + Body | G.Epsilon
    Bbody %= obrace + Body + cbrace
    BExp %= obrace + Exp + cbrace
    # Funciones
    Func %= function_ + id_ + opar + Param + cpar + Bbody
    
    #Param %= id_ + comma + Param | id_ | G.Epsilon
    Param %= id_ + Param1| G.Epsilon
    Param1 %= comma + Param | G.Epsilon 

    # Expresiones más complejas
    # Exp %= E | auxExp | id_ + assign + E | id_ + plus_assign + E | id_ + minus_assign + E | id_ + star_assign + E | id_ + div_assign + E | if_ + opar + E + cpar + obrace + Exp + else_ + Exp + cbrace | while_ + opar + E + cpar + obrace + Exp + cbrace | for_ + opar + id_ + in_ + Range + cpar + obrace + Exp + cbrace 
    Exp %= auxExp | id_ + ExpId1 
    
    auxExp %= Exp2 + auxX 
    auxX %= or_ + Exp2 | and_ + Exp2 
    Exp2 %= not_ + Exp2 | Exp3 | auxX
    Exp3 %= E + Exp4
    Exp4 %= eq + E | neq + E | lt + E | gt + E | leq + E | geq + E | true | false 
    ExpId1 %=  assign + E | plus_assign + E | minus_assign + E | star_assign + E | div_assign + E 
    
    print(G)
    return G
