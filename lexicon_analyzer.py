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
#do: survive
#break: choke

#int: integrity [0 - 9]+
#float: breakdown [0 - 9]+ "." [0 - 9]+
#char: letter [a - z]+

#camus: true = suicide | false = coffee

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


from typing import NamedTuple, Union

class Token(NamedTuple):
    type: str
    value: Union[int, float, str]


#criar classe do Analisador Léxico
class LexiconAnalayzer(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]


    def token_generator(self):
        
        keywords = {'death', 'breath', 'life', 'choke', 'what', 'everwhat', 'ever', 'happy', 'tree', 'accident'}
        token_specification = [
                #('DEATH',    r'death'),       # function declaration
                #('BREATH',   r'breath'),      # for
                #('LIFE',     r'life'),        # while
                #('CHOKE',    r'choke'),       # break
                ('WHAT',     r'what'),        # if
                ('EVERWHAT', r'everwhat'),    # elif
                ('EVER',     r'ever'),        # else
                #('HAPPY',    r'happy'),       # switch
                #('TREE',     r'tree'),        # case
                #('ACCIDENT', r'accident'),    # default
                #('COMMA',    r','),
                #('OPEN_P',   r'\('),
                #('CLOSE_P',  r'\)'),
                ('OPEN_B',   r'{'),
                ('CLOSE_B',  r'}'),
                ('INTEGER',  r'\d+'),         # int number
                ('CAMUS',    r'coffee|suicide'), #true / false
                ('FLOAT',    r'\d+(\.\d*)?'), # float number
                ('STRING',   r'\"[a-z ,]+\"'),  # string always using double quotes
                ('CHAR',     r'\'[a-z]+\''),  # char always using sigle quotes
                ('ID',       r'[A-Za-z]+'),   # Identifiers
                ('PLUS',     r'\+'),          # plus op +
                ('MINUS',    r'-'),           # minus op -
                ('MULTI',    r'\*'),          # multiplication op *
                ('DIV',      r'/'),           # divising op /
                ('EQUALS',   r'=='),          # equals to
                ('DIFF',     r'!='),          # different then
                ('GTR_THAN', r'>='),
                ('LESS_THAN',r'<='),
                ('GREATER',  r'>'),
                ('LESS',     r'<'),
                ('ASSIGN',   r'='),           # Assignment operator
                ('ENDLINE',  r'\n'),          # endline
                #('COMMENT',  r''),           # comment
                ('SKIP',     r'[ \t]+'),      # skip char for spaces and tabs
                ('MISMATCH', r'\.'),          # Any other character
                
                # add greater and less then things
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
            yield Token(kind, value)

class AST(object):
    pass


class StatList(AST):
    def __init__(self, left, endline, right):
        self.left = left
        self.token = self.endline = endline
        self.right = right

class op_StatOp(AST):
    def __init__(self, left, space, right):
        self.left = left
        self.token = self.space = space
        self.right = right

class StatOp(AST):
    def __init__(self, left, exp, right):
        self.left = left
        self.token = self.exp = exp
        self.right = right

class CompOp(AST):
    def __init__(self, left, comp, right):
        self.left = left
        self.token = self.comp = comp
        self.right = right

class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right

class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

class Interpreter(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.token_generator = self.lexer.token_generator()
        self.current_token = next(self.token_generator)

    def error(self):
        raise Exception('Invalid syntax')

    def eat(self, token_type):

        if self.current_token.type == token_type:
            try:
                self.current_token = next(self.token_generator)
            except StopIteration:
                print("")
        else:
            self.error()

    def identifier(self):
        token = self.current_token
        self.eat(token.type)

        if token.type == 'ID':
            return Num(token)

    def factor(self):
        token = self.current_token
        
        if token.type == 'INTEGER':
            self.eat(token.type)
            token._replace(value = int(token.value)) 
            return Num(token)

        elif token.type == 'BREAKDOWN':
            self.eat(token.type)
            token.value = float(token.value)
            return Num(token)

        elif token.type == 'STRING':
            self.eat(token.type)
            token.value = str(token.value)
            return Num(token)

        elif token.type == 'CAMUS':
            self.eat(token.type)
            token.value = bool(token.value)
            return Num(token)

        elif token.type == 'ID':
            return self.identifier()

        else:
            return 'invalid'

    def term(self):
        node = self.factor()

        while self.current_token.type in ('MULTI', 'DIV'):
            token = self.current_token
            if token.type == 'MULTI':
                self.eat('MULTI')

            elif token.type == 'DIV':
                self.eat('DIV')             

            node = BinOp(left=node, op=token, right=self.factor())
        
        return node

    def simple_expression(self):

        node = self.term()

        while self.current_token.type in ('PLUS', 'MINUS'):
            token = self.current_token
            if token.type == 'PLUS':
                self.eat('PLUS')

            elif token.type == 'MINUS':
                self.eat('MINUS')

            node = BinOp(left=node, op=token, right=self.term())
        
        return node
    
    def expression(self):

        node = self.simple_expression()

        while self.current_token.type in ('EQUALS', 'DIFF', 'GREATER', 'LESS', 'GTR_THAN', 'LESS_THAN'):
            token = self.current_token
            if token.type == 'EQUALS':
                self.eat('EQUALS')
                # ISSO SIM SINTATICO SEM EXECUÇÃO
                #self.simple_expression()
            elif token.type == 'DIFF':
                self.eat('DIFF')
                #self.simple_expression()
            elif token.type == 'GREATER':
                self.eat('GREATER')
                #self.simple_expression()
            elif token.type == 'LESS':
                self.eat('LESS')
                #self.simple_expression()
            elif token.type == 'GTR_THAN':
                self.eat('GTR_THAN')
                #self.simple_expression()
            elif token.type == 'LESS_THAN':
                self.eat('LESS_THAN')
                #self.simple_expression()
            else:
                return 'invalid'

            node = CompOp(left=node, comp=token.type, right=self.simple_expression())
        
        return node

    def statement(self):
        #statement_result = ""

        while self.current_token.type in ('ID', 'WHAT', 'EVER', 'ENDLINE'):
            token = self.current_token

            if token.type == 'ID':
                node = self.identifier()

                token = self.current_token
                if token.type == 'ASSIGN':
                    self.eat('ASSIGN')
                    #expression_result = self.expression()

                    # if expression_result == 'invalid':
                    #     return 'invalid'

                    # if self.current_token.type == 'ID':
                    #     return 'invalid'

                else:
                    return 'invalid'

                node = StatOp(left=node, exp=token.type, right=self.expression())
                return node

            elif token.type == 'WHAT':
                self.eat('WHAT')
                what_token = 'WHAT'

                node = self.expression()

                # if self.current_token.type == 'ENDLINE':
                #     self.eat('ENDLINE')

                # elif self.current_token.type == 'OPEN_B':
                self.eat('OPEN_B')
                right_node = self.statement_list()

                if self.current_token.type == 'ENDLINE':
                    self.eat('ENDLINE')

                # elif statement == 'invalid':
                #     return 'invalid'

                self.eat('CLOSE_B')

                # else:
                #     return "invalid"

                node = StatOp(left=what_token, exp=node, right=right_node)
                return node

            elif self.current_token.type == 'EVER':
                self.eat('EVER')
                ever_token = 'EVER'

                node = self.expression()
                # if self.current_token.type == 'ENDLINE':
                #     self.eat('ENDLINE')

                self.eat('OPEN_B')

                right_node = self.statement_list()
                                
                self.eat('CLOSE_B')

                node = StatOp(left=ever_token, exp=node, right=right_node)
                return node

            elif token.type == 'ENDLINE':
                self.eat('ENDLINE')

            # elif statement_result == 'invalid':
            #     return 'invalid'

        return StatOp(left=None, exp=None, right=None)        

    def statement_list(self):
        node = self.statement()

        while self.current_token.type in ('ENDLINE'):
            token = self.current_token

            if token.type == 'ENDLINE':
                self.eat('ENDLINE')
                endline_token = 'ENDLINE'

                right_node = self.statement()
                return StatList(left=node, endline=endline_token, right=right_node)
                
        return None

    def parse(self):
        return self.statement_list()
    # nao sei exatamente como funciona retornar nada
    def optional_statements(self):
        
        statement_list_result = self.statement_list()
        if statement_list_result == 'invalid':
            return 'invalid'

        return 'valid'

    # def parameter_list(self):
    #     parameter_result = ""

    #     while self.current_token.type in ('ID'):
    #         if self.current_token.type == 'ID':
    #             self.identifier()
    #             if self.current_token.type == 'COMMA':
    #                 self.eat('COMMA')
    #                 parameter_result = self.parameter_list()

    #                 if parameter_result == 'invalid':
    #                     return 'invalid'
    #             else:
    #                 return 'valid'
        
    #         return 'valid'
    #     return 'invalid'

    # def arguments(self):
    #     arguments_result = ""

    #     while self.current_token.type in ('OPEN_P'):
    #         if self.current_token.type == 'OPEN_P':
    #             self.eat('OPEN_P')
    #             arguments_result = self.parameter_list()
                
    #             if arguments_result == 'invalid':
    #                 return 'invalid'

    #             elif self.current_token.type == 'CLOSE_P':
    #                 self.eat('CLOSE_P')
    #                 return 'valid'

    #             else:
    #                 return 'invalid'

class Interpreter_2(object):
    def __init__(self, parser):
        self.parser = parser

    def interpret(self):
        tree = self.parser.parse()
        return tree

def readfile():
    code_file = open('code_files\\test_ast.txt', 'r')
    code_string = code_file.read()

    print(code_string)
    return code_string

def main():
    #statement = input('calc -> ')
    statement = readfile()
    analyser = LexiconAnalayzer(statement)
    interpreter = Interpreter(analyser)
    result = Interpreter_2(interpreter).interpret()
    print(result)

if __name__ == '__main__':
    main()