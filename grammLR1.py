from cmp.pycompiler import Grammar
from semantic_checking.AST import *
from lexer import Lexer

def gramm_Hulk_LR1():
    G = Grammar()
    Program = G.NonTerminal('Program', True)
    statement_list, statement, expression, term, factor, function_call, arguments, parameters = G.NonTerminals('statement_list statement expression term factor function_call arguments parameters')
    type_definition, attribute_definition, method_definition, inheritance, instance_creation, member_access, type_annotation = G.NonTerminals('type_definition attribute_definition method_definition inheritance instance_creation member_access type_annotation')
    print_statement, assignment, function_definition, control_structure, contElif, contElse= G.NonTerminals('print_statement assignment function_definition control_structure contElif contElse')
    if_structure, while_structure, for_structure, create_statement, non_create_statement = G.NonTerminals('if_structure while_structure for_structure create_statement non_create_statement')
    let_in, multi_assignment, kern_assignment, destructive_assignment = G.NonTerminals('let_in multi_assignment kern_assignment destructive_assignment')
    cont_member, kern_instance_creation, concatStrings, concatStringsWithSpace, math_call = G.NonTerminals('cont_member kern_instance_creation concatStrings concatStringsWithSpace math_call')
    Print, oPar, cPar, oBrace, cBrace, Semi, Equal, Plus, Minus, Mult, Div, Arrow, Mod, Destroy  = G.Terminals('print ( ) { } ; = + - * / => % :=')
    And, Or, Not, Less, Greater, Equal, LessEqual, GreaterEqual, NotEqual, Is, In, _True, _False = G.Terminals('and or not < > == <= >= != is in True False')
    Comma, Dot, If, Else, While, For, Let, Function, Colon = G.Terminals(', . if else while for let function :')
    Print, oPar, cPar, oBrace, cBrace, Semi, Equal, Plus, Minus, Mult, Div, Arrow, Mod, Pow  = G.Terminals('print ( ) { } ; = + - * / => % ^')
    And, Or, Not, Less, Greater, CompEqual, LessEqual, GreaterEqual, NotEqual, Is, In, _True, _False = G.Terminals('and or not < > == <= >= != is in True False')
    identifier, number, string, Elif, Type, Inherits, New, In, def_Type, arroba   = G.Terminals('identifier number string elif type inherits new in def_Type @') 
    sComil, dComill, = G.Terminals('\' \"')
    sqrt, sin, cos, tan, exp, log, rand, PI = G.Terminals('sqrt sin cos tan exp log rand PI')
    
    Program %= statement_list, lambda h, s: ProgramNode(s[1])
    statement_list %= statement + statement_list, lambda h, s: [s[1]] + s[2] 
    statement_list %= G.Epsilon, lambda h, s: []
    statement_list %= oBrace + statement_list + cBrace , lambda h, s: s[2]
    statement %= non_create_statement + Semi, lambda h, s: s[1] 
    New + def_Type + oPar + arguments + cPar
    statement %= create_statement + Semi, lambda h, s: s[1] 
    
    #statement %= non_create_statement, lambda h, s: s[1]
    #statement %= create_statement, lambda h, s: s[1] 

    #non_create_statement %= print_statement, lambda h, s: s[1] 
    non_create_statement %= control_structure, lambda h, s: s[1]
    
    non_create_statement %= expression, lambda h, s: s[1]
    non_create_statement %= let_in, lambda h, s: s[1] 
    
    create_statement %= type_definition, lambda h, s: s[1]
    create_statement %= function_definition, lambda h, s: s[1]
    create_statement %= assignment, lambda h, s: s[1]
    create_statement %= destructive_assignment, lambda h, s: [1]
    
    print_statement %= Print + oPar + non_create_statement + cPar + Semi, lambda h, s: PrintStatmentNode(s[3])
    kern_assignment %= identifier + Equal + expression, lambda h, s: LetNode(s[1],s[3])
    
    multi_assignment %= kern_assignment + Comma + multi_assignment, lambda h, s: [s[1]] + s[3]
    multi_assignment %= kern_assignment, lambda h, s: [s[1]]
    
    assignment %= Let + multi_assignment, lambda h, s: s[2]
    assignment %= instance_creation, lambda h, s: s[1]
    
    destructive_assignment %= identifier + Destroy + expression + Comma + destructive_assignment, lambda h, s : [DestroyNode(s[1], s[3])] + s[4]
    destructive_assignment %= identifier + Destroy + expression, lambda h, s: [DestroyNode(s[1], s[3])]
    
    function_definition %= Function + identifier + oPar + parameters + cPar + oBrace + statement_list + cBrace, lambda h, s: FunctionDefinitionNode(s[2],TypeNode('object'),s[4],s[7]) 
    function_definition %= Function + identifier + oPar + parameters + cPar + Arrow + type_annotation + non_create_statement + Semi,lambda h, s: FunctionDefinitionNode(s[2],s[3],s[5],s[8])
    
    parameters %= expression + type_annotation + Comma + parameters, lambda h, s: [{s[1]:s[2]}] + s[4]
    parameters %= expression + type_annotation, lambda h, s: {s[1]:s[2]}
    parameters %= G.Epsilon, lambda h, s:[]
    
    control_structure %= if_structure , lambda h, s: s[1]
    control_structure %= while_structure , lambda h, s: s[1]
    control_structure %= for_structure , lambda h, s: s[1]
    
    if_structure %= If + oPar + expression + cPar + oBrace + statement_list + cBrace + contElif + contElse , lambda h, s: IfStructureNode(s[3], s[6], s[8], s[9])
    
    contElif %= Elif + oPar + expression + cPar + oBrace + statement_list + cBrace + contElif , lambda h, s: [ElifStructureNode(s[3],s[6])] + s[8]
    contElif %= G.Epsilon , lambda h, s: []
    
    contElse %= Else + oBrace + statement_list + cBrace , lambda h, s: ElseStructureNode(s[3])
    contElse %= G.Epsilon , lambda h, s:  ElseStructureNode([])
    
    while_structure %= While + oPar + expression + cPar + oBrace + statement_list + cBrace , lambda h, s:  WhileStructureNode(s[3], s[6])
    for_structure %= For + oPar + assignment + Semi + expression + Semi + assignment + cPar + oBrace + statement_list + cBrace , lambda h, s:  ForStructureNode(s[3], s[5], s[7], s[10])
    
    expression_0, expression_1, expression_2, expression_3, expression_4 = G.NonTerminals('expression_0 expression_1 expression_2 expression_3 expression_4')
    
    expression %= print_statement, lambda h, s:s[1]
    expression %= expression_0 + arroba + expression_0, lambda h, s:  StringConcatNode(s[1],s[4])
    expression %= expression_0 + arroba + arroba + expression_0, lambda h, s:  StringConcatWithSpaceNode(s[1],s[4])
    expression %= expression_0 

    expression_0 %= expression_1 + Is + def_Type, lambda h, s:  BoolIsTypeNode(s[1],s[3])
    expression_0 %= expression_1, lambda h, s:  s[1]

    expression_1 %= expression_1 + And + expression_2, lambda h, s:  BoolAndNode(s[1],s[3])
    expression_1 %= expression_1 + Or + expression_2, lambda h, s:  BoolOrNode(s[1],s[3])
    expression_1 %= expression_2, lambda h, s: s[1]

    expression_2 %= expression_3 + Less + expression_3, lambda h, s:  BoolCompLessNode(s[1],s[3])
    expression_2 %= expression_3 + Greater + expression_3, lambda h, s:  BoolCompGreaterNode(s[1],s[3])
    expression_2 %= expression_3 + CompEqual + expression_3, lambda h, s:  BoolCompEqualNode(s[1],s[3])
    expression_2 %= expression_3 + LessEqual + expression_3, lambda h, s:  BoolCompLessEqualNode(s[1],s[3])
    expression_2 %= expression_3 + GreaterEqual + expression_3, lambda h, s:  BoolCompGreaterEqualNode(s[1],s[3])
    expression_2 %= expression_3 + NotEqual + expression_3, lambda h, s:  BoolCompNotEqualNode(s[1],s[3])
    expression_2 %= expression_3, lambda h, s: s[1]

    expression_3 %= Not + expression_4, lambda h, s:  BoolNotNode(s[2])
    expression_3 %= expression_4, lambda h, s: s[1]
    
    #expression_4 %= term + Plus + expression_4 , lambda h, s:  PlusExpressionNode(s[2],s[1],s[3])
    #expression_4 %= term + Minus + expression_4 , lambda h, s:  SubsExpressionNode(s[2],s[1],s[3])
    expression_4 %= expression_4 + Plus + term , lambda h, s:  PlusExpressionNode(s[2],s[1],s[3])
    expression_4 %= expression_4 + Minus + term , lambda h, s:  SubsExpressionNode(s[2],s[1],s[3])
    expression_4 %= term , lambda h, s: s[1]
    
    term %= term + Mult + factor   , lambda h, s:  MultExpressionNode(s[1],s[3])
    term %= term + Div + factor  , lambda h, s:  DivExpressionNode(s[1],s[3])
    term %= term + Mod + factor  , lambda h, s:  ModExpressionNode(s[1],s[3])
    term %= term + Pow + factor , lambda h, s:  PowExpressionNode(s[1],s[3]) 
    term %= factor , lambda h, s: s[1]
    
    factor0, factor_0, factor_1 = G.NonTerminals('factor0 factor_0 factor_1')
    #function_call %= factor0 + oPar + arguments + cPar, lambda h, s:  FunctionCallNode(s[1],s[3]) #Todo function call
    #member_access %= factor0 + Dot + function_call , lambda h, s: MemberAccesNode(s[1], s[3], s[4])  #Todo member access
    #member_access %= factor0 + Dot + factor0 , lambda h, s: MemberAccesNode(s[1], s[3], s[4])  #Todo member access
    factor %= factor_0 + oPar + arguments + cPar, lambda h, s:  FunctionCallNode(s[1],s[3]) #Todo function call
    factor_0 %= factor_1 + Dot + function_call , lambda h, s: MemberAccesNode(s[1], s[3], s[4])  #Todo member access
    factor_0 %= factor0 + Dot + factor0 , lambda h, s: MemberAccesNode(s[1], s[3], s[4])  #Todo member access
    
    #factor %= member_access, lambda h, s:s[1]
    #factor %= function_call, lambda h, s:s[1]
    factor %= factor0, lambda h, s:  s[1]
    factor0 %= assignment + In + expression, lambda h, s: LetInExpressionNode(s[1],s[3])  
    factor0 %= oPar + statement + cPar , lambda h, s:  s[2]
    factor0 %= math_call, lambda h, s:  s[1]
    factor0 %= kern_instance_creation, lambda h, s: s[1]
    factor0 %= identifier, lambda h, s:  IdentifierNode(s[1])
    factor0 %= number, lambda h, s:  NumberNode(s[1])
    factor0 %= string, lambda h, s:  StringNode(s[1])
    factor0 %= _False, lambda h, s:  BooleanNode(s[1])
    factor0 %= _True, lambda h, s:  BooleanNode(s[1])
    
    kern_instance_creation %= New + def_Type + oPar + arguments + cPar, lambda h, s: KernInstanceCreationNode(s[2],s[4])
    
    #identifier + oPar + arguments + cPar, lambda h, s:  FunctionCallNode(s[1],s[3])
    math_call %= sqrt + oPar + expression_4 + cPar, lambda h, s: SqrtMathNode(s[3])
    math_call %= cos + oPar + expression_4 + cPar, lambda h, s: CosMathNode(s[3])
    math_call %= sin + oPar + expression_4 + cPar, lambda h, s: SinMathNode(s[3])
    math_call %= tan + oPar + expression_4 + cPar, lambda h, s: TanMathNode(s[3])
    math_call %= exp + oPar + expression_4 + cPar, lambda h, s: ExpMathNode(s[3])
    math_call %= log + oPar + expression_4 + Comma + expression_4 + cPar, lambda h, s:  LogCallNode(s[3],s[5]) 
    math_call %= rand + oPar + cPar,  lambda h, s: RandomCallNode()
    math_call %= PI, lambda h, s:NumberNode(s[1])
    
    arguments %= expression + Comma + arguments, lambda h, s: [s[1]]+s[2]
    arguments %= expression , lambda h, s: s[1]
    arguments %= G.Epsilon, lambda h, s: []
    
    #let in
    let_in %= assignment + In + oBrace + statement_list + cBrace, lambda h, s: LetInNode(s[1], s[3]) #NO TENGO CLARO CUANDO SE USA () Y CUANDO {}
    
    # Estructuras adicionales para tipos
    type_definition %= Type + identifier + inheritance + oBrace + attribute_definition + method_definition + cBrace, lambda h, s: TypeDefinitionNode(s[2],s[3], s[5], s[6])
    
    attribute_definition %= attribute_definition + kern_assignment + Semi, lambda h, s: s[1] + [s[2]]
    attribute_definition %= G.Epsilon, lambda h, s: []
    
    method_definition %= identifier + oPar + parameters + cPar + oBrace + statement_list + cBrace + method_definition, lambda h, s: [FunctionDefinitionNode(s[1], s[3], s[6])] + s[8]
    method_definition %= G.Epsilon , lambda h, s: []
    
    inheritance %= Inherits + def_Type, lambda h, s: InheritanceNode(s[2])
    inheritance %= G.Epsilon, lambda h, s: InheritanceNode("object")
    # Instanciación de tipos
    instance_creation %= Let + identifier + Equal + New + def_Type + oPar + arguments + cPar + Semi, lambda h, s: InstanceCreationNode(s[2],s[5], s[7])
    #method_override %= identifier + oPar + parameters + cPar + oBrace + statement_list + cBrace | G.Epsilon
    
    
    nonzero_digits = '|'.join(str(n) for n in range(1,10))
    zero_digits = '|'.join(str(n) for n in range(0,10))
    minletters = '|'.join(chr(n) for n in range(ord('a'),ord('z')+1)) 
    capletters = '|'.join(chr(n) for n in range(ord('A'),ord('Z')+1)) 
    all_characters = f"{minletters}| |{capletters}"


    lexer = Lexer([
    (number, f'({nonzero_digits})({zero_digits})*'),
    (string, f'\'({all_characters}|{zero_digits})*\'|\"({all_characters}|{zero_digits})*\"'),
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
    ('space', '  *'),
    (Function, 'function'),
    (Colon, ':'),
    (Elif, 'elif'),
    (arroba, '@'),
    (Type, 'type'),
    (Inherits, 'inherits'),
    (New, 'new'),
    (In, 'in'),
    (def_Type, 'def_Type'),
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
    (identifier, f'({minletters})({minletters}|{zero_digits})*')
], G.EOF)
    
    return G, lexer

    