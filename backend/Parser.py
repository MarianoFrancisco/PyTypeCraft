import ply.yacc as yacc
from Lexer import tokens, lexer, errors, find_column
from src.Expression.array import Array
from src.Instruction.loop_while import While
from src.Instruction.variable_assignation import VariableAssignation
from src.Instruction.variable_declaration import VariableDeclaration
from src.Expression.unary_operation import ArithmeticUnaryOperation, BooleanUnaryOperation
from src.Instruction.if_declaration import IfSentence
from src.Instruction.call_function import CallFunction
from src.Instruction.function import Function
from src.Instruction.loo_for import For
from src.Instruction.reserved_return import ReservedReturn
from src.Instruction.console_log import ConsoleLog
from src.Semantic.symbol_table import SymbolTable
from src.Semantic.exception import CompilerException
from src.Expression.identifier import Identifier
from src.Native.native_typeof import TypeOf
from src.Native.native_tostring import ToString
from src.Native.native_tolowercase import ToLowerCase
from src.Native.native_touppercase import ToUpperCase
from src.Native.native_push import Push
from src.Instruction.concat import Concat
from src.Native.native_split import Split
from src.Native.native_tofixed import ToFixed
from src.Native.native_length import Length
from src.Native.native_toexponential import ToExponential
from src.Semantic.tree import Tree_
from src.Expression.primitive import Primitive
from src.Expression.binary_operation import ArithmeticOperation, BooleanOperation

precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'UNOT'),  # token ficticio
    ('left', 'TREQ', 'NOTDBEQ'),
    ('left', 'LT', 'GT', 'GTEQ', 'LTEQ'),
    ('left', 'PLUS', 'MINUS', 'COMMA'),
    ('left', 'MULT', 'DIV', 'MOD'),
    ('left', 'LPAREN', 'RPAREN'),
    ('left', 'POW'),
    ('right', 'UMINUS'),  # token ficticio
)

''' Start program '''

def p_program(p):
    'program : instructions'
    p[0] = p[1]

''' Instruction '''

# Many instructions

def p_instructions_list(p):
    'instructions : instructions instruction'
    if (p[2] != ""):#empty
        p[1].append(p[2])
    p[0] = p[1]

# One instruction

def p_instruction_only(p):
    'instructions : instruction'
    if p[1] == "":#empty
        p[0] = []
    else:
        p[0] = [p[1]]

# Options for instruction
# agregar de nuevo, revisar que da clavos
# | struct SEMI
# | new_struct SEMI
# | call_struct SEMI
def p_instruccion(p):
    '''instruction : print SEMI
                    | declaration SEMI
                    | assignment SEMI
                    | start_if SEMI
                    | function SEMI
                    | call_function SEMI
                    | while SEMI
                    | for SEMI
                    | return SEMI''' 
    p[0] = p[1]

def p_instruccion_out_semi(p):
    '''instruction : print
                    | declaration
                    | assignment
                    | start_if
                    | function
                    | call_function
                    | while
                    | for
                    | return''' 
    p[0] = p[1]

''' Type '''

#Type take value number, boolean, string & any
def p_type(p):
    '''type : NUMBER
            | BOOLEAN
            | STRING
            | ANY
            '''
    p[0]=p[1]

''' Concat '''

def p_concat(p):
    'concat : CONCAT LPAREN parameters_call RPAREN'
    p[0] = Concat(p[3],p.lineno(1), find_column(input, p.slice[1]))

''' Print'''

def p_print(p):
    'print : CONSOLE DOT LOG LPAREN parameters_call RPAREN'
    p[0] = ConsoleLog(p[5],p.lineno(1), find_column(input, p.slice[1]))


#definir local, definir global , funcion, struct, console, while, for
''' Assignment '''
def p_assignment(p):
    'assignment : ID EQ expression'
    p[0] = VariableAssignation(p[1], p[3], p.lineno(1), find_column(input, p.slice[1]))
# let a:String = "abc" let a:Number = [1,2,3]

''' Declaration'''
def p_declaration_assignment_type(p):
    'declaration : LET ID COLON type EQ expression'
    p[0] = VariableDeclaration(p[2], p[4], p[6], p.lineno(1), find_column(input, p.slice[1]))

def p_declaration_assignment_type_array(p):
    'declaration : LET ID COLON type LBRACKET RBRACKET EQ expression'
    p[0] = VariableDeclaration(p[2], p[4], p[8], p.lineno(1), find_column(input, p.slice[1]))

# def p_assignment_arrays(p):
#     'assignment : LET ID COLON type EQ LBRACE datas_array RBRACE'
#     p[0]

def p_declaration_assignment_notype(p):
    'declaration : LET ID EQ expression'
    p[0] = VariableDeclaration(p[2], 'any', p[4], p.lineno(1), find_column(input, p.slice[1]))


# let a:String let

def p_declaration_type(p):
    'declaration : LET ID COLON type'
    p[0] = VariableDeclaration(p[2], p[4], None, p.lineno(1), find_column(input, p.slice[1]))

# let a

def p_declaration_notype(p):
    'declaration : LET ID'
    p[0] = VariableDeclaration(p[2], 'any', None, p.lineno(1), find_column(input, p.slice[1]))

''' Function'''
#function a(){instructions}
def p_function(p):
    'function : FUNCTION ID LPAREN RPAREN LBRACE instructions RBRACE'
    p[0]= Function(p[2],[],p[6], p.lineno(1), find_column(input, p.slice[1]))
#function a(x){instructions}
def p_function_parameter(p):
    'function : FUNCTION ID LPAREN parameters RPAREN LBRACE instructions RBRACE'
    p[0]=Function(p[2], p[4], p[7], p.lineno(1), find_column(input, p.slice[1]))

''' Call function '''

# a(x)
def p_call_function_parameters(p):
    'call_function : ID LPAREN parameters_call RPAREN'
    p[0]= CallFunction(p[1], p[3], p.lineno(1), find_column(input, p.slice[1]))

# a()
def p_call_function(p):
    'call_function : ID LPAREN RPAREN'
    p[0]= CallFunction(p[1],[],p.lineno(1), find_column(input, p.slice[1]))

def p_call_concat(p):
    'call_function : concat'
    p[0]=p[1]

''' Parameters Function'''

# Many parameters id,id

def p_parameters_list(p):
    'parameters : parameters COMMA parameter'
    p[1].append(p[3])
    p[0]=p[1]

# One parameter id

def p_parameter_one(p):
    'parameters : parameter'
    p[0]=[p[1]]
# function name(id) 

# function name(id,id,id){} -x,x,x
def p_parameter_id(p):
    'parameter : ID'
    p[0] = {'type': 'any', 'id': p[1]}

# function name(id:String) - x: number[] 
def p_parameter_type(p):
    'parameter : ID COLON type'
    p[0] = {'type': p[3], 'id': p[1]}

''' Parameteres call function'''

def p_parameters_call_list(p):
    'parameters_call : parameters_call COMMA parameter_call'
    p[1].append(p[3])
    p[0] = p[1]

def p_parameters_call_one(p):
    'parameters_call : parameter_call'
    p[0] = [p[1]]

def p_parameter_call_data(p):
    'parameter_call : expression'
    p[0] = p[1]


''' Conditional if'''
# start if

def p_start_if(p):
    'start_if : IF if'
    p[0]=p[2]

# if (true){instructions}
def p_if(p):
    'if : LPAREN expression RPAREN LBRACE instructions RBRACE'
    p[0] = IfSentence(p[2], p[5], None, None, p.lineno(1), find_column(input, p.slice[1]))
# if (true){instructions} else{instructions}
def p_if_else(p):
    'if : LPAREN expression RPAREN LBRACE instructions RBRACE ELSE LBRACE instructions RBRACE'
    p[0] = IfSentence(p[2], p[5], p[9], None, p.lineno(1), find_column(input, p.slice[1]))
# if (true){instructions} else if (x){instructions}else if(x){instructions}
def p_if_else_if(p):
    'if : LPAREN expression RPAREN LBRACE instructions RBRACE ELSE IF if'
    p[0] = IfSentence(p[2], p[5], None, p[9], p.lineno(1), find_column(input, p.slice[1]))

''' Loop for '''

# for (let i=0;i<0;i++){instructions}
def p_for(p):
    'for : FOR LPAREN declaration SEMI expression SEMI expression RPAREN LBRACE instructions RBRACE'
    p[0] = For(p[3], p[5], p[7], p[10], p.lineno(1), find_column(input, p.slice[1]))
# for (let i of id){instructions}
def p_for_of(p):
    'for : FOR LPAREN declaration OF expression RPAREN LBRACE instructions RBRACE'
    p[0]

''' Loop while'''
# While(true){instructions}
def p_while(p):
    'while : WHILE LPAREN expression RPAREN LBRACE instructions RBRACE'
    p[0] = While(p[3], p[6], p.lineno(1), find_column(input, p.slice[1]))

# (3+2)*3
def p_expression_paren(p):
    'expression : LPAREN expression RPAREN'
    p[0]=p[2]

# Expressions, aritmetic, logics, relational, structure expr data expr, len = 3
def p_expression_operation(p):
    '''expression : expression MULT expression
                    | expression PLUS expression
                    | expression DIV expression
                    | expression MINUS expression
                    | expression EQ expression
                    | expression TREQ expression
                    | expression NOTDBEQ expression
                    | expression LT expression
                    | expression GT expression
                    | expression LTEQ expression
                    | expression GTEQ expression
                    | expression OR expression
                    | expression AND expression
                    | expression MOD expression
                    | expression POW expression
                    '''
    if p[2] in ['+', '-', '*', '/', '%', '^']:
        p[0] = ArithmeticOperation(p[1], p[3], p[2], p.lineno(2), find_column(input, p.slice[2]))
    else:
        p[0] = BooleanOperation(p[1], p[3], p[2], p.lineno(2), find_column(input, p.slice[2]))

''' unary --3=-(-3)'''
def p_expression_unaria(p):
    '''expression : MINUS expression %prec UMINUS
                | NOT expression %prec UNOT'''
    if p[1] == '-':
        p[0] = ArithmeticUnaryOperation(p[2], p[1], p.lineno(1), find_column(input, p.slice[1]))
    elif p[1] == '!':
        p[0] = BooleanUnaryOperation(p[2], p[1], p.lineno(1), find_column(input, p.slice[1]))

''' Array Expression'''

def p_expression_array(p):
    'expression : LBRACKET parameters_call RBRACKET'
    # CREAR EL ARRAY CON LOS DATOS QUE TRAE PARAMETER CALL
    p[0] = Array(p[2], p.lineno(1), find_column(input, p.slice[1]))

''' Primivite '''
# 1234
def p_expression_number(p):
    'expression : NUM_CONST'
    p[0] = Primitive(p[1], 'number', p.lineno(1), find_column(input, p.slice[1]))

# "asdf"
def p_expression_string(p):
    'expression : STR_CONST'
    p[0] = Primitive(p[1], 'string', p.lineno(1), find_column(input, p.slice[1]))    
# true
def p_expression_boolean_true(p):
    'expression : TRUE'
    p[0] = Primitive(True, 'boolean', p.lineno(1), find_column(input, p.slice[1]))

# false
def p_expression_boolean_false(p):
    'expression : FALSE'
    p[0] = Primitive(False, 'boolean', p.lineno(1), find_column(input, p.slice[1]))

# asdf1234
def p_expression_id(p):
    'expression : ID'
    p[0] = Identifier(p[1], p.lineno(1), find_column(input, p.slice[1]))


'''Increment and decrement'''
# i++, i--
def p_expression_dec_inc(p):
    '''expression : expression DBPLUS
                | expression DBMINUS
                '''
    print('reconociendo incremento, decremento')
    p[0] = ArithmeticUnaryOperation(p[1], p[2], p.lineno(2), find_column(input, p.slice[2]))



'''Call function with other function'''

def p_expresion_call_function(p):
    'expression : call_function'
    p[0] = p[1]

''' Return '''
def p_return(p):
    'return : RETURN expression'
    p[0] = ReservedReturn(p[2], p.lineno(1), find_column(input, p.slice[1]))

def add_natives(ast):
    instructions=[]
    #typeof
    name = "typeof"
    parameter=[{'type': 'any', 'id': 'typeof#parameter'}]
    typeof=TypeOf(name,parameter,instructions,-1,-1)
    ast.setFunctions(typeof)
    #toString
    name = "toString"
    parameter=[{'type': 'any', 'id': 'tostring#parameter'}]
    toString=ToString(name,parameter,instructions,-1,-1)
    ast.setFunctions(toString)
    #toLowerCase
    name = "toLowerCase"
    parameter=[{'type': 'string', 'id': 'tolowercase#parameter'}]
    toLowerCase=ToLowerCase(name,parameter,instructions,-1,-1)
    ast.setFunctions(toLowerCase)
    #toUpperCase
    name = "toUpperCase"
    parameter=[{'type': 'string', 'id': 'touppercase#parameter'}]
    toUpperCase=ToUpperCase(name,parameter,instructions,-1,-1)
    ast.setFunctions(toUpperCase)
    #push
    name = "push"
    parameters=[{'type': 'any', 'id': 'push#parameter'},{'type':'NoType', 'id':'push#parameter2'}]
    push=Push(name,parameters,instructions,-1,-1)
    ast.setFunctions(push)
    #split
    name = "split"
    parameters=[{'type': 'string', 'id': 'split#parameter'},{'type':'string', 'id':'split#parameter2'}]
    split=Split(name,parameters,instructions,-1,-1)
    ast.setFunctions(split)
    #toFixed
    name = "toFixed"
    parameters=[{'type': 'number', 'id': 'tofixed#parameter'},{'type':'number', 'id':'tofixed#parameter2'}]
    toFixed=ToFixed(name,parameters,instructions,-1,-1)
    ast.setFunctions(toFixed)
    #length
    name = "length"
    parameter=[{'type': 'string', 'id': 'length#parameter'}]
    length=Length(name,parameter,instructions,-1,-1)
    ast.setFunctions(length)
    #toExponential
    name = "toExponential"
    parameters=[{'type': 'number', 'id': 'toexponential#parameter'},{'type':'number', 'id':'toexponential#parameter2'}]
    toExponential=ToExponential(name,parameters,instructions,-1,-1)
    ast.setFunctions(toExponential)


def p_error(t):
    print(" Error sintáctico en '%s'" % t.value, t)


input = ''

def parse(inp):
    global errors
    global parser
    errors = []
    parser = yacc.yacc()
    global input
    input = inp
    lexer.lineno = 1
    return parser.parse(inp)


entrada = '''
let a:number = 1.4231243123;
let b:string = "Mariano";
let c:number = 123.456;
let d:boolean = true;
let e:string = "MARIANO";
let f:string = "mariano";
let g:string = "abc,def,ghi,jkl";
let h:number[] = [1,2,3,4];
let i:number[] = [5,6,7,8];
console.log(toFixed(a,length(b)))
console.log(length(b))
console.log(toExponential(c,2))
console.log(typeof(toString(d)))
console.log(toLowerCase(e))
console.log(toUpperCase(f))
console.log(split(g,","))
console.log(h)
console.log(concat(h,i))
push(h,3)
console.log(h)
'''

def test_lexer(lexer):
    while True:
        tok = lexer.token()
        if not tok:
            break  # No more input
        print(tok)

lexer.input(entrada)
# test_lexer(lexer)


instrucciones = parse(entrada)
ast = Tree_(instrucciones)
globalScope = SymbolTable()
ast.setGlobalScope(globalScope)
add_natives(ast)

for instruccion in ast.getInstr():     
    if isinstance(instruccion, Function):
        ast.setFunctions(instruccion)

for instruccion in ast.getInstr():
    if not(isinstance(instruccion, Function)):
        value = instruccion.execute(ast,globalScope)
        if isinstance(value, CompilerException):
            ast.setExceptions(value)
    """ value = instruccion.execute(ast,globalScope)
    if isinstance(value, CompilerException):
        ast.setExceptions(value) """
print(ast.getConsole())
for err in ast.getExceptions():
    print(err)