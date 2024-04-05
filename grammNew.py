from cmp.pycompiler import Grammar
from semantic_checking.AST import *
from lexer import Lexer
import string as stringMod

def gramm_Hulk_LR1():
    G = Grammar()
    Program = G.NonTerminal('Program', True)
    statement_list, statement, expression , expression , term, factor, method_call, arguments, parameters = G.NonTerminals('statement_list statement expression expression term factor method_call arguments parameters')
    type_definition, attribute_definition, method_definition, inheritance, instance_creation, member_access, type_annotation = G.NonTerminals('type_definition attribute_definition method_definition inheritance instance_creation member_access type_annotation')
    print_statement, assignment, function_definition, control_structure, contElif, contElse= G.NonTerminals('print_statement assignment function_definition control_structure contElif contElse')
    if_structure, while_structure, for_structure, create_statement, non_create_statement, expr_statementWithoutSemi = G.NonTerminals('if_structure while_structure for_structure create_statement non_create_statement expr_statementWithoutSemi')
    let_in, multi_assignment, kern_assignment, destructive_assignment, let_in_as_expression , expr_statement= G.NonTerminals('let_in multi_assignment kern_assignment destructive_assignment let_in_as_expr expr_statement')
    cont_member, kern_instance_creation, concatStrings, concatStringsWithSpace, math_call, factorPow = G.NonTerminals('cont_member kern_instance_creation concatStrings concatStringsWithSpace math_call factorPow')
    Print, oPar, cPar, oBrace, cBrace, Semi, Equal, Plus, Minus, Mult, Div, Arrow, Mod, Destroy, Pow = G.Terminals('print ( ) { } ; = + - * / => % := ^')
    And, Or, Not, Less, Greater, CompEqual, LessEqual, GreaterEqual, NotEqual, Is, In, _True, _False = G.Terminals('and or not < > == <= >= != is in True False')
    Comma, Dot, If, Else, While, For, Let, Function, Colon, PowMult, _self = G.Terminals(', Dot if else while for Let Function : ** self')
    identifier, number, string, Elif, Type, Inherits, New, In, arroba, arroba2,PI   = G.Terminals('identifier number string elif type Inherits New in @ @@ PI') 
    sComil, dComill, = G.Terminals('\' \"')
    sqrt, sin, cos, tan, exp, log, rand = G.Terminals('sqrt sin cos tan exp log rand')
    statement_list, body, attribute_call, member_access, type_body_2, type_body = G.NonTerminals('statement_list body attribute_call member_access type_body_2 type_body')
    ExprAnd, ExprNeg, ExprIsType, ExprComp, ExprNum, ExprOr, ExprComp2, ExprConcat= G.NonTerminals('ExprAnd ExprNeg ExprIsType ExprComp ExprNum ExprOr ExprComp2 ExprConcat')
    atom, function_call, declarations,eol_expression , expr_list, simple_expression , arguments_2, optional_typing_var, parameters_2, optional_typing_param, params_for_type = G.NonTerminals('atom function_call declarations eol_expr expr_list simple_expression arguments_2 optional_typing_var parameters_2 optional_typing_param params_for_type')
    

    # A Program is 0 or more functions, types or protocols declarations followed by a single expression
    Program %= eol_expression , lambda h, s: hulk_ast_nodes.ProgramNode([], s[1])
    Program %= declarations + eol_expression , lambda h, s: hulk_ast_nodes.ProgramNode(s[1], s[2])

    declarations %= declarations + function_definition, lambda h, s: s[1] + [s[2]]
    declarations %= function_definition, lambda h, s: [s[1]]
    declarations %= declarations + type_definition, lambda h, s: s[1] + [s[2]]
    declarations %= type_definition, lambda h, s: [s[1]]

    # An end of line expression is an expression followed by a Semi or an expression block
    eol_expression %= expression + Semi, lambda h, s: s[1]
    eol_expression %= body, lambda h, s: s[1]

    # An expression block is a sequence of expressions between brackets
    body %= oBrace + expr_list + cBrace, lambda h, s: hulk_ast_nodes.ExpressionBlockNode(s[2])

    expr_list %= eol_expression + expr_list, lambda h, s: [s[1]] + s[2]
    expr_list %= eol_expression , lambda h, s: [s[1]]

    # An expression is a simple expression or an expression block
    expression %= body, lambda h, s: s[1]
    expression %= simple_expression , lambda h, s: s[1]

    simple_expression %= if_structure, lambda h, s: s[1]
    simple_expression %= let_in, lambda h, s: s[1]
    simple_expression %= while_structure, lambda h, s: s[1]
    simple_expression %= for_structure, lambda h, s: s[1]
    simple_expression %= destructive_assignment, lambda h, s: s[1]

    destructive_assignment %= (member_access + Destroy + expression ,
                               lambda h, s: hulk_ast_nodes.DestructiveAssignmentNode(s[1], s[3]))
    destructive_assignment %= ExprOr, lambda h, s: s[1]

    ExprOr %= ExprOr + Or + ExprAnd, lambda h, s: hulk_ast_nodes.OrNode(s[1], s[3])
    ExprOr %= ExprAnd, lambda h, s: s[1]

    ExprAnd %= ExprAnd + And + ExprComp, lambda h, s: hulk_ast_nodes.AndNode(s[1], s[3])
    ExprAnd %= ExprComp, lambda h, s: s[1]

    ExprComp %= ExprComp + CompEqual + ExprComp2, lambda h, s: hulk_ast_nodes.EqualNode(s[1], s[3])
    ExprComp %= ExprComp + NotEqual + ExprComp2, lambda h, s: hulk_ast_nodes.NotEqualNode(s[1], s[3])
    ExprComp %= ExprComp2, lambda h, s: s[1]

    ExprComp2 %= (ExprComp2 + LessEqual + ExprIsType,
                   lambda h, s: hulk_ast_nodes.LessOrEqualNode(s[1], s[3]))
    ExprComp2 %= (ExprComp2 + GreaterEqual + ExprIsType,
                   lambda h, s: hulk_ast_nodes.GreaterOrEqualNode(s[1], s[3]))
    ExprComp2 %= (ExprComp2 + Less + ExprIsType,
                   lambda h, s: hulk_ast_nodes.LessThanNode(s[1], s[3]))
    ExprComp2 %= (ExprComp2 + Greater + ExprIsType,
                   lambda h, s: hulk_ast_nodes.GreaterThanNode(s[1], s[3]))
    ExprComp2 %= ExprIsType, lambda h, s: s[1]

    ExprIsType %= ExprConcat + Is + identifier, lambda h, s: hulk_ast_nodes.IsNode(s[1], s[3])
    ExprIsType %= ExprConcat, lambda h, s: s[1]

    ExprConcat %= (ExprConcat + arroba + ExprNum,
                         lambda h, s: hulk_ast_nodes.ConcatNode(s[1], s[3]))
    ExprConcat %= (ExprConcat + arroba2 + ExprNum,
                         lambda h, s: hulk_ast_nodes.ConcatNode(
                             hulk_ast_nodes.ConcatNode(s[1], hulk_ast_nodes.ConstantStringNode("\" \"")),
                             s[3]))
    ExprConcat %= ExprNum, lambda h, s: s[1]

    ExprNum %= (ExprNum + Plus + factor,
                                lambda h, s: hulk_ast_nodes.PlusNode(s[1], s[3]))
    ExprNum %= (ExprNum + Minus + factor,
                                lambda h, s: hulk_ast_nodes.MinusNode(s[1], s[3]))
    ExprNum %= factor, lambda h, s: s[1]

    factor %= (factor + Mult + factorPow,
                                  lambda h, s: hulk_ast_nodes.MultNode(s[1], s[3]))
    factor %= (factor + Div + factorPow,
                                  lambda h, s: hulk_ast_nodes.DivNode(s[1], s[3]))
    factor %= (factor + Mod + factorPow,
                                  lambda h, s: hulk_ast_nodes.ModNode(s[1], s[3]))
    factor %= factorPow, lambda h, s: s[1]

    #factorPow %= Plus + factorPow, lambda h, s: s[2]
    #factorPow %= Minus + factorPow, lambda h, s: hulk_ast_nodes.NegNode(s[2])
    #factorPow %= factorPow, lambda h, s: s[1]

    factorPow %= kern_instance_creation + Pow + factorPow, lambda h, s: hulk_ast_nodes.PowNode(s[1], s[3], s[2])
    factorPow %= kern_instance_creation + PowMult + factorPow, lambda h, s: hulk_ast_nodes.PowNode(s[1], s[3], s[2])
    factorPow %= kern_instance_creation, lambda h, s: s[1]

    kern_instance_creation %= (New + identifier + oPar + arguments + cPar,
                           lambda h, s: hulk_ast_nodes.TypeInstantiationNode(s[2], s[4]))
    kern_instance_creation %= ExprNeg, lambda h, s: s[1]

    ExprNeg %= Not + member_access, lambda h, s: hulk_ast_nodes.NotNode(s[2])
    ExprNeg %= member_access, lambda h, s: s[1]

    member_access %= (
        member_access + Dot + identifier + oPar + arguments + cPar,
        lambda h, s: hulk_ast_nodes.MethodCallNode(s[1], s[3], s[5]))
    member_access %= (member_access + Dot + identifier,
                                                 lambda h, s: hulk_ast_nodes.AttributeCallNode(s[1], s[3]))
    
    member_access %= factor, lambda h, s: s[1]

    factor %= oPar +expression + cPar, lambda h, s: s[2]
    factor %= atom, lambda h, s: s[1]

    atom %= number, lambda h, s: hulk_ast_nodes.ConstantNumNode(s[1])
    atom %= _True, lambda h, s: hulk_ast_nodes.ConstantBoolNode(s[1])
    atom %= _False, lambda h, s: hulk_ast_nodes.ConstantBoolNode(s[1])
    atom %= string, lambda h, s: hulk_ast_nodes.ConstantStringNode(s[1])
    atom %= identifier, lambda h, s: hulk_ast_nodes.VariableNode(s[1])
    atom %= function_call, lambda h, s: s[1]

    # Function call
    function_call %= identifier + oPar + arguments + cPar, lambda h, s: hulk_ast_nodes.FunctionCallNode(s[1], s[3])

    arguments %= G.Epsilon, lambda h, s: []
    arguments %= arguments_2, lambda h, s: s[1]

    arguments_2 %= expression , lambda h, s: [s[1]]
    arguments_2 %= expression + Comma + arguments_2, lambda h, s: [s[1]] + s[3]

    # Let in expression
    let_in %= Let + assignment + In + expression , lambda h, s: hulk_ast_nodes.LetInNode(s[2], s[4])

    assignment %= assignment + Comma + optional_typing_var, lambda h, s: s[1] + [s[3]]
    assignment %= optional_typing_var, lambda h, s: [s[1]]

    optional_typing_var %= identifier + Equal + expression , lambda h, s: hulk_ast_nodes.VarDeclarationNode(s[1], s[3])
    optional_typing_var %= (identifier + Colon + identifier + Equal + expression ,
                            lambda h, s: hulk_ast_nodes.VarDeclarationNode(s[1], s[5], s[3]))

    # Functions can be declared using lambda notation or classic notation
    function_definition %= (Function + identifier + oPar + parameters + cPar + Arrow + simple_expression + Semi,
                             lambda h, s: hulk_ast_nodes.FunctionDeclarationNode(s[2], s[4], s[7]))
    function_definition %= (Function + identifier + oPar + parameters + cPar + body,
                             lambda h, s: hulk_ast_nodes.FunctionDeclarationNode(s[2], s[4], s[6]))
    function_definition %= (Function + identifier + oPar + parameters + cPar + body + Semi,
                             lambda h, s: hulk_ast_nodes.FunctionDeclarationNode(s[2], s[4], s[6]))

    # specifying return type
    function_definition %= (
        Function + identifier + oPar + parameters + cPar + Colon + identifier + Arrow + simple_expression + Semi,
        lambda h, s: hulk_ast_nodes.FunctionDeclarationNode(s[2], s[4], s[9], s[7]))
    function_definition %= (Function + identifier + oPar + parameters + cPar + Colon + identifier + body,
                             lambda h, s: hulk_ast_nodes.FunctionDeclarationNode(s[2], s[4], s[8], s[7]))
    function_definition %= (
        Function + identifier + oPar + parameters + cPar + Colon + identifier + body + Semi,
        lambda h, s: hulk_ast_nodes.FunctionDeclarationNode(s[2], s[4], s[8], s[7]))

    parameters %= parameters_2, lambda h, s: s[1]
    parameters %= G.Epsilon, lambda h, s: []

    parameters_2 %= optional_typing_param, lambda h, s: [s[1]]
    parameters_2 %= parameters_2 + Comma + optional_typing_param, lambda h, s: s[1] + [s[3]]

    optional_typing_param %= identifier, lambda h, s: (s[1], None)
    optional_typing_param %= identifier + Colon + identifier, lambda h, s: (s[1], s[3])

    # if_structure expressions must have one if and one else and can 0 or more elifs
    if_structure %= (If + oPar +expression + cPar +expression + contElif + Else + expression ,
                    lambda h, s: hulk_ast_nodes.if_structureNode([(s[3], s[5])] + s[6], s[8]))
    contElif %= (Elif + oPar +expression + cPar +expression + contElif,
                           lambda h, s: [(s[3], s[5])] + s[6])
    contElif %= G.Epsilon, lambda h, s: []

    # Loop expression
    while_structure %= While + oPar +expression + cPar + expression , lambda h, s: hulk_ast_nodes.WhileNode(s[3], s[5])

    for_structure %= (For + oPar + identifier + In +expression + cPar + expression ,
                 lambda h, s: hulk_ast_nodes.ForNode(s[3], s[5], s[7]))

    # Type declaration
    type_definition %= (
        Type + identifier + params_for_type + inheritance + oBrace + type_body + cBrace,
        lambda h, s: hulk_ast_nodes.TypeDeclarationNode(s[2], s[3], s[6], s[4]))
    type_definition %= (
        Type + identifier + params_for_type + Inherits + identifier + oPar + arguments + cPar + oBrace + type_body + cBrace,
        lambda h, s: hulk_ast_nodes.TypeDeclarationNode(s[2], s[3], s[10], s[5], s[7]))

    inheritance %= Inherits + identifier, lambda h, s: s[2]
    inheritance %= G.Epsilon, lambda h, s: None

    params_for_type %= oPar + parameters + cPar, lambda h, s: s[2]
    params_for_type %= G.Epsilon, lambda h, s: None

    type_body %= G.Epsilon, lambda h, s: []
    type_body %= type_body_2, lambda h, s: s[1]

    type_body_2 %= type_body_2 + attribute_definition, lambda h, s: s[1] + [s[2]]
    type_body_2 %= type_body_2 + method_definition, lambda h, s: s[1] + [s[2]]
    type_body_2 %= attribute_definition, lambda h, s: [s[1]]
    type_body_2 %= method_definition, lambda h, s: [s[1]]

    # Method declaration
    method_definition %= (identifier + oPar + parameters + cPar + Arrow + simple_expression + Semi,
                           lambda h, s: hulk_ast_nodes.MethodDeclarationNode(s[1], s[3], s[6]))
    method_definition %= (identifier + oPar + parameters + cPar + body,
                           lambda h, s: hulk_ast_nodes.MethodDeclarationNode(s[1], s[3], s[5]))
    method_definition %= (identifier + oPar + parameters + cPar + body + Semi,
                           lambda h, s: hulk_ast_nodes.MethodDeclarationNode(s[1], s[3], s[5]))

    # specifying return type
    method_definition %= (identifier + oPar + parameters + cPar + Colon + identifier + Arrow + simple_expression + Semi,
                           lambda h, s: hulk_ast_nodes.MethodDeclarationNode(s[1], s[3], s[8], s[6]))
    method_definition %= (identifier + oPar + parameters + cPar + Colon + identifier + body,
                           lambda h, s: hulk_ast_nodes.MethodDeclarationNode(s[1], s[3], s[7], s[6]))
    method_definition %= (identifier + oPar + parameters + cPar + Colon + identifier + body + Semi,
                           lambda h, s: hulk_ast_nodes.MethodDeclarationNode(s[1], s[3], s[7], s[6]))

    # Attribute declaration
    attribute_definition %= identifier + Equal + eol_expression , lambda h, s: hulk_ast_nodes.AttributeDeclarationNode(s[1], s[3])
    attribute_definition %= (identifier + Colon + identifier + Equal + eol_expression ,
                  lambda h, s: hulk_ast_nodes.AttributeDeclarationNode(s[1], s[5], s[3]))


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
    (PowMult, '\*\*'),
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
    (Let, 'Let'),
    (_self, 'self'),
    ('space', '  *'),
    (Function, 'Function'),
    (Colon, ':'),
    (Elif, 'elif'),
    (arroba, '@'),
    (arroba2, '@@'),
    (Type, 'type'),
    (Inherits, 'Inherits'),
    (New, 'New'),
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
