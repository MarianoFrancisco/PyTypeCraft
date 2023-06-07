import ply.yacc as yacc
from Lexer import tokens, lexer, errors

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

# Inicializador


def p_program(p):
    'program:instructions'
    p[0] = p[1]

# Una sola instruccion


def p_instruction_only(p):
    'instructions:instruction'
    if p[1] == "":
        p[0] = []
    else:
        p[0] = [p[1]]

# Varias instrucciones


def p_instructions_list(p):
    'instructions:instructions instruction'
    if (p[2] != ""):
        p[1].append(p[2])
    p[0] = p[1]


def p_instruccion(p):
    '''instruction : print SEMI''' 
    p[0] = p[1]


def p_print(p):
    'print : CONSOLE DOT LOG LPAREN expr RPAREN'
    p[0] = p[5]
