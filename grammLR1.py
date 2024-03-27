from cmp.pycompiler import Grammar
from semantic_checking.ast_nodes import *
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
    sqrt, sin, cos, tan, exp, log, rand = G.Terminals('sqrt sin cos tan exp log rand')
    math_op, math_call = G.NonTerminals('math_op math_call')
    
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
    
    print_statement %= Print + oPar + non_create_statement + cPar + Semi, lambda h, s: PrintStatementNode(s[3])
    kern_assignment %= identifier + Equal + expression, lambda h, s: KernAssigmentNode(s[1],s[3])
    
    multi_assignment %= kern_assignment + Comma + multi_assignment, lambda h, s: [s[1]] + s[3]
    multi_assignment %= kern_assignment + Semi, lambda h, s: [s[1]]
    
    assignment %= Let + multi_assignment, lambda h, s: s[2]
    assignment %= instance_creation, lambda h, s: s[1]
    
    type_annotation %= Colon + def_Type, lambda h, s: TypeNode(s[2]) 
    type_annotation %= G.Epsilon, lambda h, s: TypeNode('object')
    
    function_definition %= Function + identifier + type_annotation + oPar + parameters + cPar + oBrace + statement_list + cBrace, lambda h, s: FunctionDefinitionNode(s[2],s[3],s[5],s[8]) 
    function_definition %= Function + identifier + type_annotation + oPar + parameters + cPar + Arrow + non_create_statement + Semi,lambda h, s: FunctionDefinitionNode(s[2],s[3],s[5],s[8])
    
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
    
    compBoolCond %= And , lambda h, s:  s[1]
    compBoolCond %= Or , lambda h, s:  s[1]
    
    compAritCond %= Less , lambda h, s:  s[1]
    compAritCond %= Greater , lambda h, s:  s[1]
    compAritCond %= Equal , lambda h, s:  s[1]
    compAritCond %= LessEqual  
    compAritCond %= GreaterEqual 
    compAritCond %= NotEqual 
    
    expression_1, expression_2, expression_3, expression_4, expression_5 = G.NonTerminals('expression_1 expression_2 expression_3 expression_4 expression_5')
    
    expression %= expression_1 + Is + def_Type 
    expression %= expression_1 
    expression_1 %= expression_2 + compBoolCond + expression_2
    expression_1 %= expression_2
    expression_2 %= expression_3 + compAritCond + expression_3
    expression_2 %= expression_3
    expression_3 %= Not + expression_4
    expression_3 %= expression_4
    
    expression_4 %= term + op_term
    op_term %= Plus + term + op_term
    op_term %= Minus + term + op_term
    op_term %= G.Epsilon
    Plus
    
    term %= factor + op_factor
    op_factor %= Mult + factor + op_factor
    op_factor %= Div + factor + op_factor
    op_factor %= Mod + factor + op_factor
    op_factor %= G.Epsilon

    factor %= number
    factor %= oPar + expression + cPar 
    factor %= function_call  
    factor %= member_access 
    factor %= math_call 
    factor %= identifier  
    factor %= _False 
    factor %= _True 
    

    math_op %= sqrt  
    math_op %= cos  
    math_op %= sin  
    math_op %= tan  
    math_op %= exp 
    math_op %= tan  
    
    function_call %= identifier + oPar + arguments + cPar
    math_call %= math_op + oPar + expression_4 + cPar
    math_call %= log + oPar + expression_4 + Comma + expression_4 + cPar
    math_call %= rand + oPar + cPar
    base_args %= expression 
    base_args %= G.Epsilon
    
    arguments %= base_args + Comma + arguments
    arguments %= base_args 
    
    #let in
    let_in %= assignment + In + non_create_statement 
    let_in %= assignment + In + oBrace + statement_list + cBrace
    
    # Estructuras adicionales para tipos
    type_definition %= Type + identifier + inheritance + oBrace + attribute_definition + method_definition + cBrace 
    
    attribute_definition %= attribute_definition + kern_assignment + Semi 
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
    member_access %= factor + Dot + member
    return G