import ply.yacc as yacc
from Lexer import tokens, lexer, errors, find_column

from src.Expression.arithmetic_operation import ArithmeticOperation
precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'UNOT'),  # token ficticio
    ('left', 'EQ', 'NOTDBEQ'),
    ('left', 'LT', 'GT', 'GTEQ', 'LTEQ'),
    ('left', 'PLUS', 'MINUS', 'COMA'),
    ('left', 'MULT', 'DIV', 'MOD'),
    ('left', 'LPAREN', 'RPAREN'),
    ('left', 'POW'),
    ('right', 'UMINUS'),  # token ficticio
)

''' Start program '''

def p_program(p):
    'program:instructions'
    p[0] = p[1]

''' Instruction '''

# Many instructions

def p_instructions_list(p):
    'instructions:instructions instruction'
    if (p[2] != ""):#empty
        p[1].append(p[2])
    p[0] = p[1]

# One instruction

def p_instruction_only(p):
    'instructions:instruction'
    if p[1] == "":#empty
        p[0] = []
    else:
        p[0] = [p[1]]

# Options for instruction

def p_instruccion(p):
    '''instruction : assignment SEMI
                    | declaration SEMI
                    | print SEMI
                    | function SEMI
                    | call_function SEMI
                    | start_if SEMI
                    | while SEMI
                    | for SEMI
                    | struct SEMI
                    | new_struct SEMI
                    | call_struct SEMI
                    | break SEMI
                    | continue SEMI
                    | return SEMI

                    ''' 
    p[0] = p[1]
''' Array '''
def p_array_position(p):
    '''array_position: ID LBRACE expression RBRACE EQ expression
                    | ID LBRACE expression RBRACE '''
    p[0]

''' Type '''

#Type take value number, boolean, string & any
def p_type(p):
    '''type : NUMBER
            | BOOLEAN
            | STRING
            | ANY
            | NUMBER LBRACE RBRACE
            | BOOLEAN LBRACE RBRACE
            | STRING LBRACE RBRACE
            | ANY LBRACE RBRACE
            '''
    p[0]=p[1]

#definir local, definir global , funcion, struct, console, while, for
''' Assignment '''
''' With type'''
# let a:String = "abc" let a:Number = [1,2,3]

def p_assignment_type(p):
    'assignment: LET ID COLON type EQ expression'
    p[0]

def p_assignment_arrays(p):
    'assignment: LET ID COLON type EQ LBRACE datas_array RBRACE'
    p[0]

# Many Datas array 3,3,id

def p_datas_array_list(p):
    'datas_array: datas_array COMMA data_array'
    p[1].append(p[3])
    p[0]=p[1]

# One data array

def p_datas_array_one(p):
    'datas_array: data_array'
    p[0]=p[1]
# Expression - 3
def p_data_array(p):
    'data_array: expression'
    p[0]=p[1]
''' No type'''
# let a="abc"

def p_assignment_notype(p):
    'assignment: LET ID EQ expression'
    p[0]
# let id = [3,id]
def p_assignment_arrays(p):
    'assignment: LET ID EQ LBRACE datas_array RBRACE'
    p[0]

''' Declaration'''

# let a:String let

def p_declaration_type(p):
    'declaration: LET ID COLON type'
    p[0]

# let a

def p_declaration_notype(p):
    'declaration: LET ID'
    p[0]

''' Print'''

def p_print(p):
    'print : CONSOLE DOT LOG LPAREN expression RPAREN'
    p[0] = p[5]

''' Function'''
#function a(){instructions}
def p_function(p):
    'function: FUNCTION ID LPAREN RPAREN LBRACE instructions RBRACE'
    p[0]
#function a(x){instructions}
def p_function_parameter(p):
    'function: FUNCTION ID LPAREN parameters RPAREN LBRACE instructions RBRACE'
    p[0]

''' Call function '''

# a(x)
def p_call_function(p):
    'call_function: ID LPAREN parameters RPAREN'
    p[0]

# a()
def p_call_function(p):
    'call_function: ID LPAREN RPAREN'
    p[0]

''' Parameters'''

# Many parameters id,id

def p_parameters_list(p):
    'parameters: parameters COMMA parameter'
    p[1].append(p[3])
    p[0]=p[1]

# One parameter id

def p_parameter_one(p):
    'parameters: parameter'
    p[0]=p[1]
# function name(id) 

# function name(id,id,id){} -x,x,x
def p_parameter_id(p):
    'parameter: ID'
    p[0]

# function name(id:String) - x: number[] 
def p_parameter_type(p):
    'parameter: ID COLON type'
    p[0]


''' Conditional if'''
# start if

def p_start_if(p):
    'start_if: IF if'
    p[0]=[2]

# if (true){instructions}
def p_if(p):
    'if: LPAREN expression RPAREN LBRACE instructions RBRACE'
    p[0]
# if (true){instructions} else{instructions}
def p_if_else(p):
    'if: LPAREN expression RPAREN LBRACE instructions RBRACE ELSE LBRACE instructions RBRACE'
    p[0]
# if (true){instructions} else if (x){instructions}else if(x){instructions}
def p_if_else_if(p):
    'if: LPAREN expression RPAREN LBRACE instructions RBRACE ELSE IF if'
    p[0]

''' Loop for '''

# for (let i=0;i<0;i++){instructions}
def p_for(p):
    'for: FOR LPAREN assignment SEMI expression SEMI expression RPAREN LBRACE instructions RBRACE'
    p[0]
# for (let i of id){instructions}
def p_for_of(p):
    'for: FOR LPAREN declaration OF expression RPAREN LBRACE instructions RBRACE'
    p[0]
''' Loop While '''

# While(true){instructions}
def p_while(p):
    'while: WHILE LPAREN expression RPAREN LBRACE instructions RBRACE'
    p[0]

''' unary --3=-(-3)'''
def p_expresion_unaria(t):
    '''expresion : MINUS expression %prec UMINUS
                | NOT expreSsion %prec UNOT'''
    if t[1] == '-':
        t[0] 
    elif t[1] == '!':
        t[0]

''' Primivite '''
# 1234
def p_expression_number(p):
    'expression: NUM_CONST'
    p[0]

# "asdf"
def p_expression_string(p):
    'expression: STR_CONST'
    p[0]
# true
def p_expression_boolean_true(p):
    'expression: TRUE'
    p[0]

# false
def p_expression_boolean_false(p):
    'expression: FALSE'
    p[0]

# asdf1234
def p_expression_id(p):
    'expression: ID'
    p[0]

'''Increment and decrement'''
# i++, i--
def p_expression_dec_inc(p):
    '''expression: ID DBPLUS
                | ID DBMINUS'''
    if(p[2] =='++'):
        p[0]
    elif(p[2]=='--'):
        p[0]

# (3+2)*3
def p_expression_paren(p):
    'expression: LPAREN expression RPAREN'
    p[0]=p[2]

# Expressions, aritmetic, logics, relational, structure expr data expr, len = 3
def p_expression_operation(p):
    '''expression : expression MULT expression
                    | expression PLUS expression
                    | expression DIV expression
                    | expression MINUS expression
                    | expression EQ expression
                    | expression TREQ expression
                    | expression LT expression
                    | expression GT expression
                    | expression LTEQ expression
                    | expression GTEQ expression
                    | expression OR expression
                    | expression AND expression
                    | expression MOD expression
                    | expression POW expression
                    '''
    if (p[2]=='*'):
        p[0] = ArithmeticOperation(p[1], p[3], '*', p.lineno(2), find_column(input, p.slice[2]))
    elif (p[2]=='+'):
        p[0]
    elif (p[2]=='/'):
        p[0]
    elif (p[2]=='-'):
        p[0]
    elif (p[2]=='='):
        p[0]
    elif (p[2]=='==='):
        p[0]
    elif (p[2]=='<'):
        p[0]
    elif (p[2]=='>'):
        p[0]
    elif (p[2]=='<='):
        p[0]
    elif (p[2]=='>='):
        p[0]
    elif (p[2]=='||'):
        p[0]
    elif (p[2]=='&&'):
        p[0]
    elif (p[2]=='%'):
        p[0]
    elif (p[2]=='^'):
        p[0]
''' Struct '''
# interface x{data}
def p_struct(p):
    'struct: INTERFACE ID LBRACE data_structs RBRACE'
    p[0]

# let x1:x={data new}
def p_struct(p):
    'new_struct: LET ID COLON ID EQ LBRACE data_new_structs RBRACE'
    p[0]
# a:number; e:string; loop struct

# Many data structs
# id:string; id:number;
def p_data_structs(p):
    'data_structs: data_structs data_struct'
    if (p[2] != ""):#empty
        p[1].append(p[2])
    p[0] = p[1]
# One data struct
def p_data_structs_only(p):
    'data_structs: data_struct'
    if p[1] == "":#empty
        p[0] = []
    else:
        p[0] = [p[1]]
# Data struct
# x:type;
def p_data_struct(p):
    'data_struct: ID COLON type SEMI'
    p[0]

# a:1234, e:"string" loop new struct
# Many data new structs placa:"as",color:"negro"
def p_data_new_structs(p):
    'data_new_structs: data_new_structs COMMA data_new_struct'
    if (p[3] != ""):#empty
        p[1].append(p[3])
    p[0] = p[1]

# One data new struct
def p_data_new_structs_only(p):
    'data_new_structs: data_new_struct'
    if p[1] == "":#empty
        p[0] = []
    else:
        p[0] = [p[1]]

# Data new struct
# x:
def p_data_new_struct(p):
    'data_new_struct: ID COLON expression'
    p[0]

''' Call struct'''
# x1.color
def p_call_struct(p):
    'call_struct: ID DOT ID'
    p[0]
# x1.color = "azul";
def p_change_struct(p):
    'call_struct: ID DOT ID EQ expression SEMI'
    p[0]

''' Break '''
def p_break(p):
    'break: BREAK'
    p[0]
''' Continue '''
def p_continue(p):
    'continue: CONTINUE'
    p[0]
''' Return '''
def p_return(p):
    'return: RETURN expression'
    p[0]