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
import pickle

# class Symbol:
#     def __init__(self, name, type, scope):
#         self.name = name
#         self.type = type
#         self.scope = scope


from typing import NamedTuple, Union

class Token(NamedTuple):
    type: str
    value: Union[int, float, str, bool]


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
            token._replace(value = float(token.value)) 
            return Num(token)

        elif token.type == 'STRING':
            self.eat(token.type)
            token._replace(value = str(token.value)) 
            return Num(token)

        elif token.type == 'CAMUS':
            self.eat(token.type)
            token._replace(value = bool(token.value)) 
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

            node = CompOp(left=node, comp=token, right=self.simple_expression())
        
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

                node = StatOp(left=node, exp=token, right=self.expression())
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

                node = StatOp(left=what_token, exp=node, right=right_node)
                return node

            elif self.current_token.type == 'EVER':
                self.eat('EVER')
                ever_token = 'EVER'

                node = self.expression()
                # if self.current_token.type == 'ENDLINE':
                #     self.eat('ENDLINE')

                self.eat('OPEN_B')

                right_node = self.optional_statements()
                                
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
                
        return node

    def parse(self):
        return self.optional_statements()

    def optional_statements(self):
        
        left_node = self.statement_list()

        if not isinstance(left_node, StatOp) and not left_node.right.exp == None:    
            return op_StatOp(left=left_node, space='ENDLINE', right=self.optional_statements())
        else:
            return op_StatOp(left=left_node, space='ENDLINE', right=self.statement_list())



class NodeVisitor(object):
    python_code = ""

    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))

class Interpreter_2(NodeVisitor):
    def __init__(self, parser):
        self.parser = parser

    def visit_StatList(self, node):
        python_code = ""

        if node.endline == 'ENDLINE':
            left_exp = self.visit(node.left)
            right_exp = self.visit(node.right)
            python_code += str(left_exp) + str(right_exp)

        return python_code

    def visit_op_StatOp(self, node):
        python_code = ""
        left_exp = self.visit(node.left)
        python_code += str(left_exp)

        if node.right != None:
            right_exp = self.visit(node.right)
            python_code += str(right_exp)

        return python_code

    def visit_StatOp(self, node):
        left_var = node.left
        python_code = ""

        if left_var == 'WHAT':
            comparisson_text = self.visit(node.exp)

            statements_text = self.visit(node.right)
            split_statement = statements_text.split("\n")

            tabbed_text = ""
            for i in split_statement:
                if i:
                    tabbed_text += "\n\t" + i

            python_code += "if " + str(comparisson_text) + ":" + str(tabbed_text) + "\n"

        
        elif left_var == 'EVER':
            statements_text = self.visit(node.right)
            split_statement = statements_text.split("\n")

            tabbed_text = ""
            for i in split_statement:
                if i:
                    tabbed_text += "\n\t" + i

            python_code += "else" + ":" + str(tabbed_text) + "\n"

 
        elif node.exp == None:
            return python_code

        elif node.exp.type == 'ASSIGN':
            
            var = self.visit(node.left)
            var_value = self.visit(node.right)

            python_code += str(var) + "=" + str(var_value) + "\n"

        return python_code
            

    def visit_CompOp(self, node):
        python_code = ""

        if node.comp.type == 'EQUALS':
            python_code += str(self.visit(node.left)) + "==" + str(self.visit(node.right))
        elif node.comp.type == 'DIFF':
            python_code += str(self.visit(node.left)) + "!=" + str(self.visit(node.right))
        elif node.comp.type == 'GREATER':
            python_code += str(self.visit(node.left)) + ">" + str(self.visit(node.right))
        elif node.comp.type == 'LESS':
            python_code += str(self.visit(node.left)) + "<" + str(self.visit(node.right))
        elif node.comp.type == 'GTR_THAN':
            python_code += str(self.visit(node.left)) + ">=" + str(self.visit(node.right))
        elif node.comp.type == 'LESS_THAN':
            python_code += str(self.visit(node.left)) + "<=" + str(self.visit(node.right))

        return python_code

    def visit_BinOp(self, node):
        python_code = ""

        if node.op.type == 'PLUS':
            python_code += str(self.visit(node.left)) + "+" + str(self.visit(node.right))
        elif node.op.type == 'MINUS':
            python_code += str(self.visit(node.left)) + "-" + str(self.visit(node.right))
        elif node.op.type == 'MULTI':
            python_code += str(self.visit(node.left)) + "*" + str(self.visit(node.right))
        elif node.op.type == 'DIV':
            python_code += str(self.visit(node.left)) + "/" + str(self.visit(node.right))

        return python_code
        
    def visit_Num(self, node):
        if node.value == 'coffee':
            return str("False")
        elif node.value == 'suicide':
            return str("True")
        else:
            return node.value

    def interpret(self):
        tree = self.parser.parse()
        python_code = self.visit(tree)
        #print(python_code)
        return python_code


def readfile(filename):
    code_file = open('code_files\\' + filename +'.txt', 'r')
    code_string = code_file.read()

    #print(code_string)
    return code_string

def write_file(python_code, filename):
    with open('code_files\\' + filename + '.py', 'w') as code_file:
        code_file.write(python_code)

    code_file.close()

def main():
    input_file = input('filename (input) -> ')
    output_file = input('filename (output) -> ')
    statement = readfile(input_file)
    analyser = LexiconAnalayzer(statement)
    interpreter = Interpreter(analyser)
    result = Interpreter_2(interpreter).interpret()
    python_code = result.replace("None", "")
    #print(python_code)
    write_file(python_code, output_file)

if __name__ == '__main__':
    main()