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
    Comma, Dot, If, Else, While, For, Let, Function, Colon, PowStar, _self = G.Terminals(', Dot if else while for let function : ** self')
    identifier, number, string, Elif, Type, Inherits, New, In, arroba, arroba2,PI   = G.Terminals('identifier number string elif type inherits new in @ @@ PI') 
    sComil, dComill, = G.Terminals('\' \"')
    sqrt, sin, cos, tan, exp, log, rand = G.Terminals('sqrt sin cos tan exp log rand')
    list_statement_body = G.NonTerminal('list_statement_body')
    
    Program %= statement_list, lambda h, s: ProgramNode(s[1])
    statement_list %= statement + statement_list, lambda h, s: [s[1]] + s[2] 
    statement_list %= oBrace + statement_list + cBrace + statement_list , lambda h, s: s[2] + s[4]
    statement_list %= G.Epsilon, lambda h, s: []
    
    identifier2,body,statement_body = G.NonTerminals('identifier2 body statement_body')
    #statement %= expr_statement + Semi, lambda h, s: s[1] 
    statement %= type_definition, lambda h, s: s[1]
    statement %= function_definition, lambda h, s: s[1]
    statement %= statement_body, lambda h, s: s[1]
    
    statement_body %= control_structure, lambda h, s: s[1]    
    statement_body %= assignment + Semi, lambda h, s:s[1]
    statement_body %= expression + Semi, lambda h, s: s[1]
    #statement_body %= G.Epsilon, lambda h, s: []
    
    list_statement_body %= statement_body + list_statement_body, lambda h, s: [s[1]] + s[2]
    list_statement_body %= statement_body, lambda h, s: [s[1]] + s[2]
    #list_statement_body %= G.Epsilon, lambda h, s: []
    
    body %= oBrace + list_statement_body + cBrace, lambda h,s:s[2]
    
    
    #factor %= assignment + In + expression, lambda h, s: LetInExpressionNode(s[1], s[3])
    
    control_structure %= if_structure , lambda h, s: s[1]
    control_structure %= while_structure , lambda h, s: s[1]
    control_structure %= for_structure , lambda h, s: s[1]
    
    if_structure %= If + oPar + expression + cPar + body + contElif + contElse , lambda h, s: IfStructureNode(s[3], s[5], s[6], s[7])
    contElif %= Elif + oPar + expression + cPar + body + contElif , lambda h, s: [ElifStructureNode(s[3],s[5])] + s[6]
    contElif %= G.Epsilon , lambda h, s: []
    contElse %= Else + body , lambda h, s: ElseStructureNode(s[2])
    contElse %= G.Epsilon , lambda h, s:  ElseStructureNode([])
    while_structure %= While + oPar + expression + cPar + body , lambda h, s:  WhileStructureNode(s[3], s[5])
    for_assignment,kern_assignment_self = G.NonTerminals('for_assignment kern_assignment_self')
    for_structure %= For + oPar + assignment + Semi + expression + Semi + assignment + cPar + body , lambda h, s:  ForStructureNode(s[3], s[5], s[7], s[9])
    
    assignment %= Let + identifier + Equal + expression + Comma + kern_assignment, lambda h, s: s[2]
    assignment %= _self + Dot + identifier + Equal + expression + Comma + kern_assignment, lambda h, s: [s[1]] + s[3]
    assignment %= Let + identifier + Equal + expression + Comma + assignment, lambda h, s: s[2]
    assignment %= _self + Dot + identifier + Equal + expression + Comma + assignment, lambda h, s: [s[1]] + s[3]
    assignment %= Let + identifier + Equal + expression , lambda h, s: s[2]
    assignment %= _self + Dot + identifier + Equal + expression, lambda h, s: [s[1]] + s[3]
    kern_assignment %= identifier + Equal + expression + Comma + kern_assignment, lambda h, s: KernAssigmentNode(s[1],s[3])  
    kern_assignment %= identifier + Equal + expression, lambda h, s: KernAssigmentNode(s[1],s[3])  
    assignment %= identifier + Destroy + expression + Comma + kern_assignment, lambda h, s: [DestroyNode(s[1], s[3])]
    assignment %= identifier + Destroy + expression, lambda h, s: [DestroyNode(s[1], s[3])]
    kern_assignment %= identifier + Destroy + expression + Comma + kern_assignment
    kern_assignment %= identifier + Destroy + expression
   
    function_definition %= Function + identifier + oPar + parameters + cPar + type_annotation + body, lambda h, s: FunctionDefinitionNode(IdentifierNode(s[2]),s[5],s[4],s[6]) 
    function_definition %= Function + identifier + oPar + parameters + cPar + type_annotation + Arrow + expression,lambda h, s: FunctionDefinitionNode(IdentifierNode(s[2]),s[6],s[4],[s[8]])
    
    parameters %= identifier + type_annotation + Comma + parameters, lambda h, s: [{IdentifierNode(s[1]):s[2]}] + [s[4]]
    parameters %= identifier + type_annotation, lambda h, s: {IdentifierNode(s[1]):s[2]}
    parameters %= G.Epsilon, lambda h, s:[]
    
    type_annotation %= Colon + identifier, lambda h, s: TypeNode(s[2]) 
    type_annotation %= G.Epsilon, lambda h, s: TypeNode('object')
    
    ExprAnd, ExprNeg, ExprIsType, ExprComp, ExprNum, ExprOr= G.NonTerminals('ExprAnd ExprNeg ExprIsType ExprComp ExprNum ExprOr')
    
    expression %= ExprOr, lambda h, s: s[1] 
    expression %= expression + arroba2 + ExprOr, lambda h, s:  StringConcatWithSpaceNode(s[1],s[3])
    expression %= expression + arroba + ExprOr, lambda h, s:  StringConcatNode(s[1],s[3])
    

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
    factorPow %= factor + PowStar + factorPow , lambda h, s:  PowExpressionNode(s[1],s[3])

    factor %= number, lambda h, s:  NumberNode(s[1])
    factor %= string, lambda h, s:  StringNode(s[1])
    factor %= _False, lambda h, s:  BooleanNode(s[1])
    factor %= _True, lambda h, s:  BooleanNode(s[1])
    factor %= math_call, lambda h, s:  s[1]
    factor %= control_structure, lambda h, s: s[1]
    factor %= oPar + assignment + cPar, lambda h, s: s[2] 
    factor %= _self + Dot + identifier, lambda h, s: SelfNode(IdentifierNode(s[3])) 
    factor %= body, lambda h, s:s[1]
    factor %= identifier + oPar + arguments + cPar, lambda h, s: FunctionCallNode(IdentifierNode(s[1]),s[3])
    factor %= factor + Dot + identifier + oPar + arguments + cPar , lambda h, s: MemberAccessNode(s[1], IdentifierNode(s[3]), s[5])   
    factor %= New + identifier + oPar + arguments + cPar, lambda h, s: KernInstanceCreationNode(IdentifierNode(s[2]),s[4])
    factor %= oPar + expression + cPar , lambda h, s:  s[2]
    factor %= oPar + assignment + In + expression + cPar, lambda h, s: LetInExpressionNode(s[1], s[3])
    factor %= Print + oPar + expression + cPar, lambda h, s: PrintStatmentNode(s[3])
    factor %= identifier, lambda h, s:s[1]
    #identifier2 %= identifier, lambda h, s:  IdentifierNode(s[1])
    
    math_call %= sqrt + oPar + ExprNum + cPar, lambda h, s: SqrtMathNode(s[3])
    math_call %= cos + oPar + ExprNum + cPar, lambda h, s: CosMathNode(s[3])
    math_call %= sin + oPar + ExprNum + cPar, lambda h, s: SinMathNode(s[3])
    math_call %= tan + oPar + ExprNum + cPar, lambda h, s: TanMathNode(s[3])
    math_call %= exp + oPar + ExprNum + cPar, lambda h, s: ExpMathNode(s[3])
    math_call %= log + oPar + ExprNum + Comma + ExprNum + cPar, lambda h, s:  LogCallNode(s[3],s[5]) 
    math_call %= rand + oPar + cPar,  lambda h, s: RandomCallNode()
    math_call %= PI, lambda h, s: PINode()
    
    
    arguments %= expression + Comma + arguments, lambda h, s: [s[1]] + s[3]
    arguments %= expression , lambda h, s: [s[1]]
    arguments %= G.Epsilon, lambda h, s: []
    
    # Estructuras adicionales para tipos
    type_definition %= Type + identifier + oPar + parameters + cPar + inheritance + oBrace + attribute_definition + method_definition + cBrace, lambda h, s: TypeDefinitionNode(IdentifierNode(s[2]),s[4], s[6], s[8],s[9])
    type_definition %= Type + identifier + inheritance + oBrace + attribute_definition + method_definition + cBrace, lambda h, s: TypeDefinitionNode(IdentifierNode(s[2]),[], s[6], s[8],s[9])

    attribute_definition %= kern_assignment + Semi + attribute_definition, lambda h, s: s[5] + [s[3]]
    attribute_definition %= G.Epsilon, lambda h, s: []

    method_definition %= identifier + oPar + parameters + cPar + type_annotation + body + method_definition, lambda h, s: [FunctionDefinitionNode(IdentifierNode(s[1]), s[5], s[3],s[6])] + s[7]
    method_definition %= identifier + oPar + parameters + cPar + type_annotation + Arrow + expression + method_definition, lambda h, s: [FunctionDefinitionNode(IdentifierNode(s[1]), s[5], s[3],[s[7]])] + s[8]
    method_definition %= G.Epsilon , lambda h, s: []

    inheritance %= Inherits + identifier, lambda h, s: InheritanceNode(IdentifierNode(s[2]))
    inheritance %= G.Epsilon, lambda h, s: InheritanceNode("object")
    
    nonzero_digits = '|'.join(str(n) for n in range(1,10))
    zero_digits = '|'.join(str(n) for n in range(0,10))
    minletters = '|'.join(chr(n) for n in range(ord('a'),ord('z')+1))+"|_" 
    capletters = '|'.join(chr(n) for n in range(ord('A'),ord('Z')+1)) 
    all_characters = "0|1|2|3|4|5|6|7|8|9|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|!|#|$|%|&|\(|\)|\*|+|,|-|.|/|:|;|<|=|>|?|@|[|]|^|_|`|{|}|~| |\\||\'"

    lexer = Lexer([
    (number, f'(((({nonzero_digits})({zero_digits})*)|0)(.({zero_digits})*))|((({nonzero_digits})({zero_digits})*)|0)'),
    (string, f'\"(({all_characters})|(\\\\\"))*\"'),
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
