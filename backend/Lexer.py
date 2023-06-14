import re
import ply.lex as lex

errors = []

# Palabras reservadas
keywords = {
    'console': 'CONSOLE',
    'log': 'LOG',
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
    'true': 'TRUE',
    'false': 'FALSE'
}

# Tokens
tokens = [
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
    'ID'
] + list(keywords.values())

# Patron de tokens
t_MULT = r'\*'
t_PLUS = r'\+'
t_DIV = r'\/'
t_MINUS = r'\-'
t_EQ = r'\='
t_TREQ = r'\=\=\='
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
    r'(\".*?\")|(\'.*?\')|(\`.*?\`)'
    t.value = t.value[1:-1]
    t.value = t.value.replace('\\"', '\"')
    t.value = t.value.replace("\\'", "\'")
    t.value = t.value.replace('\\\\', '\\')
    t.value = t.value.replace('\\t', '\t')
    t.value = t.value.replace('\\n', '\n')
    return t

# ID


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = keywords.get(t.value, 'ID')
    return t
# COMMENT


def t_comment(t):
    r'\/\/.*(\\n)?'
    if ("\n" in t.value):
        t.lexer.lineno += 1

# MULTCOMMENT


def t_multcomment(t):
    r'\/\*(.|\n)*?\*\/'
    t.lexer.lineno += t.value.count('\n')


# WHIT_SPACE
t_ignore = " \t\f\v"

# SKIPLINE


def t_skip_line(t):
    r'\n+'
    t.lexer.lineno += t.value.count('\n')

# ERROR


def t_error(t):
    t.lexer.skip(1)

def find_column(inp, tk):
    line_start = inp.rfind('\n', 0, tk.lexpos) + 1
    return (tk.lexpos - line_start) + 1

lexer = lex.lex(reflags=re.IGNORECASE)

""" # Crear instancia del lexer
lexer = lex.lex(reflags=re.IGNORECASE)

# Ingresar la cadena de texto para analizar
texto = "console.log('3')"

# Configurar la entrada del lexer
lexer.input(texto)

# Iterar sobre los tokens generados
while True:
    token = lexer.token()
    if not token:
        break
    print(token) """
