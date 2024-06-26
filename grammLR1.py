from cmp.pycompiler import Grammar
from semantic_checking.AST import *
from lexer import Lexer
import string as stringMod

def gramm_Hulk_LR1():
    G = Grammar()
    Program = G.NonTerminal('Program', True)
    statement_list, statement, expression, expression, term, factor, function_call, arguments, parameters = G.NonTerminals('statement_list statement expression expression term factor function_call arguments parameters')
    type_definition, attribute_definition, method_definition, inheritance, instance_creation, member_access, type_annotation = G.NonTerminals('type_definition attribute_definition method_definition inheritance instance_creation member_access type_annotation')
    print_statement, assignment, function_definition, control_structure, contElif, contElse= G.NonTerminals('print_statement assignment function_definition control_structure contElif contElse')
    if_structure, while_structure, for_structure, create_statement, non_create_statement, expr_statementWithoutSemi = G.NonTerminals('if_structure while_structure for_structure create_statement non_create_statement expr_statementWithoutSemi')
    let_in, multi_assignment, kern_assignment, destructive_assignment, let_in_as_expr, expr_statement= G.NonTerminals('let_in multi_assignment kern_assignment destructive_assignment let_in_as_expr expr_statement')
    cont_member, kern_instance_creation, concatStrings, concatStringsWithSpace, math_call, factorPow = G.NonTerminals('cont_member kern_instance_creation concatStrings concatStringsWithSpace math_call factorPow')
    Print, oPar, cPar, oBrace, cBrace, Semi, Equal, Plus, Minus, Mult, Div, Arrow, Mod, Destroy, Pow = G.Terminals('print ( ) { } ; = + - * / => % := ^')
    And, Or, Not, Less, Greater, CompEqual, LessEqual, GreaterEqual, NotEqual, Is, In, _True, _False = G.Terminals('and or not < > == <= >= != is in True False')
    Comma, Dot, If, Else, While, For, Let, Function, Colon, PowStar, _self = G.Terminals(', . if else while for let function : ** self')
    identifier, number, string, Elif, Type, Inherits, New, In, arroba, arroba2,PI   = G.Terminals('identifier number string elif type inherits new in @ @@ PI') 
    sComil, dComill, = G.Terminals('\' \"')
    sqrt, sin, cos, tan, exp, log, rand = G.Terminals('sqrt sin cos tan exp log rand')
    collection, destroy_collection, selfExpr = G.NonTerminals('collection destroy_collection selfExpr')
    self_access = G.NonTerminal('self_access')
    list_non_create_statement = G.NonTerminal('list_non_create_statement')
    
    Program %= statement_list, lambda h, s: ProgramNode(s[1])
    statement_list %= statement + statement_list, lambda h, s: [s[1]] + s[2] 
    #statement_list %= oBrace + list_non_create_statement + cBrace + statement_list , lambda h, s: s[2] + s[4]
    statement_list %= G.Epsilon, lambda h, s: []
    
    statement %= non_create_statement, lambda h, s: s[1] 
    statement %= create_statement, lambda h, s: s[1]
    # statement %= oBrace + list_non_create_statement + cBrace, lambda h, s: s[2]
    
    list_non_create_statement %= non_create_statement + list_non_create_statement,lambda h,s: [s[1]]+s[2]
    list_non_create_statement %= G.Epsilon,lambda h,s: []
    
    non_create_statement %= control_structure, lambda h, s: s[1]
    non_create_statement %= expr_statement + Semi, lambda h, s: s[1]
    non_create_statement %= assignment + Semi, lambda h, s: s[1] 
    
    non_create_statement %= destroy_collection + Semi, lambda h, s: s[1]
    non_create_statement %= oBrace + list_non_create_statement + cBrace, lambda h, s: BlockNode(s[2])
    
    create_statement %= type_definition, lambda h, s: s[1]
    create_statement %= function_definition, lambda h, s: s[1]
    
    #TODO aqui hay que ver como se maneja la cosa de las listas
    #factor %= assignment + In + expr_statement, lambda h, s: LetInExpressionNode(s[1], s[3])
    expr_statement %= assignment + In + expr_statement, lambda h, s: LetInExpressionNode(s[1], s[3], s[2]) #Ya
    expr_statement %= expression, lambda h, s: s[1]
    
    #print_statement %= Print + oPar + non_create_statement + cPar, lambda h, s: PrintStatmentNode(s[3], s[1]) #Ya
    print_statement %= Print + oPar + expr_statement + cPar, lambda h, s: PrintStatmentNode(s[3], s[1]) #Ya
    
    control_structure %= if_structure , lambda h, s: s[1]
    control_structure %= while_structure , lambda h, s: s[1]
    control_structure %= for_structure , lambda h, s: s[1]
    
    if_structure %= If + oPar + expression + cPar + oBrace + list_non_create_statement + cBrace + contElif + contElse , lambda h, s: IfStructureNode(s[3], s[6], s[8], s[9], s[1]) #Ya

    #TODO Ponerle que sea un coleccion
    contElif %= Elif + oPar + expression + cPar + oBrace + list_non_create_statement + cBrace + contElif , lambda h, s: [ElifStructureNode(s[1], s[3],s[6])] + s[8] #Ya
    contElif %= G.Epsilon , lambda h, s: []

    contElse %= Else + oBrace + statement_list + cBrace , lambda h, s: ElseStructureNode(s[3], s[1]) #Ya
    contElse %= G.Epsilon , lambda h, s:  ElseStructureNode([]) #Ya

    while_structure %= While + oPar + expression + cPar + oBrace + list_non_create_statement + cBrace , lambda h, s:  WhileStructureNode(s[3], s[6], s[1]) #Ya
    for_assignment = G.NonTerminal('for_assignment')
    for_assignment %= G.Epsilon, lambda h, s: CollectionNode([])
    for_assignment %= assignment, lambda h, s: s[1]

    for_assignment %= destroy_collection, lambda h, s: s[1]
    
    for_structure %= For + oPar + for_assignment + Semi + expression + Semi + destroy_collection + cPar + oBrace + list_non_create_statement + cBrace , lambda h, s:  ForStructureNode(s[3], s[5], s[7], s[10], s[1]) #Ya
    
    #TODO Cambie la atributacion y le puse que creara un nodo collection para saber luego en los checkeos que hay que iterar en ese tipo de nodos
    # assignment %= Let + multi_assignment, lambda h, s: s[2]
    # assignment %= Let + multi_assignment, lambda h, s: CollectionNode(s[2], s[1]) #Ya
    #* En los assigments y en los destroy se crean collection y cada uno de esos debe tener su propio token cada a = expression se supone q a tiene un token y expression tiene otro
    assignment %= Let + multi_assignment, lambda h, s: CollectionNode(s[2])
    multi_assignment %= kern_assignment + Comma + multi_assignment, lambda h, s: [s[1]] + s[3]
    multi_assignment %= kern_assignment, lambda h, s: [s[1]]
    kern_assignment %= identifier + Equal + expr_statement, lambda h, s: KernAssigmentNode(IdentifierNode(s[1]),s[3], s[1]) #Ya
    kern_assignment %= self_access + Equal + expr_statement, lambda h, s: KernAssigmentNode(IdentifierNode(s[1]),s[3], s[1])  #Ya
    
   
    destroy_collection %= destructive_assignment, lambda h, s : CollectionNode(s[1])
    destructive_assignment %= self_access + Destroy + expression + Comma + destructive_assignment, lambda h, s : [DestroyNode(s[1],s[3], s[1])] + s[4] #Ya
    destructive_assignment %= identifier + Destroy + expression + Comma + destructive_assignment, lambda h, s : [DestroyNode(IdentifierNode(s[1]) , s[3], s[1])] + s[4] #Ya
    destructive_assignment %= self_access + Destroy + expression, lambda h, s: [DestroyNode(s[1] , s[3], s[1])] #Ya
    destructive_assignment %= identifier + Destroy + expression, lambda h, s: [DestroyNode(IdentifierNode(s[1]) , s[3], s[1])] #Ya

    function_definition %= Function + identifier + oPar + parameters + cPar + type_annotation + oBrace + list_non_create_statement + cBrace, lambda h, s: FunctionDefinitionNode(IdentifierNode(s[2]),s[6],s[4],s[8]) #Ya
    #TODO aqui puse el statment entre corchetes en la creacion del nodo porque de lo contrario no lo puedo iterar
    function_definition %= Function + identifier + oPar + parameters + cPar + type_annotation + Arrow + statement,lambda h, s: FunctionDefinitionNode(IdentifierNode(s[2]),s[6],s[4], s[8] )
    
    #TODO Cambie expression por identifier porque el parametro de una funcion tiene que ser obligatoria mente un variable 
    parameters %= identifier + type_annotation + Comma + parameters, lambda h, s: [{IdentifierNode(s[1]):s[2]}] + s[4] #Ya
    #* Puse el diccionario que se creaba solo entre corchetes para formar la lisat
    parameters %= identifier + type_annotation, lambda h, s: [{IdentifierNode(s[1]):s[2]}] #Ya
    parameters %= G.Epsilon, lambda h, s:[]
    
    type_annotation %= Colon + identifier, lambda h, s: TypeNode(s[2]) #Ya
    type_annotation %= G.Epsilon, lambda h, s: TypeNode('object') #Ya
    
    ExprAnd, ExprNeg, ExprIsType, ExprComp, ExprNum, ExprOr= G.NonTerminals('ExprAnd ExprNeg ExprIsType ExprComp ExprNum ExprOr')
    
    expression %= ExprOr, lambda h, s: s[1] 
    expression %= expression + arroba2 + ExprOr, lambda h, s:  StringConcatWithSpaceNode(s[1],s[3], s[2]) #Ya
    expression %= expression + arroba + ExprOr, lambda h, s:  StringConcatNode(s[1],s[3], s[2]) #Ya
    

    ExprOr %= ExprAnd, lambda h, s: s[1]
    ExprOr %= ExprOr + Or + ExprAnd, lambda h, s:  BoolOrNode(s[1],s[3], s[2]) #Ya
    
    ExprAnd %= ExprNeg, lambda h, s: s[1]
    ExprAnd %= ExprAnd + And + ExprNeg, lambda h, s:  BoolAndNode(s[1],s[3], s[2]) #Ya
    ExprNeg %= ExprIsType, lambda h, s: s[1]
    ExprNeg %= Not + ExprIsType, lambda h, s:  BoolNotNode(s[2], s[1])  #Ya
    
    ExprIsType %= ExprComp, lambda h, s: s[1]
    ExprIsType %= ExprComp + Is + identifier, lambda h, s:  BoolIsTypeNode(s[1],TypeNode(s[3]), s[2]) #Y
    
    ExprComp %= ExprNum, lambda h, s: s[1]
    ExprComp %= ExprNum + Less + ExprNum, lambda h, s:  BoolCompLessNode(s[1],s[3], s[2]) #Y
    ExprComp %= ExprNum + Greater + ExprNum, lambda h, s:  BoolCompGreaterNode(s[1],s[3], s[2]) #Y
    ExprComp %= ExprNum + CompEqual + ExprNum, lambda h, s:  BoolCompEqualNode(s[1],s[3], s[2]) #Y
    ExprComp %= ExprNum + LessEqual + ExprNum, lambda h, s:  BoolCompLessEqualNode(s[1],s[3], s[2]) #Y
    ExprComp %= ExprNum + GreaterEqual + ExprNum, lambda h, s:  BoolCompGreaterEqualNode(s[1],s[3], s[2]) #Y
    ExprComp %= ExprNum + NotEqual + ExprNum, lambda h, s:  BoolCompNotEqualNode(s[1],s[3], s[2]) #Y
    
    ExprNum %= term , lambda h, s: s[1]
    ExprNum %= ExprNum + Plus + term , lambda h, s:  PlusExpressionNode(s[1],s[3], s[2]) #Y
    ExprNum %= ExprNum + Minus + term , lambda h, s:  SubsExpressionNode(s[1],s[3], s[2]) #Y
    
    term %= factorPow , lambda h, s: s[1]
    term %= term + Mult+ factorPow, lambda h, s:  MultExpressionNode(s[1],s[3], s[2]) #Y
    term %= term + Div + factorPow, lambda h, s:  DivExpressionNode(s[1],s[3], s[2]) #Y
    term %= term + Mod + factorPow, lambda h, s:  ModExpressionNode(s[1],s[3], s[2]) #Y
    
    
    factorPow %= factor, lambda h, s:s[1]
    factorPow %= factor + Pow + factorPow , lambda h, s:  PowExpressionNode(s[1],s[3], s[2]) #Y
    factorPow %= factor + PowStar + factorPow , lambda h, s:  PowExpressionNode(s[1],s[3], s[2]) #Y
        
    factor %= oPar + expr_statement + cPar , lambda h, s:  s[2]
    factor %= number, lambda h, s:  NumberNode(s[1]) #Ya
    factor %= string, lambda h, s:  StringNode(s[1]) #Ya
    factor %= _False, lambda h, s:  BooleanNode(s[1]) #Ya
    factor %= _True, lambda h, s:  BooleanNode(s[1]) #Ya
    factor %= identifier + oPar + arguments + cPar, lambda h, s: FunctionCallNode(s[1],s[3]) #Ya
    factor %= identifier, lambda h, s:  IdentifierNode(s[1]) #Ya
    factor %= control_structure, lambda h, s: s[1]
    factor %= oPar + assignment + cPar, lambda h, s: s[2] 
    factor %= oPar+ destroy_collection + cPar, lambda h, s: s[2]
    factor %=  oBrace + list_non_create_statement + cBrace, lambda h, s: BlockNode(s[2])
    factor %= print_statement, lambda h, s: s[1]
    
    #TODO Dear future Leo: assignment In expr_statement NO ES UN FACTOR (acuerdate del ejemplo q lo parte, el del punto y coma necesario al final)
    #factor %= assignment + In + expr_statement, lambda h, s: LetInExpressionNode(s[1], s[3])
    factor %= math_call, lambda h, s:  s[1]
    factor %= member_access, lambda h, s:  s[1]  
    factor %= self_access, lambda h, s:  s[1]  
    factor %= kern_instance_creation, lambda h,s: s[1]  
    
    member_access %= factor + Dot + identifier + oPar + arguments + cPar , lambda h, s: MemberAccessNode(s[1], IdentifierNode(s[3]), s[5]) #Ya
    self_access %= _self + Dot + identifier , lambda h, s: SelfNode(IdentifierNode(s[3]), s[1]) #Ya #Todo member access Los parametros son privados de la clase #! NAOMI ARREGLA ESTO EN EL CHECKEO SEMANTICO ❤️
    kern_instance_creation %= New + identifier + oPar + arguments + cPar, lambda h, s: KernInstanceCreationNode(IdentifierNode(s[2]),s[4]) #Ya
    #kern_instance_creation %= New + identifier, lambda h, s: KernInstanceCreationNode(IdentifierNode(s[2]),[])
    
    math_call %= sqrt + oPar + ExprNum + cPar, lambda h, s: SqrtMathNode(s[3], s[1]) #Ya
    math_call %= cos + oPar + ExprNum + cPar, lambda h, s: CosMathNode(s[3], s[1])  #Ya
    math_call %= sin + oPar + ExprNum + cPar, lambda h, s: SinMathNode(s[3], s[1])  #Ya
    math_call %= tan + oPar + ExprNum + cPar, lambda h, s: TanMathNode(s[3], s[1])  #Ya
    math_call %= exp + oPar + ExprNum + cPar, lambda h, s: ExpMathNode(s[3], s[1])  #Ya
    #TODO Cambie la forma en la que se creaba el nodo 
    math_call %= log + oPar + ExprNum + Comma + ExprNum + cPar, lambda h, s: LogFunctionCallNode(s[3],s[5],s[1]) #Ya
    math_call %= rand + oPar + cPar,  lambda h, s: RandomFunctionCallNode(s[1]) #Ya
    math_call %= PI, lambda h, s: PINode(s[1])
    
    arguments %= expr_statement + Comma + arguments, lambda h, s: [s[1]] + s[3]
    arguments %= expr_statement , lambda h, s: [s[1]]
    arguments %= G.Epsilon, lambda h, s: []
    
    # Estructuras adicionales para tipos
    type_definition %= Type + identifier + oPar + parameters + cPar+ inheritance + oBrace + attribute_definition + method_definition + cBrace, lambda h, s: TypeDefinitionNode(IdentifierNode(s[2]),s[4],s[6], s[8],s[9])
    type_definition %= Type + identifier + inheritance + oBrace + attribute_definition + method_definition + cBrace, lambda h, s: TypeDefinitionNode(IdentifierNode(s[2]),[],s[3], s[5],s[6])

    #! El siguiente comentario paso a ser lo que era antes
    #TODO Quite el self porque cuando se inicializan los atributos no se pone self
    attribute_definition %= _self + Dot + kern_assignment + Semi + attribute_definition, lambda h, s: [s[3]] + s[5]
    #attribute_definition %= kern_assignment + Semi + attribute_definition, lambda h, s: [s[1]] + s[3]
    attribute_definition %= G.Epsilon, lambda h, s: []

    method_definition %= identifier + oPar + parameters + cPar + type_annotation + oBrace + list_non_create_statement + cBrace + method_definition, lambda h, s: [FunctionDefinitionNode(IdentifierNode(s[1]), s[5], s[3],s[7])] + s[9]
    #TODO aqui puse el statment entre corchetes en la creacion del nodo porque de lo contrario no lo puedo iterar
    method_definition %= identifier + oPar + parameters + cPar + type_annotation + Arrow + statement + method_definition, lambda h, s: [FunctionDefinitionNode(IdentifierNode(s[1]), s[5], s[3], s[7])] + s[8]
    method_definition %= G.Epsilon , lambda h, s: []

    inheritance %= Inherits + identifier, lambda h, s: InheritanceNode(IdentifierNode(s[2]),[])
    inheritance %= Inherits + identifier + oPar + arguments + cPar, lambda h, s: InheritanceNode(IdentifierNode(s[2]),s[4])
    inheritance %= G.Epsilon, lambda h, s: InheritanceNode(IdentifierNode('object'),[])
    
    nonzero_digits = '|'.join(str(n) for n in range(1,10))
    zero_digits = '|'.join(str(n) for n in range(0,10))
    minletters = '|'.join(chr(n) for n in range(ord('a'),ord('z')+1))+"|_" 
    capletters = '|'.join(chr(n) for n in range(ord('A'),ord('Z')+1)) 
    all_characters = "0|1|2|3|4|5|6|7|8|9|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|!|#|$|%|&|\(|\)|\*|+|,|-|.|/|:|;|<|=|>|?|@|[|]|^|_|`|{|}|~| |\\||\'"

    lexer = Lexer([
    (number, f'(((({nonzero_digits})({zero_digits})*)|0)(.({zero_digits})*))|((({nonzero_digits})({zero_digits})*)|0)'),
    (string, f'\"(({all_characters})|(\\\\\"))*\"'),
    ('[comment]', f'//'),
    ("[LineJump]", "[LineJump]"),
    (Print, 'print'),
    (oPar, "\("),
    (cPar, "\)"),
    (oBrace, '{'),
    (cBrace, '}'),
    (Semi, ';'),
    (Equal, '='),
    (Plus, '+'),
    (Minus, '-'),
    (Pow, '^'),
    (PowStar, '\*\*'),
    (Mult, "\*"),
    (Div, '/'),
    (Arrow, '=>'),
    (Mod, '%'),
    (And, 'and'),
    (Or, 'or'),
    (Not, 'not'),
    (Less, '<'),
    (Greater, '>'),
    (CompEqual, '=='),
    (LessEqual, '<='),
    (GreaterEqual, '>='),
    (NotEqual, '!='),
    (Is, 'is'),
    (In, 'in'),
    (_True, 'True'),
    (_False, 'False'),
    (Comma, ','),
    (Dot, '.'),
    (If, 'if'),
    (Else, 'else'),
    (While, 'while'),
    (For, 'for'),
    (Let, 'let'),
    (_self, 'self'),
    ('space', '  *'),
    (Function, 'function'),
    (Colon, ':'),
    (Elif, 'elif'),
    (arroba, '@'),
    (arroba2, '@@'),
    (Type, 'type'),
    (Inherits, 'inherits'),
    (New, 'new'),
    (In, 'in'),
    (sComil, '\''),
    (dComill, '\"'),
    (sqrt, 'sqrt'),
    (sin, 'sin'),
    (cos, 'cos'),
    (tan, 'tan'),
    (exp, 'exp'),
    (log, 'log'),
    (rand, 'rand'),
    (PI, 'PI'),
    (Destroy, ':='),
    
    (identifier, f'({minletters}|{capletters})({minletters}|{zero_digits}|{capletters})*')
], G.EOF)
    
    return G, lexer
