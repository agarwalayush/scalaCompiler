#!/usr/bin/env python
import ply.lex as lex
import sys
from collections import defaultdict
#reserved = {'abstract', 'case', 'catch', 'class', 'def', 'do', 'else', 'extends', 'false', 'final', 'finally', 'for', 'forSome', 'if', 'implicit', 'import', 'lazy', 'match', 'new', 'null', 'object', 'override', 'package', 'private', 'protected', 'return', 'sealed', 'super', 'this', 'throw', 'trait', 'try', 'true', 'type', 'val', 'var', 'while', 'with', 'yield' }

reserved = {'abstract' : 'K_ABSTRACT',
        'case' : 'K_CASE',
        'catch' : 'K_CATCH',
        'class' : 'K_CLASS',
        'def' : 'K_DEF',
        'do' : 'K_DO',
        'else' : 'K_ELSE',
        'extends' : 'K_EXTENDS',
        'false' : 'K_FALSE',
        'final' : 'K_FINAL',
        'finally' : 'K_FINALLY',
        'for' : 'K_FOR',
        'forSome' : 'K_FORSOME',
        'if' : 'K_IF',
        'implicit' : 'K_IMPLICIT',
        'import' : 'K_IMPORT',
        'lazy' : 'K_LAZY',
        'match' : 'K_MATCH',
        'new' : 'K_NEW',
        'null' : 'K_NULL',
        'object' : 'K_OBJECT',
        'override' : 'K_OVERRIDE',
        'package' : 'K_PACKAGE',
        'private' : 'K_PRIVATE',
        'protected' : 'K_PROTECTED',
        'return' : 'K_RETURN',
        'sealed' : 'K_SEALED',
        'super' : 'K_SUPER',
        'this' : 'K_THIS',
        'throw' : 'K_THROW',
        'trait' : 'K_TRAIT',
        'try' : 'K_TRY',
        'true' : 'K_TRUE',
        'type' : 'K_TYPE',
        'val' : 'K_VAL',
        'var' : 'K_VAR',
        'while' : 'K_WHILE',
        'with' : 'K_WITH',
        'yield' : 'K_YIELD',
	'until' : 'K_UNTIL',
	'to' : 'K_TO',
        'Byte' : 'K_BYTE',
	    'Short' : 'K_SHORT',
	    'Int' : 'K_INT',
	    'Long' : 'K_LONG',
	    'Float' : 'K_FLOAT',
	    'Double' : 'K_DOUBLE',
	    'Char' : 'K_CHAR',
	    'String' : 'K_STRING',
	    'Boolean' : 'K_BOOLEAN',
	    'Unit' : 'K_UNIT',
	    'Nothing' : 'K_NOTHING',
	    'Any' : 'K_ANY',
	    'AnyRef' : 'K_ANYREF',
	    'Option' : 'K_OPTION',
	    'Iterator' : 'K_ITERATOR',
	    'Some' : 'K_SOME',
	    'None' : 'K_NONE',
	    'Array' : 'K_ARRAY'	}

# List of token names.   This is always required

tokens = list(reserved.values()) + [
    'INT',
    'LONG',
    'FLOAT',
    'CHAR',
    'STRING',
    'ARITH_OP',
    'REL_OP',
    'LOGIC_OP',
    'BIT_OP',
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
    'PERIOD',
    'DOT',
    'AND',
    'OR',
    'GREATER_THAN',
    'NOT',
    'LESS_THAN',
    'GREATER_THAN_EQUAL',
    'LESS_THAN_EQUAL',
    'EQUAL',
    'NEQUAL',
    'MINUS',
    'MOD',
    'DIVIDE',
    'COLON',
    'MULT',
    'SEMI_COLON',
    'ASSIGN',
    'PLUS',
    'COMMA',
    'IN',
    'XOR',
    'AND_BITWISE',
    'LSHIFT',
    'RSHIFT',
    'FUNTYPE',
    'NEWLINE'
]
def t_NEWLINE(t):
    r'\n'
    t.lexer.lineno += len(t.value)


def t_FLOAT(t):
    r'((\d+)(\.\d+)([eE](\+|-)?(\d+))? | (\d+)[eE](\+|-)?(\d+))([lL]|[fF])?'
    t.value = float(t.value)
    return t

t_LSHIFT = r'>>'
t_RSHIFT = r'<<'
t_XOR = r'\^'
t_AND_BITWISE = r'&'
t_PLUS = r'\+'
t_MINUS = r'-'
t_MULT = r'\*'
t_DIVIDE = r'/'
t_MOD = r'%'
t_LOGIC_OP = r'&&|\|\|'
t_AND = r'&&'
t_OR = r'\|\|'
t_LESS_THAN = r'<'
t_GREATER_THAN = r'>'
t_LESS_THAN_EQUAL = r'<='
t_GREATER_THAN_EQUAL = r'>='
t_BIT_OP = r'\b(\||~)\b'
t_NOT = r'!'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_BLOCK_BEGIN  = r'\{'
t_SQUARE_BEGIN  = r'\['
t_BLOCK_END  = r'\}'
t_SQUARE_END  = r'\]'
t_SYMBOL  = r'(_|<:|<%|>:|\#|@|,)'
t_ASSIGN = r'='
t_EQUAL = r'=='
t_NEQUAL = r'!='
t_COLON = r':'
t_SEMI_COLON = r';'
t_COMMA = r','
t_DOT = r'\.'
t_IN = r'<-'
t_FUNTYPE = r'=>'



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
    t.type = reserved.get(t.value, 'IDENTIFIER')
    return t


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
