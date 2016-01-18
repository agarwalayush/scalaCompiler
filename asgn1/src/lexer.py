#!/usr/bin/env python
import ply.lex as lex
import sys
from collections import defaultdict
reserved = {'abstract', 'case', 'catch', 'class', 'def', 'do', 'else', 'extends', 'false', 'final', 'finally', 'for', 'forSome', 'if', 'implicit', 'import', 'lazy', 'match', 'new', 'null', 'object', 'override', 'package', 'private', 'protected', 'return', 'sealed', 'super', 'this', 'throw', 'trait', 'try', 'true', 'type', 'val', 'var', 'while', 'with', 'yield' }

primitives = {'Byte','Short','Int','Long','Float','Double','Char','String','Boolean','Unit','Null','Nothing','Any','AnyRef'}

# List of token names.   This is always required
tokens = (
    'INT',
    'LONG',
    'FLOAT',
    'CHAR',
    'STRING',
    'ARITH_OP',
    'REL_OP',
    'BIT_OP',
    'LOGIC_OP',
    'UNARY_OP',
    'LPAREN',
    'RPAREN',
    'BLOCK_BEGIN',
    'BLOCK_END',
    'SQUARE_BEGIN',
    'SQUARE_END',
    'IDENTIFIER',
    'PRIMITIVE',
    'RESERVED',
    'SYMBOL',
    'PERIOD'
)

# Regular expression rules for simple tokens

def t_FLOAT(t):
    r'^[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?$'
    t.value = float(t.value)
    return t

t_ARITH_OP = r'(\+|-|\*|/|%)'
t_REL_OP = r'(<|>|<=|>=|!=|==)'
t_LOGIC_OP = r'(&&|\|\|)'
t_BIT_OP = r'(&|\||\^|~|<<|>>)'
t_UNARY_OP = r'(-|!)'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_BLOCK_BEGIN  = r'\{'
t_SQUARE_BEGIN  = r'\['
t_BLOCK_END  = r'\}'
t_SQUARE_END  = r'\]'
t_SYMBOL  = r'(_|:|=|=>|<-|<:|<%|>:|\#|@|,|\.)'


def t_INT(t):
    r'[-+]?\d+'
    t.value = int(t.value)
    return t

def t_LONG(t):
    r'[-+]?\d+(L|l)'
    t.value = int(t.value)
    return t

def t_CHAR(t):
    r'\'.\''
    t.value = t[1:-1]
    return t

def t_STRING(t):
    r'\"(\\.|[^\\"])*\"'
    t.value = t.value[1:-1]
    return t

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = 'RESERVED' if t.value in reserved else 'PRIMITIVE' if t.value in primitives else 'IDENTIFIER'
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore  = ' \t'

def t_ccode_comment(t):
    r'(/\*(.|\n)*?\*/)|(//.*)'
    pass

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()

if __name__ == "__main__" :
    filep = open(sys.argv[1])
    data = filep.read()
    lexer.input(data)
    tk = defaultdict(list)
    num_tk = {}
    while True:
        tok = lexer.token()
        if not tok:
            break
        if(tok.type not in tk):
            num_tk[tok.type] = 0
        if(tok.value not in tk[tok.type]):
            tk[tok.type].append(tok.value)
        num_tk[tok.type] += 1
    print ("Token         ", "Occurences", "      Lexemes    ")
    for x in tk.keys():
        print ('{:16s} {:3d}            {}'.format(x, num_tk[x], tk[x]))
