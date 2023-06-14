import ply.yacc as yacc
from Lexer import tokens, lexer, errors, find_column
from src.Instruction.console_log import ConsoleLog
from src.Semantic.symbol_table import SymbolTable_
from src.Semantic.exception import CompilerException
from src.Expression.identifier import Identifier
from src.Semantic.tree import Tree_
from src.Expression.primitive import Primitive
from src.Expression.binary_operation import ArithmeticOperation

precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'UNOT'),  # token ficticio
    ('left', 'EQ', 'NOTDBEQ'),
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
                    | start_if SEMI''' 
    p[0] = p[1]

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
    'assignment : LET ID COLON type EQ expression'
    p[0]

# def p_assignment_arrays(p):
#     'assignment : LET ID COLON type EQ LBRACE datas_array RBRACE'
#     p[0]

def p_assignment_notype(p):
    'assignment : LET ID EQ expression'
    p[0]

''' Declaration'''

# let a:String let

def p_declaration_type(p):
    'declaration : LET ID COLON type'
    p[0]

# let a

def p_declaration_notype(p):
    'declaration : LET ID'
    p[0]

''' Print'''

def p_print(p):
    'print : CONSOLE DOT LOG LPAREN expression RPAREN'
    p[0] = ConsoleLog(p[5],p.lineno(1), find_column(input, p.slice[1]))

''' Conditional if'''
# start if

def p_start_if(p):
    'start_if : IF if'
    p[0]=[2]

# if (true){instructions}
def p_if(p):
    'if : LPAREN expression RPAREN LBRACE instructions RBRACE'
    p[0]
# if (true){instructions} else{instructions}
def p_if_else(p):
    'if : LPAREN expression RPAREN LBRACE instructions RBRACE ELSE LBRACE instructions RBRACE'
    p[0]
# if (true){instructions} else if (x){instructions}else if(x){instructions}
def p_if_else_if(p):
    'if : LPAREN expression RPAREN LBRACE instructions RBRACE ELSE IF if'
    p[0]

''' unary --3=-(-3)'''
def p_expresion_unaria(t):
    '''expresion : MINUS expression %prec UMINUS
                | NOT expression %prec UNOT'''
    if t[1] == '-':
        t[0] 
    elif t[1] == '!':
        t[0]

'''Increment and decrement'''
# i++, i--
def p_expression_dec_inc(p):
    '''expression : ID DBPLUS
                | ID DBMINUS'''
    if(p[2] =='++'):
        p[0]
    elif(p[2]=='--'):
        p[0]

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
                    | expression LT expression
                    | expression GT expression
                    | expression LTEQ expression
                    | expression GTEQ expression
                    | expression OR expression
                    | expression AND expression
                    | expression MOD expression
                    | expression POW expression
                    '''
    p[0] = ArithmeticOperation(p[1], p[3], p[2], p.lineno(2), find_column(input, p.slice[2]))

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

def p_error(t):
    print(" Error sintáctico en '%s'" % t.value)


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

console.log(5*4+2/5);
console.log(5*4);
console.log(5*4);
'''

instrucciones = parse(entrada)
ast = Tree_(instrucciones)
globalScope = SymbolTable_()
ast.setGlobalScope(globalScope)

# for instruccion in ast.getInstr():
#     if isinstance(instruccion, Funcion):
#         ast.setFunciones(instruccion)

for instruccion in ast.getInstr():
    print('hola')
    value = instruccion.execute(ast,globalScope)
    if isinstance(value, CompilerException):
        ast.setExceptions(value)
print(ast.getConsole())