from cmp.pycompiler import Grammar
# from semantic_checking.ast_nodes import *
from semantic_checking.AST import *
from lexer import Lexer

def gramm_Hulk_LR1():
    G = Grammar()
    Program = G.NonTerminal('Program', True)
    statement_list, statement, condition, expression, term, factor, function_call, arguments, parameters = G.NonTerminals('statement_list statement condition expression term factor function_call arguments parameters')
    type_definition, attribute_definition, method_definition, inheritance, instance_creation, member_access, type_annotation = G.NonTerminals('type_definition attribute_definition method_definition inheritance instance_creation member_access type_annotation')
    print_statement, assignment, function_definition, control_structure, contElif, contElse= G.NonTerminals('print_statement assignment function_definition control_structure contElif contElse')
    if_structure, while_structure, for_structure, create_statement, non_create_statement = G.NonTerminals('if_structure while_structure for_structure create_statement non_create_statement')
    let_in, multi_assignment, kern_assignment, destructive_assignment, let_in_as_expr, expr_statement= G.NonTerminals('let_in multi_assignment kern_assignment destructive_assignment let_in_as_expr expr_statement')
    cont_member, kern_instance_creation, concatStrings, concatStringsWithSpace, math_call, factorPow = G.NonTerminals('cont_member kern_instance_creation concatStrings concatStringsWithSpace math_call factorPow')
    Print, oPar, cPar, oBrace, cBrace, Semi, Equal, Plus, Minus, Mult, Div, Arrow, Mod, Destroy, Pow = G.Terminals('print ( ) { } ; = + - * / => % := ^')
    And, Or, Not, Less, Greater, CompEqual, LessEqual, GreaterEqual, NotEqual, Is, In, _True, _False = G.Terminals('and or not < > == <= >= != is in True False')
    Comma, Dot, If, Else, While, For, Let, Function, Colon = G.Terminals(', . if else while for let function :')
    identifier, number, string, Elif, Type, Inherits, New, In, arroba,PI   = G.Terminals('identifier number string elif type inherits new in @ PI') 
    sComil, dComill, = G.Terminals('\' \"')
    sqrt, sin, cos, tan, exp, log, rand = G.Terminals('sqrt sin cos tan exp log rand')
    
    Program %= statement_list, lambda h, s: ProgramNode(s[1])
    statement_list %= statement + statement_list, lambda h, s: [s[1]] + s[2] 
    statement_list %= G.Epsilon, lambda h, s: []
    statement_list %= oBrace + statement_list + cBrace , lambda h, s: s[2]
    
    statement %= non_create_statement, lambda h, s: s[1] 
    statement %= create_statement, lambda h, s: s[1]
     
    non_create_statement %= control_structure, lambda h, s: s[1]
    non_create_statement %= expr_statement+ Semi , lambda h, s: s[1]
    
    create_statement %= type_definition, lambda h, s: s[1]
    create_statement %= function_definition, lambda h, s: s[1]
    create_statement %= destructive_assignment+ Semi, lambda h, s: s[1]
    
    expr_statement %= print_statement, lambda h, s: s[1]
    expr_statement %= expression, lambda h, s: s[1]
    print_statement %= Print + oPar + expression + cPar, lambda h, s: PrintStatmentNode(s[3])
    
    kern_assignment %= identifier + Equal + kern_instance_creation, lambda h, s: KernAssigmentNode(s[1],s[3])
    control_structure %= if_structure , lambda h, s: s[1]
    control_structure %= while_structure , lambda h, s: s[1]
    control_structure %= for_structure , lambda h, s: s[1]
    
    if_structure %= If + oPar + condition + cPar + oBrace + statement_list + cBrace + contElif + contElse , lambda h, s: IfStructureNode(s[3], s[6], s[8], s[9])

    contElif %= Elif + oPar + condition + cPar + oBrace + statement_list + cBrace + contElif , lambda h, s: [ElifStructureNode(s[3],s[6])] + s[8]
    contElif %= G.Epsilon , lambda h, s: []

    contElse %= Else + oBrace + statement_list + cBrace , lambda h, s: ElseStructureNode(s[3])
    contElse %= G.Epsilon , lambda h, s:  ElseStructureNode([])

    while_structure %= While + oPar + condition + cPar + oBrace + statement_list + cBrace , lambda h, s:  WhileStructureNode(s[3], s[6])
    for_structure %= For + oPar + assignment + Semi + condition + Semi + destructive_assignment + cPar + oBrace + statement_list + cBrace , lambda h, s:  ForStructureNode(s[3], s[5], s[7], s[10])
    
    assignment %= Let + multi_assignment, lambda h, s: s[2]
    multi_assignment %= kern_assignment + Comma + multi_assignment, lambda h, s: [s[1]] + s[3]
    multi_assignment %= kern_assignment + Semi, lambda h, s: [s[1]]
    kern_assignment %= identifier + Equal + expression, lambda h, s: KernAssigmentNode(s[1],s[3])
    
    destructive_assignment %= identifier + Destroy + expression + Comma + destructive_assignment, lambda h, s : [DestroyNode(s[1], s[3])] + s[4]
    destructive_assignment %= identifier + Destroy + expression, lambda h, s: [DestroyNode(s[1], s[3])]

    function_definition %= Function + identifier + oPar + parameters + cPar + type_annotation + oBrace + statement_list + cBrace, lambda h, s: FunctionDefinitionNode(s[2],s[3],s[5],s[8]) 
    function_definition %= Function + identifier + oPar + parameters + cPar + type_annotation + Arrow + non_create_statement,lambda h, s: FunctionDefinitionNode(s[2],s[3],s[5],s[8])
    
    parameters %= expression + type_annotation + Comma + parameters, lambda h, s: [{s[1]:s[2]}] + s[4]
    parameters %= expression + type_annotation, lambda h, s: {s[1]:s[2]}
    parameters %= G.Epsilon, lambda h, s:[]
    
    type_annotation %= Colon + identifier, lambda h, s: TypeNode(s[2]) 
    type_annotation %= G.Epsilon, lambda h, s: TypeNode('object')
    
    ExprAnd, ExprNeg, ExprIsType, ExprComp, ExprNum, ExprOr= G.NonTerminals('ExprAnd ExprNeg ExprIsType ExprComp ExprNum ExprOr')
    
    expression %= ExprOr, lambda h, s: s[1] 
    expression %= expression + arroba + ExprOr, lambda h, s:  StringConcatNode(s[1],s[4])
    expression %= expression + arroba + arroba + ExprOr, lambda h, s:  StringConcatWithSpaceNode(s[1],s[4])
 
    ExprOr %= ExprAnd, lambda h, s: s[1]
    ExprOr %= ExprOr + Or + ExprAnd, lambda h, s:  BoolOrNode(s[1],s[3])
    
    ExprAnd %= ExprNeg, lambda h, s: s[1]
    ExprAnd %= ExprAnd + And + ExprNeg, lambda h, s:  BoolAndNode(s[1],s[3])
    
    ExprNeg %= ExprIsType, lambda h, s: s[1]
    ExprNeg %= Not + ExprIsType, lambda h, s:  BoolNotNode(s[2])
    
    ExprIsType %= ExprComp, lambda h, s: s[1]
    ExprIsType %= ExprComp + Is + identifier, lambda h, s:  BoolIsTypeNode(s[1],s[3])
    
    ExprComp %= ExprNum, lambda h, s: s[1]
    ExprComp %= ExprNum + Less + ExprNum, lambda h, s:  BoolCompLessNode(s[1],s[3])
    ExprComp %= ExprNum + Greater + ExprNum, lambda h, s:  BoolCompGreaterNode(s[1],s[3])
    ExprComp %= ExprNum + CompEqual + ExprNum, lambda h, s:  BoolCompEqualNode(s[1],s[3])
    ExprComp %= ExprNum + LessEqual + ExprNum, lambda h, s:  BoolCompLessEqualNode(s[1],s[3])
    ExprComp %= ExprNum + GreaterEqual + ExprNum, lambda h, s:  BoolCompGreaterEqualNode(s[1],s[3])
    ExprComp %= ExprNum + NotEqual + ExprNum, lambda h, s:  BoolCompNotEqualNode(s[1],s[3])
    
    ExprNum %= term , lambda h, s: s[1]
    ExprNum %= ExprNum + Plus + term , lambda h, s:  PlusExpressionNode(s[1],s[3])
    ExprNum %= ExprNum + Minus + term , lambda h, s:  SubsExpressionNode(s[1],s[3])
    
    term %= factorPow , lambda h, s: s[1]
    term %= term + Mult+ factorPow, lambda h, s:  MultExpressionNode(s[1],s[3])
    term %= term + Div + factorPow, lambda h, s:  DivExpressionNode(s[1],s[3])
    term %= term + Mod + factorPow, lambda h, s:  ModExpressionNode(s[1],s[3])
    
    
    factorPow %= factor, lambda h, s:s[1]
    factorPow %= factor + Pow + factorPow , lambda h, s:  PowExpressionNode(s[1],s[3])
    factor %= oPar + expr_statement + cPar , lambda h, s:  s[2]
    factor %= number, lambda h, s:  NumberNode(s[1])
    factor %= string, lambda h, s:  StringNode(s[1])
    factor %= _False, lambda h, s:  BooleanNode(s[1])
    factor %= _True, lambda h, s:  BooleanNode(s[1])
    factor %= identifier + oPar + arguments + cPar, lambda h, s: FunctionCallNode(s[1],s[3])
    factor %= identifier, lambda h, s:  IdentifierNode(s[1])
    factor %= assignment + In + expr_statement + Semi, lambda h, s: LetInExpressionNode(s[1], s[3])
    factor %= assignment + In + oBrace + statement_list + cBrace, lambda h, s: LetInNode(s[1], s[3])    
    factor %= math_call, lambda h, s:  s[1]
    factor %= member_access, lambda h, s:  s[1]    
    
    member_access %= factor + Dot + identifier + oPar + arguments + cPar , lambda h, s: MemberAccessNode(s[1], s[3], s[5]) 
    #member_access %= factor + Dot + identifier , lambda h, s: MemberAccesNode(s[1], s[3], [])  #Todo member access Los parametros son privados de la clase #! NAOMI ARREGLA ESTO EN EL CHECKEO SEMANTICO ❤️
    kern_instance_creation %= New + identifier + oPar + arguments + cPar, lambda h, s: KernInstanceCreationNode(s[2],s[4])
    
    math_call %= sqrt + oPar + ExprNum + cPar, lambda h, s: SqrtMathNode(s[3])
    math_call %= cos + oPar + ExprNum + cPar, lambda h, s: CosMathNode(s[3])
    math_call %= sin + oPar + ExprNum + cPar, lambda h, s: SinMathNode(s[3])
    math_call %= tan + oPar + ExprNum + cPar, lambda h, s: TanMathNode(s[3])
    math_call %= exp + oPar + ExprNum + cPar, lambda h, s: ExpMathNode(s[3])
    math_call %= log + oPar + ExprNum + Comma + ExprNum + cPar, lambda h, s:  LogCallNode(s[3],s[5]) 
    math_call %= rand + oPar + cPar,  lambda h, s: RandomCallNode()
    math_call %= PI, lambda h, s: PINode(3.1415)
    
    arguments %= expr_statement + Comma + arguments, lambda h, s: [s[1]]+s[2]
    arguments %= expr_statement , lambda h, s: s[1]
    arguments %= G.Epsilon, lambda h, s: []
    
    # Estructuras adicionales para tipos
    type_definition %= Type + identifier + inheritance + oBrace + attribute_definition + method_definition + cBrace, lambda h, s: TypeDefinitionNode(s[2],s[3], s[5], s[6])

    attribute_definition %= attribute_definition + kern_assignment + Semi, lambda h, s: s[1] + [s[2]]
    attribute_definition %= G.Epsilon, lambda h, s: []

    method_definition %= identifier + oPar + parameters + cPar + type_annotation + oBrace + statement_list + cBrace + method_definition, lambda h, s: [FunctionDefinitionNode(s[1], s[3], s[6])] + s[8]
    method_definition %= G.Epsilon , lambda h, s: []

    inheritance %= Inherits + identifier, lambda h, s: InheritanceNode(s[2])
    inheritance %= G.Epsilon, lambda h, s: InheritanceNode("object")
    
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
    (identifier, 'identifier'),
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
