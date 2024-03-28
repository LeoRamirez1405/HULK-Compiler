from cmp.pycompiler import Grammar
from semantic_checking.AST import *
from lexer import Lexer

def gramm_Hulk_LR1():
    G = Grammar()
    Program = G.NonTerminal('Program', True)
    statement_list, statement, condition, expression, term, factor, function_call, arguments, parameters = G.NonTerminals('statement_list statement condition expression term factor function_call arguments parameters')
    type_definition, attribute_definition, method_definition, inheritance, instance_creation, member_access, type_annotation = G.NonTerminals('type_definition attribute_definition method_definition inheritance instance_creation member_access type_annotation')
    print_statement, assignment, function_definition, control_structure, contElif, contElse= G.NonTerminals('print_statement assignment function_definition control_structure contElif contElse')
    if_structure, while_structure, for_structure, create_statement, non_create_statement = G.NonTerminals('if_structure while_structure for_structure create_statement non_create_statement')
    let_in, multi_assignment, kern_assignment = G.NonTerminals('let_in multi_assignment kern_assignment')
    cont_member, kern_instance_creation, concatStrings, concatStringsWithSpace, math_call = G.NonTerminals('cont_member kern_instance_creation concatStrings concatStringsWithSpace math_call')
    
    Comma, Dot, If, Else, While, For, Let, Function, Colon = G.Terminals(', . if else while for let function :')
    Print, oPar, cPar, oBrace, cBrace, Semi, Equal, Plus, Minus, Mult, Div, Arrow, Mod = G.Terminals('print ( ) { } ; = + - * / => %')
    And, Or, Not, Less, Greater, CompEqual, LessEqual, GreaterEqual, NotEqual, Is, In, _True, _False = G.Terminals('and or not < > == <= >= != is in True False')
    identifier, number, string, Elif, Type, Inherits, New, In, def_Type, arroba   = G.Terminals('identifier number string elif type inherits new in def_Type @') 
    sComil, dComill, = G.Terminals('\' \"')
    sqrt, sin, cos, tan, exp, log, rand = G.Terminals('sqrt sin cos tan exp log rand')
    
    Program %= statement_list, lambda h, s: ProgramNode(s[1])
    statement_list %= statement + statement_list, lambda h, s: [s[1]] + s[2] 
    statement_list %= G.Epsilon, lambda h, s: []
    
    statement %= non_create_statement + Semi, lambda h, s: s[1] #AÑADI SEMI
    statement %= create_statement + Semi, lambda h, s: s[1] #AÑADI SEMI
    
    statement %= non_create_statement, lambda h, s: s[1]
    statement %= create_statement, lambda h, s: s[1] 

    non_create_statement %= print_statement, lambda h, s: s[1] 
    non_create_statement %= control_structure, lambda h, s: s[1]
    
    non_create_statement %= expression #AÑADI ESTO PARA QUE RECONOZCA id @ id
    non_create_statement %= let_in, lambda h, s: s[1] #PARCHE

    #Acreate_statement %= type_definition, lambda h, s: s[1]
    #Acreate_statement %= function_definition, lambda h, s: s[1]
    #Acreate_statement %= assignment, lambda h, s: s[1]
    
    print_statement %= Print + oPar + non_create_statement + cPar, lambda h, s: PrintStatmentNode(s[3]) #QUITE SEMI
    
    kern_assignment %= identifier + Equal + expression, lambda h, s: KernAssigmentNode(s[1],s[3])
    # kern_assignment %= identifier + Equal + string, lambda h, s: KernAssigmentNode(s[1],s[3]) #PARCHE

    
    multi_assignment %= kern_assignment + Comma + multi_assignment, lambda h, s: [s[1]] + s[3]
    #multi_assignment %= kern_assignment + Semi, lambda h, s: [s[1]]
    multi_assignment %= kern_assignment, lambda h, s: [s[1]] #PARCHE
    
    assignment %= Let + multi_assignment, lambda h, s: s[2]
    assignment %= instance_creation, lambda h, s: s[1]
    
    #Atype_annotation %= Colon + def_Type, lambda h, s: TypeNode(s[2]) 
    #Atype_annotation %= G.Epsilon, lambda h, s: TypeNode('object')
    
    #Afunction_definition %= Function + identifier + type_annotation + oPar + parameters + cPar + oBrace + statement_list + cBrace, lambda h, s: FunctionDefinitionNode(s[2],s[3],s[5],s[8]) 
    #Afunction_definition %= Function + identifier + type_annotation + oPar + parameters + cPar + Arrow + non_create_statement + Semi,lambda h, s: FunctionDefinitionNode(s[2],s[3],s[5],s[8])
    
    ##--------------------------Redefinir luego-----------------------------------------------
    #Aparameters %= expression + type_annotation + Comma + parameters, lambda h, s: [s[1]] + s[4]
    #Aparameters %= expression + type_annotation, lambda h, s: [s[1]]
    #Aparameters %= G.Epsilon, lambda h, s:[]
    #A
    #Acontrol_structure %= if_structure , lambda h, s: s[1]
    #Acontrol_structure %= while_structure , lambda h, s: s[1]
    #Acontrol_structure %= for_structure , lambda h, s: s[1]
    #A
    #Aif_structure %= If + oPar + condition + cPar + oBrace + statement_list + cBrace + contElif + contElse , lambda h, s: IfStructureNode(s[3], s[6], s[8], s[9])
    #A
    #AcontElif %= Elif + oPar + condition + cPar + oBrace + statement_list + cBrace + contElif , lambda h, s: [ElifStructureNode(s[3],s[6])] + s[8]
    #AcontElif %= G.Epsilon , lambda h, s: []
    #A
    #AcontElse %= Else + oBrace + statement_list + cBrace , lambda h, s: ElseStructureNode(s[3])
    #AcontElse %= G.Epsilon , lambda h, s:  ElseStructureNode([])
    #A
    #Awhile_structure %= While + oPar + condition + cPar + oBrace + statement_list + cBrace , lambda h, s:  WhileStructureNode(s[3], s[6])
    #Afor_structure %= For + oPar + assignment + Semi + condition + Semi + assignment + cPar + oBrace + statement_list + cBrace , lambda h, s:  ForStructureNode(s[3], s[5], s[7], s[10])
    #A
    expression_0, expression_1, expression_2, expression_3, expression_4 = G.NonTerminals('expression_0 expression_1 expression_2 expression_3 expression_4')
    
    #AconcatStrings %= expression + arroba + expression, lambda h, s:  StringConcatNode(s[1],s[4])
    #AconcatStringsWithSpace %= expression + arroba + arroba + expression, lambda h, s:  StringConcatWithSpaceNode(s[1],s[4])
    #A
    expression %= expression_0 + arroba + expression_0, lambda h, s:  StringConcatNode(s[1],s[4])
    expression %= expression_0 + arroba + arroba + expression_0, lambda h, s:  StringConcatWithSpaceNode(s[1],s[4])
    expression %= expression_0 #AÑADI

    expression_0 %= expression_1 + Is + def_Type, lambda h, s:  BoolIsTypeNode(s[1],s[3])
    expression_0 %= expression_1, lambda h, s:  s[1]

    expression_1 %= expression_2 + And + expression_2, lambda h, s:  BoolAndNode(s[1],s[3])
    expression_1 %= expression_2 + Or + expression_2, lambda h, s:  BoolOrNode(s[1],s[3])
    expression_1 %= expression_2, lambda h, s: s[1]

    expression_2 %= expression_3 + Less + expression_3, lambda h, s:  BoolCompLessNode(s[1],s[3])
    expression_2 %= expression_3 + Greater + expression_3, lambda h, s:  BoolCompGreaterNode(s[1],s[3])
    expression_2 %= expression_3 + CompEqual + expression_3, lambda h, s:  BoolCompEqualNode(s[1],s[3])
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
    #Afactor %= function_call, lambda h, s:  s[1]
    #Afactor %= member_access, lambda h, s:  s[1]
    #Afactor %= math_call, lambda h, s:  s[1]
    factor %= identifier, lambda h, s:  IdentifierNode(s[1])
    #Afactor %= _False, lambda h, s:  BooleanNode(s[1])
    #Afactor %= _True, lambda h, s:  BooleanNode(s[1])
    #Afactor %= kern_instance_creation, lambda h, s: s[1]
    #A
    #Akern_instance_creation %= New + def_Type + oPar + arguments + cPar, lambda h, s: KernInstanceCreationNode(s[2],s[4])
    #A
    #Afunction_call %= identifier + oPar + arguments + cPar, lambda h, s:  s[1]
    #Amath_call %= sqrt + oPar + expression_4 + cPar, lambda h, s: SqrtMathNode(s[3])
    #Amath_call %= cos + oPar + expression_4 + cPar, lambda h, s: CosMathNode(s[3])
    #Amath_call %= sin + oPar + expression_4 + cPar, lambda h, s: SinMathNode(s[3])
    #Amath_call %= tan + oPar + expression_4 + cPar, lambda h, s: TanMathNode(s[3])
    #Amath_call %= exp + oPar + expression_4 + cPar, lambda h, s: ExpMathNode(s[3])
    #Amath_call %= log + oPar + expression_4 + Comma + expression_4 + cPar, lambda h, s:  LogCallNode(s[3],s[5]) 
    #Amath_call %= rand + oPar + cPar,  lambda h, s: RandomCallNode()
    #A
    #Aarguments %= expression + Comma + arguments, lambda h, s: [s[1]]+s[2]
    #Aarguments %= expression , lambda h, s: s[1]
    #Aarguments %= G.Epsilon, lambda h, s: []
    #A
    #let in
    let_in %= assignment + In + non_create_statement, lambda h, s: LetInNode(s[1], s[3])
    let_in %= assignment + In + oBrace + statement_list + cBrace, lambda h, s: LetInNode(s[1], s[3]) #NO TENGO CLARO CUANDO SE USA () Y CUANDO {}
    
    # Estructuras adicionales para tipos
    #Atype_definition %= Type + identifier + inheritance + oBrace + attribute_definition + method_definition + cBrace, lambda h, s: TypeDefinitionNode(s[2],s[3], s[5], s[6])
    #A
    #Aattribute_definition %= attribute_definition + kern_assignment + Semi, lambda h, s: s[1] + [s[2]]
    #Aattribute_definition %= G.Epsilon, lambda h, s: []
    #A
    #Amethod_definition %= identifier + oPar + parameters + cPar + oBrace + statement_list + cBrace + method_definition, lambda h, s: [MethodDefinitionNode(s[1], s[3], s[6])] + s[8]
    #Amethod_definition %= G.Epsilon , lambda h, s: []
    #A
    #Ainheritance %= Inherits + def_Type, lambda h, s: InheritanceNode(s[2])
    #Ainheritance %= G.Epsilon, lambda h, s: InheritanceNode("object")
    #A# Instanciación de tipos
    #Ainstance_creation %= Let + identifier + Equal + New + def_Type + oPar + arguments + cPar + Semi, lambda h, s: InstanceCreationNode(s[2],s[5], s[7])
    #A#method_override %= identifier + oPar + parameters + cPar + oBrace + statement_list + cBrace | G.Epsilon
    #A
    #Acont_member %= oPar + arguments + cPar, lambda h, s: s[2]
    #Acont_member %= G.Epsilon, lambda h, s: []
    #Amember_access %= factor + Dot + identifier + cont_member , lambda h, s: MemberAccesNode(s[1], s[3], s[4]) 
    #A
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
    (identifier, f'({minletters})({minletters}|{zero_digits})*')
], G.EOF)
    
    return G, lexer
