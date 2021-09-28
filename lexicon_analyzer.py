#MEMBROS:
#Guilherme Chagas / 22119013-5
#Luca Milla / 22119002-8
#Matheus Pelicer / 22119024-2
#Thiago Soares / 22.119.044-0

#S.A.D. = Sistema Automato Diferenciado/Depressivo

#Comment: (:
#Line Ender: :(

#def: death

#for: breath
#while: life
#break: choke

#int: integrity [0 - 9]+
#float: breakdown [0 - 9]+ "." [0 - 9]+
#char: letter [a - z]+

#String: "" || ''

#if: what
#elif: everwhat
#else: ever

#and: &&
#or: ||

#switch: happy
#case: tree
#default: accident

#Operações Aritméticas
#Soma: +
#Subtração: -
#Multiplicação: *
#Divisão: /

#Identificadores
#variáveis: ([a-z])+([a-z]|[0-9]|[_])*
#funções: ([a-z])+([a-z]|[0-9]|[_])*

#Alfabetos
#A: {a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z,0,1,2,3,4,5,6,7,8,9,_}

#============================================================================================================================================#
#********************************************************************************************************************************************#
#============================================================================================================================================#

#criar classe Symbol

import re

# class Symbol:
#     def __init__(self, name, type, scope):
#         self.name = name
#         self.type = type
#         self.scope = scope


from typing import NamedTuple

class Token(NamedTuple):
    type: str
    value: str
    line: int
    column: int

# class SymbolTable:
#     def __init__(self):
#         self.elements = {}
    
#     def insert(self, symbol):
#         self.elements[str(symbol.name)] = symbol

#     def lookup(self, name):
#         return self.elements[str(name)]

#criar classe do Analisador Léxico

class LexiconAnalayzer(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]


    def token_generator(self):
        
        keywords = {'death', 'breath', 'life', 'choke', 'what', 'everwhat', 'ever', 'happy', 'tree', 'accident'}
        token_specification = [
                ('DEATH',    r'death'),       # function declaration
                ('BREATH',   r'breath'),      # for
                ('LIFE',     r'life'),        # while
                ('CHOKE',    r'choke'),       # break
                ('WHAT',     r'what'),        # if
                ('EVERWHAT', r'everwhat'),    # elif
                ('EVER',     r'ever'),        # else
                ('HAPPY',    r'happy'),       # switch
                ('TREE',     r'tree'),        # case
                ('ACCIDENT', r'accident'),    # default
                ('INTEGER',   r'\d+'),        # int number
                ('FLOAT',    r'\d+(\.\d*)?'), # float number
                ('STRING',   r'\"[a-z]+\"'),  # string always using double quotes
                ('CHAR',     r'\'[a-z]+\''),  # char always using sigle quotes
                ('ID',       r'[A-Za-z]+'),   # Identifiers
                ('PLUS',     r'\+'),          # plus op +
                ('MINUS',    r'-'),           # minus op -
                ('MULTI',    r'\*'),          # multiplication op *
                ('DIV',      r'/'),           # divising op /
                ('ASSIGN',   r'='),           # Assignment operator
                ('ENDLINE',  r'\n'),          # endline
                #('COMMENT',  r''),           # comment
                ('SKIP',     r'[ \t]+'),      # skip char for spaces and tabs
                ('MISMATCH', r'\.'),          # Any other character
            ]

        tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
        token_regex = re.compile(tok_regex)
        line_num = 1
        line_start = 0

        iterable = re.finditer(token_regex, self.text) 

        for mo in iterable:
            kind = mo.lastgroup
            value = mo.group()
            column = mo.start() - line_start
            if kind == 'NUMBER':
                value = float(value) if '.' in value else int(value)
            elif kind == 'ID' and value in keywords:
                kind = value
            elif kind == 'NEWLINE':
                line_start = mo.end()
                line_num += 1
                continue
            elif kind == 'SKIP':
                continue
            elif kind == 'MISMATCH':
                raise RuntimeError(f'{value!r} unexpected on line {line_num}')
            yield Token(kind, value, line_num, column)



statement = """
    x = 10 + 2
"""

analyser = LexiconAnalayzer(statement)

for token in analyser.token_generator():
    print(token)