from cmp.pycompiler import Grammar

def gramm_Hulk_LR1():
    G = Grammar()
    Program = G.NonTerminal('Program', True)
    statement_list, statement, condition, expression, term, factor, function_call, arguments, parameters = G.NonTerminals('statement_list statement condition expression term factor function_call arguments parameters')
    type_definition, attribute_definition, method_definition, inheritance, instance_creation, member_access, type_annotation = G.NonTerminals('type_definition attribute_definition method_definition inheritance instance_creation member_access type_annotation')
    print_statement, assignment, function_definition, control_structure, contElif, contElse, exp_or_cond= G.NonTerminals('print_statement assignment function_definition control_structure contElif contElse exp_or_cond')
    if_structure, while_structure, for_structure, member,method_override, create_statement, non_create_statement = G.NonTerminals('if_structure while_structure for_structure member method_override create_statement non_create_statement')
    compAritCond, compBoolCond, base_args, let_in, multi_assignment, kern_assignment, op_factor, op_term  = G.NonTerminals('compAritCond compBoolCond base_args let_in multi_assignment kern_assignment op_factor op_term')
    cont_member, kern_instance_creation = G.NonTerminals('cont_member kern_instance_creation')
    Print, oPar, cPar, oBrace, cBrace, Semi, Equal, Plus, Minus, Mult, Div, Arrow, Mod = G.Terminals('print ( ) { } ; = + - * / => %')
    And, Or, Not, Less, Greater, Equal, LessEqual, GreaterEqual, NotEqual, Is, In, _True, _False = G.Terminals('and or not < > == <= >= != is in True False')
    Comma, Dot, If, Else, While, For, Let, Function, Colon = G.Terminals(', . if else while for let function :')
    identifier, number, string, Elif, Type, Inherits, New, In, def_Type   = G.Terminals('identifier number string elif type inherits new in def_Type') 
    sComil, dComill = G.Terminals('\' \"')

    Program %= statement_list
    statement_list %= statement + statement_list
    statement_list %= statement
    statement_list %= G.Epsilon
    
    statement %= non_create_statement  
    statement %= create_statement 
    
    non_create_statement %= print_statement 
    non_create_statement %= control_structure 
    non_create_statement %= exp_or_cond
    
    create_statement %= type_definition
    create_statement %= function_definition 
    create_statement %= assignment
    
    print_statement %= Print + oPar + non_create_statement + cPar + Semi
    kern_assignment %= identifier + Equal + exp_or_cond 
    
    multi_assignment %= kern_assignment + Comma + multi_assignment 
    multi_assignment %= kern_assignment + Semi
    
    assignment %= Let + multi_assignment
    assignment %= instance_creation
    
    type_annotation %= Colon + def_Type 
    type_annotation %= G.Epsilon
    
    function_definition %= Function + identifier + type_annotation + oPar + parameters + cPar + oBrace + statement_list + cBrace 
    function_definition %= Function + identifier + type_annotation + oPar + parameters + cPar + Arrow + non_create_statement  + Semi
    
    parameters %= expression + type_annotation + Comma + parameters 
    parameters %= expression + type_annotation
    parameters %= G.Epsilon
    
    control_structure %= if_structure
    control_structure %= while_structure
    control_structure %= for_structure
    
    if_structure %= If + oPar + condition + cPar + oBrace + statement_list + cBrace + contElif + contElse
    
    contElif %= Elif + oPar + condition + cPar + oBrace + statement_list + cBrace + contElif 
    contElif %= G.Epsilon
    
    contElse %= Else + oBrace + statement_list + cBrace
    contElse %= G.Epsilon
    
    while_structure %= While + oPar + condition + cPar + oBrace + statement_list + cBrace 
    for_structure %= For + oPar + assignment + Semi + condition + Semi + assignment + cPar + oBrace + statement_list + cBrace
    
    compBoolCond %= And 
    compBoolCond %= Or 
    
    compAritCond %= Less
    compAritCond %= Greater 
    compAritCond %= Equal 
    compAritCond %= LessEqual  
    compAritCond %= GreaterEqual 
    compAritCond %= NotEqual 
    
    expression_1, expression_2, expression_3, expression_4, expression_5 = G.NonTerminals('expression_1 expression_2 expression_3 expression_4 expression_5')
    #expression %= Not + expression_1 
    #expression %= expression_1 
    #expression_1 %= expression_2 + Is + def_Type 
    #expression_1 %= expression_2 
    #expression_2 %= expression_3 + compBoolCond + expression_3
    #expression_2 %= expression_3
    #expression_3 %= expression_4 + compAritCond + expression_4 
    #expression_3 %= _False 
    #expression_3 %= _True 
    #expression_3 %= expression_4  
#
    #expression_4 %= term + op_term + term 
    #expression_4 %= term
    # 
    
    #expression %= Not + expression_1
    #expression_1 %= expression_2 + Is + def_Type 
    #expression_2 %= expression_3 + compBoolCond + expression_3
    #expression_4 %= expression_5 + compAritCond + expression_5 
    #expression_5 %= _False 
    #expression_5 %= _True 
#
    #expression_5 %= term + op_term + term 
    #expression_5 %= term
    
    
    expression %= expression_1 + Is + def_Type 
    expression %= expression_1 
    expression_1 %= expression_2 + compBoolCond + expression_2
    expression_1 %= expression_2
    expression_2 %= expression_3 + compAritCond + expression_3
    expression_2 %= expression_3
    expression_3 %= Not + expression_4
    expression_3 %= expression_4
    
    expression_4 %= term + op_term + term 
    expression_4 %= term

    op_term %= Plus 
    op_term %= Minus
    
    term %= factor + op_factor + factor 
    term %= factor
    
    op_factor %= Mult 
    op_factor %= Div 
    op_factor %= Mod
    
    factor %= number
    factor %= oPar + expression + cPar 
    factor %= function_call  
    factor %= member_access 
    factor %= identifier  
    factor %= _False 
    factor %= _True 
    
    function_call %= identifier + oPar + arguments + cPar
    base_args %= expression 
    base_args %= G.Epsilon
    
    arguments %= base_args + Comma + arguments
    arguments %= base_args 
    
    #let in
    let_in %= assignment + In + non_create_statement 
    let_in %= assignment + In + oBrace + statement_list + cBrace
    
    # Estructuras adicionales para tipos
    type_definition %= Type + identifier + inheritance + oBrace + attribute_definition + method_definition + cBrace 
    
    attribute_definition %= kern_assignment + Semi + attribute_definition 
    attribute_definition %= G.Epsilon
    
    method_definition %= identifier + oPar + parameters + cPar + oBrace + statement_list + cBrace + method_definition 
    method_definition %= G.Epsilon
    
    inheritance %= Inherits + def_Type
    inheritance %= G.Epsilon
    # Instanciación de tipos
    instance_creation %= Let + identifier + Equal + kern_instance_creation + Semi
    kern_instance_creation %= New + def_Type + oPar + arguments + cPar
    #
    #method_override %= identifier + oPar + parameters + cPar + oBrace + statement_list + cBrace | G.Epsilon
    cont_member %= oPar + arguments + cPar  
    cont_member %= G.Epsilon   
    
    member %= identifier + cont_member
    member_access %= expression + Dot + member
    return G
