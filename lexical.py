"""
!!! **DON't** change any comment in this file !!!

"""

import ply.lex as lex

reserved = {
    'class': 'class',
    'return': 'return',
    'static': 'static',

    # permission
    'private': 'private',
    'protected': 'protected',
    'public': 'public',

    # types
    'boolean': 'boolean',
    'char': 'char',
    'int': 'int',
    'String': 'string',
    'void': 'void',

    # control
    'break': 'break',
    'continue': 'continue',
    'else': 'else',
    'for': 'for',
    'if': 'if',
    'while': 'while',

    # other
    'true': 'true',
    'false': 'false',
    'null': 'null',
}

tokens = (
             # operator
             'add',
             'sub',
             'mul',
             'div',
             'and',
             'or',
             'assign',

             # relation
             'equal',
             'neq',
             'less',
             'greater',
             'leq',
             'geq',

             # punctuation
             'semi',
             'comma',
             'dot',
             'lp',
             'rp',
             'lb',
             'rb',
             'lc',
             'rc',

             'id',
             'integer',
             'chr',
             'str',
         ) + tuple(reserved.values())

t_add = r'\+'
t_sub = r'-'
t_mul = r'\*'
t_div = r'/'
t_and = r'&&'
t_or = r'\|\|'
t_assign = r'='

t_equal = r'=='
t_neq = r'!='
t_less = r'<'
t_greater = r'>'
t_leq = r'<='
t_geq = r'>='

t_semi = r';'
t_comma = r','
t_dot = r'\.'
t_lp = r'\('
t_rp = r'\)'
t_lb = r'\['
t_rb = r'\]'
t_lc = r'\{'
t_rc = r'\}'


def t_id(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'id')
    return t


def t_integer(t):
    r'[1-9][0-9]*|0'
    t.value = int(t.value)
    return t


t_chr = r'\'.\''
t_str = r'".*"'


def t_newLine(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


t_ignore = ' \t'


def t_error(t):
    print('Illegal character {}'.format(t.value[0]))
    t.lexer.skip(1)


lexer = lex.lex(debug=True)
