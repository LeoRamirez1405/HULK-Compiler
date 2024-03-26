from cmp.pycompiler import Grammar

def gramm_Hulk_LR1():
    G = Grammar()
    Program = G.NonTerminal('Program', True)
    statement_list, statement, condition, expression, term, factor, function_call, arguments, parameters = G.NonTerminals('statement_list statement condition expression term factor function_call arguments parameters')
    type_definition, attribute_definition, method_definition, inheritance, instance_creation, member_access, type_annotation = G.NonTerminals('type_definition attribute_definition method_definition inheritance instance_creation member_access type_annotation')
    print_statement, assignment, function_definition, control_structure, contElif, contElse, exp_or_cond= G.NonTerminals('print_statement assignment function_definition control_structure contElif contElse exp_or_cond')
    if_structure, while_structure, for_structure, member,method_override, create_statement, non_create_statement = G.NonTerminals('if_structure while_structure for_structure member method_override create_statement non_create_statement')
    compAritCond, compBoolCond, base_args, let_in, multi_assignment, kern_assignment, op_factor, op_term  = G.NonTerminals('compAritCond compBoolCond base_args let_in multi_assignment kern_assignment op_factor op_term')
    
    Print, oPar, cPar, oBrace, cBrace, Semi, Equal, Plus, Minus, Mult, Div, Arrow, Mod = G.Terminals('print ( ) { } ; = + - * / => %')
    And, Or, Not, Less, Greater, Equal, LessEqual, GreaterEqual, NotEqual, Is, In, _True, _False = G.Terminals('and or not < > == >= <= != is in True False')
    Comma, Dot, If, Else, While, For, Let, Function, Colon = G.Terminals(', . if else while for let function :')
    identifier, number, string, Elif, Type, Inherits, New, In, def_Type   = G.Terminals('identifier number string elif type inherits new in def_Type') 
    sComil, dComill = G.Terminals('\' \"')

    Program %= statement_list
    statement_list %= statement + statement_list | G.Epsilon
    statement %= non_create_statement | create_statement 
    non_create_statement %= print_statement | control_structure | expression
    create_statement %= type_definition | function_definition | assignment
    print_statement %= Print + oPar + non_create_statement + cPar + Semi
    kern_assignment %= identifier + Equal + expression 
    multi_assignment %=  kern_assignment + Colon + multi_assignment | kern_assignment + Semi
    assignment %= Let + multi_assignment | instance_creation
    
    type_annotation %= Colon + def_Type | G.Epsilon
    function_definition %= Function + identifier + type_annotation + oPar + parameters + cPar + oBrace + expression + cBrace + Semi | Function + identifier + type_annotation + oPar + parameters + cPar + Arrow + non_create_statement  + Semi
    parameters %= identifier + type_annotation + Comma + parameters | identifier + type_annotation | G.Epsilon
    
    control_structure %= if_structure | while_structure | for_structure
    if_structure %= If + oPar + condition + cPar + oBrace + statement_list + cBrace + contElif + contElse
    contElif %= Elif + oPar + condition + cPar + oBrace + statement_list + cBrace + contElif | G.Epsilon
    contElse %= Else + oBrace + statement_list + cBrace | G.Epsilon
    while_structure %= While + oPar + condition + cPar + oBrace + statement_list + cBrace 
    for_structure %= For + oPar + assignment + Semi + condition + Semi + assignment + cPar + oBrace + statement_list + cBrace
    
    condition %= expression + compAritCond + expression | Not + condition | condition + compBoolCond + condition | _True | _False | identifier + Is + def_Type | oPar + condition + cPar | function_call | identifier
    compAritCond %= Less | Greater | Equal | LessEqual | GreaterEqual | NotEqual 
    compBoolCond %= And | Or 
    #expression %= term + op_term + term | term 
    #op_term %= Plus | Minus
    #term %= factor + op_factor + factor | factor
    #op_factor %= Mult | Div | Mod
    #factor %= number | string | oPar + expression + cPar | function_call | identifier | member_access
    
    function_call %= identifier + oPar + arguments + cPar
    base_args %= expression | condition | G.Epsilon
    arguments %= base_args + Comma + arguments | base_args 
    
    #let in
    let_in %= assignment + In + non_create_statement | assignment + In + oBrace + statement_list + cBrace
    
    # Estructuras adicionales para tipos
    #type_definition %= Type + identifier + inheritance + oBrace + attribute_definition + method_definition + cBrace 
    exp_or_cond %= expression | condition
    attribute_definition %= identifier + type_annotation + Equal + exp_or_cond + Semi + attribute_definition | G.Epsilon
    method_definition %= identifier + oPar + parameters + cPar + oBrace + statement_list + cBrace + method_definition | G.Epsilon
    inheritance %= Inherits + def_Type | G.Epsilon
    
    # Instanciación de tipos
    instance_creation %= Let + identifier + Equal + New + def_Type + oPar + arguments + cPar + Semi
    #
    method_override %= identifier + oPar + parameters + cPar + oBrace + statement_list + Semi + cBrace | G.Epsilon
    member %= identifier + oPar + arguments + cPar | identifier   
    member_access %= identifier + Dot + member
    return G
