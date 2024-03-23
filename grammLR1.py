from cmp.pycompiler import Grammar

def gramm_Hulk_LR1():
    G = Grammar()
    Program = G.NonTerminal('Program', True)
    statement_list, statement, condition, expression, term, factor, function_call, arguments, parameters = G.NonTerminals('statement_list statement condition expression term factor function_call arguments parameters')
    type_definition, attribute_definition, method_definition, inheritance, instance_creation, member_access, type_annotation = G.NonTerminals('type_definition attribute_definition method_definition inheritance instance_creation member_access type_annotation')
    print_statement, assignment, function_definition, control_structure, contElif, contElse = G.NonTerminals('print_statement assignment function_definition control_structure contElif contElse')
    if_structure, while_structure, for_structure, member = G.NonTerminals('if_structure while_structure for_structure member')
    
    Print, oPar, cPar, oBrace, cBrace, Semi, Equal, Plus, Minus, Mult, Div, = G.Terminals('print ( ) { } ; = + - * /')
    And, Or, Not, Less, Greater, Equal, LessEqual, GreaterEqual, NotEqual, Is, In, _True, _False = G.Terminals('and or not < > == >= <= != is in True False')
    Comma, Dot, If, Else, While, For, Let, Function, Colon = G.Terminals(', . if else while for let function :')
    sComil, dComill = G.Terminals('\' \"')
    identifier, number, string, Elif, Type, Inherits, New, In, method_override = G.Terminals('identifier number string elif type inherits new in method_override') 
    compAritCond, compBoolCond = G.NonTerminals('compAritCond compBoolCond')

    Program %= statement_list
    statement_list %= statement + statement_list | G.Epsilon
    statement %= print_statement | function_definition | control_structure | assignment | type_definition
    print_statement %= Print + oPar + expression + cPar + Semi
    assignment %= Let + identifier + Equal + expression + Semi
    
    type_annotation %= identifier + Colon + identifier | identifier
    function_definition %= Function + identifier + oPar + parameters + cPar + oBrace + expression + cBrace + Semi
    parameters %= type_annotation + Comma + parameters | type_annotation
    
    control_structure %= if_structure | while_structure | for_structure
    if_structure %= If + oPar + condition + cPar + oBrace + statement_list + cBrace + contElif + contElse
    contElif %= Elif + oPar + condition + cPar + oBrace + statement_list + cBrace + contElif | G.Epsilon
    contElse %= Else + oBrace + statement_list + cBrace | G.Epsilon
    while_structure %= While + oPar + condition + cPar + oBrace + statement_list + cBrace 
    for_structure %= For + oPar + assignment + Semi + condition + Semi + assignment + cPar + oBrace + statement_list + cBrace
    
    condition %= expression + compAritCond + expression| Not + In + expression | expression + compBoolCond + expression | Not + expression | expression | _True | _True
    compAritCond %= Less | Greater | Equal | LessEqual | GreaterEqual | NotEqual | Is 
    compBoolCond %= And | Or 
    expression %= term + Plus + term | term + Minus + term | term 
    term %= factor + Mult + factor | factor + Div + factor | factor
    factor %= number | string | oPar + expression + cPar | function_call | identifier
    
    function_call %= identifier + oPar + arguments + cPar
    arguments %= expression + Comma + arguments | expression
    
    # Estructuras adicionales para tipos
    type_definition %= Type + identifier + oBrace + attribute_definition + method_definition + cBrace + inheritance
    attribute_definition %= type_annotation + Equal + expression + Semi + attribute_definition | G.Epsilon
    method_definition %= identifier + oPar + parameters + cPar + oBrace + expression + Semi + cBrace + method_definition | G.Epsilon
    inheritance %= Inherits + identifier | G.Epsilon
    # Instanciación de tipos
    instance_creation %= Let + identifier + Equal + New + identifier + oPar + arguments + cPar + In + statement_list
    # Polimorfismo
    method_override %= identifier + oPar + parameters + cPar + oBrace + expression + Semi + cBrace + method_override | G.Epsilon
    member %= identifier + oPar + arguments + cPar | identifier   
    member_access %= identifier + Dot + member + Semi
    return G
