#!/usr/bin/env python
import ply.lex as lex
import sys

reserved = {'abstract', 'case', 'catch', 'class', 'def', 'do', 'else', 'extends', 'false', 'final', 'finally', 'for', 'forSome', 'if', 'implicit', 'import', 'lazy', 'match', 'new', 'null', 'object', 'override', 'package', 'private', 'protected', 'return', 'sealed', 'super', 'this', 'throw', 'trait', 'try', 'true', 'type', 'val', 'var', 'while', 'with', 'yield' }

primitives = {'Byte','Short','Int','Long','Float','Double','Char','String','Boolean','Unit','Null','Nothing','Any','AnyRef'}

# List of token names.   This is always required
tokens = (
    'NUMBER',
    'STRING',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'LPAREN',
    'RPAREN',
    'BLOCK_BEGIN',
    'BLOCK_END',
    'SQUARE_BEGIN',
    'SQUARE_END',
    'IDENTIFIER',
    'PRIMITIVE',
    'RESERVED',
    'SYMBOL'
)

# Regular expression rules for simple tokens
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_BLOCK_BEGIN  = r'\{'
t_SQUARE_BEGIN  = r'\['
t_BLOCK_END  = r'\}'
t_SQUARE_END  = r'\]'
t_SYMBOL  = r'(_|:|=|=>|<-|<:|<%|>:|\#|@)'

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
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

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()

if __name__ == "__main__" :
    lex.runmain()
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)
