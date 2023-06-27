from graphviz import Graph
import uuid
import ply.yacc as yacc
from Lexer import tokens, lexer, errors, find_column
from src.Instruction.struct import Struct
from src.Expression.null import Null
from src.Expression.struct_expression import StructExpression
from src.Instruction.reserved_break import ReservedBreak
from src.Instruction.reserved_continue import ReservedContinue
from src.Expression.array import Array
from src.Instruction.loop_while import While
from src.Instruction.variable_assignation import VariableAssignation, VariableArrayAssignation, VariableStructAssignation
from src.Instruction.variable_declaration import VariableDeclaration
from src.Expression.unary_operation import ArithmeticUnaryOperation, BooleanUnaryOperation
from src.Instruction.if_declaration import IfSentence
from src.Instruction.call_function import CallFunction
from src.Instruction.function import Function
from src.Instruction.loo_for import For, ForOf
from src.Instruction.reserved_return import ReservedReturn
from src.Instruction.console_log import ConsoleLog
from src.Semantic.symbol_table import SymbolTable
from src.Semantic.exception import CompilerException
from src.Expression.identifier import Identifier, IdentifierArray, IdentifierStruct
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
                    | struct SEMI
                    | call_function SEMI
                    | while SEMI
                    | for SEMI
                    | continue SEMI
                    | break SEMI
                    | return SEMI''' 
    p[0] = p[1]

def p_instruccion_out_semi(p):
    '''instruction : print
                    | declaration
                    | assignment
                    | start_if
                    | function
                    | struct
                    | call_function
                    | while
                    | for
                    | continue
                    | break
                    | return''' 
    p[0] = p[1]

''' Type '''

#Type take value number, boolean, string & any
def p_type(p):
    '''type : NUMBER
            | BOOLEAN
            | STRING
            | ANY
            | ID
            '''
    p[0]=p[1]

def p_type_array(p):
    '''type : NUMBER dimensions_array
            | BOOLEAN dimensions_array
            | STRING dimensions_array
            | ANY dimensions_array
            | ID dimensions_array
            '''
    p[0] = p[1]+p[2]

# type_function
def p_type_function(p):
    '''type_function : type
                     | VOID'''
    p[0]=p[1]

''' array dimension'''
def p_dimensions_array(p):
    'dimensions_array : dimensions_array dimension_array'
    p[1] = p[1] + p[2]
    p[0] = p[1]

def p_dimensions_array_1(p):
    'dimensions_array : dimension_array'
    p[0] = p[1]

def p_dimension_array(p):
    'dimension_array : LBRACKET RBRACKET'
    p[0] = '[]'

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

def p_assignment_array(p):
    'assignment : ID indexes_array EQ expression'
    p[0] = VariableArrayAssignation(p[1], p[4], p[2], p.lineno(1), find_column(input, p.slice[1]))

def p_assignment_struct(p):
    'assignment : ID DOT struct_datas EQ expression'
    p[0] = VariableStructAssignation(p[1], p[3], p[5], p.lineno(1), find_column(input, p.slice[1]))


''' Declaration'''
def p_declaration_assignment_type(p):
    'declaration : LET ID COLON type EQ expression'
    p[0] = VariableDeclaration(p[2], p[4], p[6], p.lineno(1), find_column(input, p.slice[1]))

# def p_declaration_assignment_type_array(p):
#     'declaration : LET ID COLON type LBRACKET RBRACKET EQ expression'
#     p[0] = VariableDeclaration(p[2], f'Array<{p[4]}>', p[8], p.lineno(1), find_column(input, p.slice[1]))

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

''' Struct '''
# data_struct
def p_struct(p):
    'struct : INTERFACE ID LBRACE multidata_struct RBRACE'
    # implementar logica para reconocer
    p[0] = Struct(p[2], p[4], p.lineno(1), find_column(input, p.slice[1]))

def p_multidata_struct(p):
    '''multidata_struct : multidata_struct parameter SEMI
                        | multidata_struct parameter'''
    p[1].append(p[2])
    p[0] = p[1]
def p_multidata_struct_1(p):
    '''multidata_struct : parameter SEMI
                        | parameter'''
    p[0] = [p[1]]

''' Function'''
#function a(){instructions}
def p_function(p):
    'function : FUNCTION ID LPAREN RPAREN LBRACE instructions RBRACE'
    p[0]= Function(p[2],[],p[6], p.lineno(1), find_column(input, p.slice[1]))
#function a(x){instructions}
def p_function_parameter(p):
    'function : FUNCTION ID LPAREN parameters RPAREN LBRACE instructions RBRACE'
    p[0]=Function(p[2], p[4], p[7], p.lineno(1), find_column(input, p.slice[1]))

def p_function_type(p):
    'function : FUNCTION ID LPAREN RPAREN COLON type_function LBRACE instructions RBRACE'
    p[0]= Function(p[2],[],p[8], p.lineno(1), find_column(input, p.slice[1]), p[6])
#function a(x){instructions}
def p_function_parameter_type(p):
    'function : FUNCTION ID LPAREN parameters RPAREN COLON type_function LBRACE instructions RBRACE'
    p[0]=Function(p[2], p[4], p[9], p.lineno(1), find_column(input, p.slice[1]), p[7])
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
    p[0] = ForOf(p[3], p[5], p[8], p.lineno(1), find_column(input, p.slice[1]))

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

''' Struct Expression'''

def p_expression_struct(p):
    'expression : LBRACE struct_attributes RBRACE'
    # CREAR EL STRUCT CON LOS DATOS QUE TRAE STRUCT ATTRIBUTES
    p[0] = StructExpression(p[2], p.lineno(1), find_column(input, p.slice[1]))

''' Struct attributes'''
def p_struct_attributes(p):
    'struct_attributes : struct_attributes COMMA struct_attribute'
    p[1].append(p[3])
    p[0] = p[1]

def p_struct_attributes_1(p):
    'struct_attributes : struct_attribute'
    p[0] = [p[1]]

def p_struct_attribute(p):
    'struct_attribute : ID COLON expression'
    p[0] = {"id": p[1], "value": p[3]}

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

# NULL
def p_expression_null(p):
    'expression : NULL'
    p[0] = Null(p.lineno(1), find_column(input, p.slice[1]))

# asdf1234
def p_expression_id_array(p):
    'expression : ID indexes_array'
    p[0] = IdentifierArray(p[1], p[2], p.lineno(1), find_column(input, p.slice[1]))

def p_expression_id_struct(p):
    'expression : ID DOT struct_datas'
    # IMPLEMENTAR LOGICA PARA EXTRAER ATRIBUTOS DE UN STRUCT
    p[0] = IdentifierStruct(p[1], p[3], p.lineno(1), find_column(input, p.slice[1]))

''' array indexes'''
def p_indexes_array(p):
    'indexes_array : indexes_array index_array'
    p[1].append(p[2])
    p[0] = p[1]

def p_indexes_array_1(p):
    'indexes_array : index_array'
    p[0] = [p[1]]

def p_index_array(p):
    'index_array : LBRACKET expression RBRACKET'
    p[0] = p[2]

''' struct attributes '''

def p_struct_datas(p):
    'struct_datas : struct_datas DOT ID'
    p[1].append(p[3])
    p[0] = p[1]

def p_struct_datas_1(p):
    'struct_datas : ID'
    p[0] = [p[1]]

'''Increment and decrement'''
# i++, i--
def p_expression_dec_inc(p):
    '''expression : expression DBPLUS
                | expression DBMINUS
                '''
    p[0] = ArithmeticUnaryOperation(p[1], p[2], p.lineno(2), find_column(input, p.slice[2]))



'''Call function with other function'''

def p_expresion_call_function(p):
    'expression : call_function'
    p[0] = p[1]

''' Return '''
def p_return(p):
    'return : RETURN expression'
    p[0] = ReservedReturn(p[2], p.lineno(1), find_column(input, p.slice[1]))

''' Continue '''
def p_continue(p):
    'continue : CONTINUE'
    p[0] = ReservedContinue(p.lineno(1), find_column(input, p.slice[1]))

''' Break '''
def p_break(p):
    'break : BREAK'
    p[0] = ReservedBreak(p.lineno(1), find_column(input, p.slice[1]))

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
    parameter=[{'type': 'any', 'id': 'length#parameter'}]
    length=Length(name,parameter,instructions,-1,-1)
    ast.setFunctions(length)
    #toExponential
    name = "toExponential"
    parameters=[{'type': 'number', 'id': 'toexponential#parameter'},{'type':'number', 'id':'toexponential#parameter2'}]
    toExponential=ToExponential(name,parameters,instructions,-1,-1)
    ast.setFunctions(toExponential)

def add_structs(ast):
    data = []
    string = Struct('string', data, -1, -1)
    ast.addInterface(string)
    number = Struct('number', data, -1, -1)
    ast.addInterface(number)
    boolean = Struct('boolean', data, -1, -1)
    ast.addInterface(boolean)
    any = Struct('any', data, -1, -1)
    ast.addInterface(any)

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
console.log("");
console.log("=======================================================================");
console.log("=============================TRANSFERENCIA=============================");
console.log("=======================================================================");

let a:number = -1;
while (a < 5){
    a = a + 1;
    if (a === 3){
        console.log("a");
        continue;
    } else if (a === 4){
        console.log("b");
        break;
    };
    console.log("El valor de a es: ", a, ", ");
};
'''

def test_lexer(lexer):
    while True:
        tok = lexer.token()
        if not tok:
            break  # No more input
        print(tok)

lexer.input(entrada)
# test_lexer(lexer)

# dot = Graph(filename='./static/process.gv')
# dot.attr(splines='false')
# dot.node_attr.update(shape='circle', fontname='arial',
#                      color='blue4', fontcolor='blue4')
# dot.edge_attr.update(color='blue4') 



# instrucciones = parse(entrada)
# ast = Tree_(instrucciones)
# globalScope = SymbolTable()
# ast.setGlobalScope(globalScope)
# add_natives(ast)
# add_structs(ast)

# for instruccion in ast.getInstr():
#     if isinstance(instruccion, Struct):
#         ast.addInterface(instruccion)
#     if isinstance(instruccion, Function):
#         ast.setFunctions(instruccion)

# for instruccion in ast.getInstr():
#     if not(isinstance(instruccion, Function)):
#         value = instruccion.execute(ast,globalScope)
#         if isinstance(value, CompilerException):
#             ast.setExceptions(value)
#     """ value = instruccion.execute(ast,globalScope)
#     if isinstance(value, CompilerException):
#         ast.setExceptions(value) """
# print(ast.getConsole())
# for err in ast.getExceptions():
#     print(err)




# def plot_instructions(instructions, root):
#     instructions_id = str(uuid.uuid4())
#     root.node(instructions_id, "instrucciones")
#     prevId = instructions_id

#     for instruction in instructions:
#         instruction_id = instruction.plot(root)
#         root.edge(prevId, instruction_id)
#         prevId = instruction_id

#     return instructions_id

# finalid = plot_instructions(ast.getInstr(), dot)

# dot.node('start', 'program')
# dot.edge('start', finalid)

# # dot.render()