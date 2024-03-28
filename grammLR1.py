from cmp.pycompiler import Grammar
from semantic_checking.AST import *

def gramm_Hulk_LR1():
    G = Grammar()
    Program = G.NonTerminal('Program', True)
    statement_list, statement, condition, expression, term, factor, function_call, arguments, parameters = G.NonTerminals('statement_list statement condition expression term factor function_call arguments parameters')
    type_definition, attribute_definition, method_definition, inheritance, instance_creation, member_access, type_annotation = G.NonTerminals('type_definition attribute_definition method_definition inheritance instance_creation member_access type_annotation')
    print_statement, assignment, function_definition, control_structure, contElif, contElse= G.NonTerminals('print_statement assignment function_definition control_structure contElif contElse')
    if_structure, while_structure, for_structure, create_statement, non_create_statement = G.NonTerminals('if_structure while_structure for_structure create_statement non_create_statement')
    let_in, multi_assignment, kern_assignment = G.NonTerminals('let_in multi_assignment kern_assignment')
    cont_member, kern_instance_creation, concatStrings, concatStringsWithSpace, math_call = G.NonTerminals('cont_member kern_instance_creation concatStrings concatStringsWithSpace math_call')
    Print, oPar, cPar, oBrace, cBrace, Semi, Equal, Plus, Minus, Mult, Div, Arrow, Mod = G.Terminals('print ( ) { } ; = + - * / => %')
    And, Or, Not, Less, Greater, Equal, LessEqual, GreaterEqual, NotEqual, Is, In, _True, _False = G.Terminals('and or not < > == <= >= != is in True False')
    Comma, Dot, If, Else, While, For, Let, Function, Colon = G.Terminals(', . if else while for let function :')
    identifier, number, string, Elif, Type, Inherits, New, In, def_Type, arroba   = G.Terminals('identifier number string elif type inherits new in def_Type @') 
    sComil, dComill, = G.Terminals('\' \"')
    sqrt, sin, cos, tan, exp, log, rand = G.Terminals('sqrt sin cos tan exp log rand')
    
    Program %= statement_list, lambda h, s: ProgramNode(s[1])
    statement_list %= statement + statement_list, lambda h, s: [s[1]] + s[2] 
    statement_list %= G.Epsilon, lambda h, s: []
    
    statement %= non_create_statement, lambda h, s: s[1] 
    statement %= create_statement, lambda h, s: s[1]
    
    non_create_statement %= print_statement, lambda h, s: s[1] 
    non_create_statement %= control_structure, lambda h, s: s[1]
    
    create_statement %= type_definition, lambda h, s: s[1]
    create_statement %= function_definition, lambda h, s: s[1]
    create_statement %= assignment, lambda h, s: s[1]
    
    print_statement %= Print + oPar + non_create_statement + cPar + Semi, lambda h, s: PrintStatmentNode(s[3])
    kern_assignment %= identifier + Equal + expression, lambda h, s: KernAssigmentNode(s[1],s[3])
    
    multi_assignment %= kern_assignment + Comma + multi_assignment, lambda h, s: [s[1]] + s[3]
    multi_assignment %= kern_assignment + Semi, lambda h, s: [s[1]]
    
    assignment %= Let + multi_assignment, lambda h, s: s[2]
    assignment %= instance_creation, lambda h, s: s[1]
    
    type_annotation %= Colon + def_Type, lambda h, s: TypeNode(s[2]) 
    type_annotation %= G.Epsilon, lambda h, s: TypeNode('object')
    
    function_definition %= Function + identifier + oPar + parameters + cPar + oBrace + statement_list + cBrace, lambda h, s: FunctionDefinitionNode(s[2],TypeNode('object'),s[4],s[7]) 
    function_definition %= Function + identifier + oPar + parameters + cPar + type_annotation + Arrow + non_create_statement + Semi,lambda h, s: FunctionDefinitionNode(s[2],s[6],s[4],s[8])
    
    ##--------------------------Redefinir luego-----------------------------------------------
    parameters %= expression + type_annotation + Comma + parameters, lambda h, s: [s[1]] + s[4]
    parameters %= expression + type_annotation, lambda h, s: [s[1]]
    parameters %= G.Epsilon, lambda h, s:[]
    
    control_structure %= if_structure , lambda h, s: s[1]
    control_structure %= while_structure , lambda h, s: s[1]
    control_structure %= for_structure , lambda h, s: s[1]
    
    if_structure %= If + oPar + condition + cPar + oBrace + statement_list + cBrace + contElif + contElse , lambda h, s: IfStructureNode(s[3], s[6], s[8], s[9])
    
    contElif %= Elif + oPar + condition + cPar + oBrace + statement_list + cBrace + contElif , lambda h, s: [ElifStructureNode(s[3],s[6])] + s[8]
    contElif %= G.Epsilon , lambda h, s: []
    
    contElse %= Else + oBrace + statement_list + cBrace , lambda h, s: ElseStructureNode(s[3])
    contElse %= G.Epsilon , lambda h, s:  ElseStructureNode([])
    
    while_structure %= While + oPar + condition + cPar + oBrace + statement_list + cBrace , lambda h, s:  WhileStructureNode(s[3], s[6])
    for_structure %= For + oPar + assignment + Semi + condition + Semi + assignment + cPar + oBrace + statement_list + cBrace , lambda h, s:  ForStructureNode(s[3], s[5], s[7], s[10])
    
    expression_0, expression_1, expression_2, expression_3, expression_4 = G.NonTerminals('expression_0 expression_1 expression_2 expression_3 expression_4')
    
    concatStrings %= expression + arroba + expression, lambda h, s:  StringConcatNode(s[1],s[4])
    concatStringsWithSpace %= expression + arroba + arroba + expression, lambda h, s:  StringConcatWithSpaceNode(s[1],s[4])
    
    expression %= expression_0 + arroba + expression_0, lambda h, s:  StringConcatNode(s[1],s[4])
    expression %= expression_0 + arroba + arroba + expression_0, lambda h, s:  StringConcatWithSpaceNode(s[1],s[4])
    expression_0 %= expression_1 + Is + def_Type, lambda h, s:  BoolIsTypeNode(s[1],s[3])
    expression_0 %= expression_1, lambda h, s:  s[1]
    expression_1 %= expression_2 + And + expression_2, lambda h, s:  BoolAndNode(s[1],s[3])
    expression_1 %= expression_2 + Or + expression_2, lambda h, s:  BoolOrNode(s[1],s[3])
    expression_1 %= expression_2, lambda h, s: s[1]
    expression_2 %= expression_3 + Less + expression_3, lambda h, s:  BoolCompLessNode(s[1],s[3])
    expression_2 %= expression_3 + Greater + expression_3, lambda h, s:  BoolCompGreaterNode(s[1],s[3])
    expression_2 %= expression_3 + Equal + expression_3, lambda h, s:  BoolCompEqualNode(s[1],s[3])
    expression_2 %= expression_3 + LessEqual + expression_3, lambda h, s:  BoolCompLessIqualNode(s[1],s[3])
    expression_2 %= expression_3 + GreaterEqual + expression_3, lambda h, s:  BoolCompGreaterIqualNode(s[1],s[3])
    expression_2 %= expression_3 + NotEqual + expression_3, lambda h, s:  BoolCompNotEqualNode(s[1],s[3])
    expression_2 %= expression_3, lambda h, s: s[1]
    expression_3 %= Not + expression_4, lambda h, s:  BoolNotNode(s[2])
    expression_3 %= expression_4, lambda h, s: s[1]
    
    expression_4 %= term + Plus + expression_4 , lambda h, s:  PlusExpressionNode(s[2],s[1],s[3])
    expression_4 %= term + Minus + expression_4 , lambda h, s:  SubsExpressionNode(s[2],s[1],s[3])
    expression_4 %= term , lambda h, s: s[1]
    
    term %= factor + Mult + term , lambda h, s:  MultExpressionNode(s[1],s[3])
    term %= factor + Div + term , lambda h, s:  DivExpressionNode(s[1],s[3])
    term %= factor + Mod + term , lambda h, s:  ModExpressionNode(s[1],s[3])
    term %= factor , lambda h, s: s[1]
    
    factor %= number, lambda h, s:  NumberNode(s[1])
    factor %= string, lambda h, s:  StringNode(s[1])
    factor %= oPar + expression + cPar , lambda h, s:  s[2]
    factor %= function_call, lambda h, s:  s[1]
    factor %= member_access, lambda h, s:  s[1]
    factor %= math_call, lambda h, s:  s[1]
    factor %= identifier, lambda h, s:  IdentifierNode(s[1])
    factor %= _False, lambda h, s:  BooleanNode(s[1])
    factor %= _True, lambda h, s:  BooleanNode(s[1])
    factor %= kern_instance_creation, lambda h, s: s[1]
    
    kern_instance_creation %= New + def_Type + oPar + arguments + cPar, lambda h, s: KernInstanceCreationNode(s[2],s[4])
    
    function_call %= identifier + oPar + arguments + cPar, lambda h, s:  s[1]
    math_call %= sqrt + oPar + expression_4 + cPar, lambda h, s: SqrtMathNode(s[3])
    math_call %= cos + oPar + expression_4 + cPar, lambda h, s: CosMathNode(s[3])
    math_call %= sin + oPar + expression_4 + cPar, lambda h, s: SinMathNode(s[3])
    math_call %= tan + oPar + expression_4 + cPar, lambda h, s: TanMathNode(s[3])
    math_call %= exp + oPar + expression_4 + cPar, lambda h, s: ExpMathNode(s[3])
    math_call %= log + oPar + expression_4 + Comma + expression_4 + cPar, lambda h, s:  LogCallNode(s[3],s[5]) 
    math_call %= rand + oPar + cPar,  lambda h, s: RandomCallNode()
    
    arguments %= expression + Comma + arguments, lambda h, s: [s[1]]+s[2]
    arguments %= expression , lambda h, s: s[1]
    arguments %= G.Epsilon, lambda h, s: []
    
    #let in
    let_in %= assignment + In + non_create_statement, lambda h, s: LetInNode(s[1], s[3])
    let_in %= assignment + In + oBrace + statement_list + cBrace, lambda h, s: LetInNode(s[1], s[3])
    
    # Estructuras adicionales para tipos
    type_definition %= Type + identifier + inheritance + oBrace + attribute_definition + method_definition + cBrace, lambda h, s: TypeDefinitionNode(s[2],s[3], s[5], s[6])
    
    attribute_definition %= attribute_definition + kern_assignment + Semi, lambda h, s: s[1] + [s[2]]
    attribute_definition %= G.Epsilon, lambda h, s: []
    
    method_definition %= identifier + oPar + parameters + cPar + oBrace + statement_list + cBrace + method_definition, lambda h, s: [MethodDefinitionNode(s[1], TypeNode('object'), s[6])] + s[8]
    method_definition %= G.Epsilon , lambda h, s: []
    
    inheritance %= Inherits + def_Type, lambda h, s: InheritanceNode(s[2])
    inheritance %= G.Epsilon, lambda h, s: InheritanceNode("object")
    # Instanciación de tipos
    instance_creation %= Let + identifier + Equal + New + def_Type + oPar + arguments + cPar + Semi, lambda h, s: InstanceCreationNode(s[2],s[5], s[7])
    #method_override %= identifier + oPar + parameters + cPar + oBrace + statement_list + cBrace | G.Epsilon
    
    cont_member %= oPar + arguments + cPar, lambda h, s: s[2]
    cont_member %= G.Epsilon, lambda h, s: []
    member_access %= factor + Dot + identifier + cont_member , lambda h, s: MemberAccesNode(s[1], s[3], s[4]) 
    return G