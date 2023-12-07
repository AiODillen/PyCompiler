from rply import ParserGenerator
from ast1 import *


class Parser:
    def __init__(self, module, builder, printf):
        self.pg = ParserGenerator(
            # A list of all token names accepted by the parser.
            ['NUMBER', 'PRINT', 'OPEN_PAREN', 'CLOSE_PAREN',
             'SEMI_COLON', 'ADD', 'SUB', 'MUL', 'DIV','STRING'],
            precedence=[
                ('left', ['ADD', 'SUB']),
                ('left', ['MUL', 'DIV'])
            ]
        )
        self.module = module
        self.builder = builder
        self.printf = printf

    def parse(self):


        @self.pg.production('expression : PRINT OPEN_PAREN expression CLOSE_PAREN SEMI_COLON')
        def expression_print(p):
            return Print(self.builder, self.module, self.printf, p[2])

        @self.pg.production('expression : STRING')
        def expression_string(p):
            return String(self.builder, self.module, p[0].value)

        @self.pg.production('expression : number ADD number')
        @self.pg.production('expression : number ADD expression')
        @self.pg.production('expression : number SUB number')
        @self.pg.production('expression : number SUB expression')
        @self.pg.production('expression : number MUL number')
        @self.pg.production('expression : number MUL expression')
        @self.pg.production('expression : number DIV number')
        @self.pg.production('expression : number DIV expression')
        def expression_binop(p):
            left = p[0]
            right = p[2]
            if p[1].gettokentype() == 'ADD':
                return Add(self.builder, self.module, left, right)
            elif p[1].gettokentype() == 'SUB':
                return Sub(self.builder, self.module, left, right)
            elif p[1].gettokentype() == 'MUL':
                return Mul(self.builder, self.module, left, right)
            elif p[1].gettokentype() == 'DIV':
                return Div(self.builder, self.module, left, right)
            else:
                raise AssertionError('Oops, this should not be possible!')

        @self.pg.production('number : NUMBER')
        def number(p):
            return Number(self.builder, self.module, p[0].value)

        @self.pg.error
        def error_handle(token):
            raise ValueError(token)

    def get_parser(self):
        return self.pg.build()
