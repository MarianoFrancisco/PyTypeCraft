import re
import ply.lex as lex

# Palabras reservadas
keywords = {
    'console.log': 'CONSOLE_LOG',
    'null': 'NULL',
    'number': 'NUMBER',
    'boolean': 'BOOLEAN',
    'string': 'STRING',
    'any': 'ANY',
    'interface': 'INTERFACE',
    'let': 'LET',
    'function': 'FUNCTION',
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'for': 'FOR',
    'of': 'OF',
    'break': 'BREAK',
    'continue': 'CONTINUE',
    'return': 'RETURN',
}

# Tokens
symbols = (
    'MULT',
    'PLUS',
    'DIV',
    'MINUS',
    'EQ',
    'TREQ',
    'DOT',
    'COMMA',
    'SEMI',
    'COLON',
    'LT',
    'GT',
    'LTEQ',
    'GTEQ',
    'LPAREN',
    'RPAREN',
    'LBRACE',
    'RBRACE',
    'OR',
    'AND',
    'NOT',
    'NOTDBEQ',
    'DBPLUS',
    'DBMINUS',
    'MOD',
    'POW',
    'LBRACKET',
    'RBRACKET',
    'NUM_CONST',
    'STR_CONST',
    'BOOL_CONST',
    'ID'
)

# Patron de tokens
t_MULT = r'\*'
t_PLUS = r'\+'
t_DIV = r'\/'
t_MINUS = r'\-'
t_EQ = r'\='
t_DOEQ = r'\=\=\='
t_DOT = r'\.'
t_COMMA = r'\,'
t_SEMI = r'\;'
t_COLON = r'\:'
t_LT = r'\<'
t_GT = r'\>'
t_LTEQ = r'\<\='
t_GTEQ = r'\>\='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_OR = r'\|\|'
t_AND = r'\&\&'
t_NOT = r'\!'
t_NOTDBEQ = r'\!\=\='
t_DBPLUS = r'\+\+'
t_DBMINUS = r'\-\-'
t_MOD = r'\%'
t_POW = r'\^'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'

# NUMBER


def t_NUM_CONST(t):
    r'\d+(\.\d+)?'
    try:
        if ("." in t.value):
            t.value = float(t.value)
        else:
            t.value = int(t.value)
    except ValueError:
        print("Number value too large %d", t.value)
        t.value = 0
    return t
# STRING "" '' ``


def t_STR_CONST(t):
    r"""(['"`])(.*?)\1"""
    t.value = t.value[1:-1]
    t.value = t.value.replace('\\"', '\"')
    t.value = t.value.replace("\\'", "\'")
    t.value = t.value.replace('\\\\', '\\')
    t.value = t.value.replace('\\t', '\t')
    t.value = t.value.replace('\\n', '\n')
    return t
# BOOLEAN


def t_BOOL_CONST(t):
    r'(true)|(false)'
    if ("true" in t.value):
        t.value = True
    else:
        t.value = False
    return t


# ID


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = keywords.get(t.value, 'ID')
    return t
# COMMENT


def t_COMMENT(t):
    r'\/\/.*(\n)?'
    if ("\n" in t.value):
        t.lexer.lineno += 1

# MULTCOMMENT


def t_MULTCOMMENT(t):
    r'\/\*(.|\n)*?\*\/'
    t.lexer.lineno += t.value.count('\n')


# WHIT_SPACE
t_WHIT_SPACE = ' \t\f\v'

# SKIPLINE


def t_SKIP_LINE(t):
    r'\n+'
    t.lexer.lineno += t.value.count('\n')

# ERROR


def t_ERROR(t):
    t.lexer.skip(1)
