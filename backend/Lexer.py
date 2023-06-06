import ply.lex as lex

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
    'RBRACKET'
)

t_MULT = r'\*'
t_PLUS = r'\+'
t_DIV = r'\/'
t_MINUS = r'\-'
t_EQ = r'\='
t_DOEQ = r'\=\=\='
t_DOT = r'\.'
t_COMMA= r'\,'
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

