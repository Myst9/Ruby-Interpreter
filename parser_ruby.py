from lexer import *

class AST(object):
    pass


class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right


class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value


class UnaryOp(AST):
    def __init__(self, op, expr):
        self.token = self.op = op
        self.expr = expr


class Compound(AST):
    def __init__(self):
        self.children = []


class Assign(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right

class Var(AST):
    """Var node is constructed from ID token"""
    def __init__(self,token):
        self.token=token
        self.value=token.value

class If(AST):
    def __init__(self, condition, body, rest):
        self.condition = condition
        self.body = body
        self.rest = rest

class Else(AST):
    def __init__(self, body):
        self.body=body


class While(AST):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class NoOp(AST):
    pass

class Parser(object):
    def __init__(self,lexer):
        self.lexer=lexer
        #set current token to the first token taken from the input
        self.current_token=self.lexer.get_next_token()

    def error(self):
        raise Exception('invalid syntax')
    
    def eat(self,token_type):
        """Compares the current token type with the passed token type"""
        #If these two match then eat the current token and set it to the next token
        #Else raise an exception
        if self.current_token.type==token_type:
            self.current_token=self.lexer.get_next_token()
        else:
            self.error()

    def program(self):
        """program : compound_statement"""
        node=self.compound_statement()
        return node

    def compound_statement(self):
        """compound_statement : statement_list"""
        nodes = self.statement_list()
        root=Compound()
        for node in nodes:
            root.children.append(node)
        return root

    def statement_list(self):
        """statement_list : statement | statement SEMI statement_list"""
        node = self.statement()
        results = [node]

        while self.current_token.type != EOF:
            results.append(self.statement())

        return results

    def statement(self):
        """
        statement : compound_statement | assignment_statement | if_statement | elsif_statement| else statement | while statement| empty
        
        """
        if self.current_token.type==ID:
            node=self.assignment_statement()
        elif self.current_token.type==IF:
            node=self.if_statement()
        elif self.current_token.type==ELSIF:
            node=self.elsif_statement()
        elif self.current_token.type==ELSE:
            node=self.else_statement()
        elif self.current_token.type==WHILE:
            node=self.while_statement()
        else:
            node=self.conditional_statement()
        return node

    def assignment_statement(self):
        """assignment_statement : variable ASSIGN expr"""
        left = self.variable()
        token = self.current_token
        self.eat(ASSIGN)
        right = self.expr()
        node = Assign(left, token, right)
        return node

    def if_statement(self):
        """
        if_statement : IF conditional_statement  statement_list  (elsif_statement | else_statement | empty) END

        """
        self.eat(IF)
        condition = self.conditional_statement()
        body=[]
        rest=[]
        while self.current_token.type!=ELSIF and self.current_token.type!=ELSE and self.current_token.type!=END:
            body.append(self.statement())
        if self.current_token.type==ELSIF:
            rest = self.elsif_statement()
        if self.current_token.type==ELSE:
            rest = self.else_statement()
        node = If(condition, body, rest)
        return node

    def while_statement(self):
        """
        while_statement : WHILE conditional_statement statement_list END

        """
        self.eat(WHILE)
        condition=self.conditional_statement()
        body=[]
        while self.current_token.type!=END:
            body.append(self.statement())
        self.eat(END)
        node=While(condition,body)
        return node
    
    def variable(self):
        """
        variable : ID

        """
        node = Var(self.current_token)
        self.eat(ID)
        return node

    def empty(self):
        """An empty production"""
        return NoOp()

    def elsif_statement(self):
        """
        elsif_statement : ELSIF conditional_statement statement_list (else | empty)
        """
        self.eat(ELSIF)
        elsif_condition=self.conditional_statement()
        elseif_body=[]
        rest=[]
        while self.current_token.type!=ELSE:
            elseif_body.append(self.statement())
        if self.current_token.type==ELSE:
            rest=self.else_statement()
        node=If(elsif_condition, elseif_body,rest)
        return node

    def else_statement(self):
        """else_statement : ELSE statement_list """
        self.eat(ELSE)
        else_body=[]
        while self.current_token.type!=END:
            else_body.append(self.statement())
        self.eat(END)
        node = Else(else_body)
        return node

    def conditional_statement(self):
        """conditional_statement : expr (EQUAL|GRE|NOT|GRET|LESE|LEST) expr"""
        node=self.expr()
        while self.current_token.type in (EQUAL,GRE,NOT,GRET,LESE,LEST):
            token=self.current_token()
            self.eat(token.type)
            node=BinOp(node,token,self.expr())
        return node

    def expr(self):
        """
        expr : term ((PLUS | MINUS) term)*
        """
        node = self.term()
        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
            elif token.type == MINUS:
                self.eat(MINUS)

            node = BinOp(node,token,self.term())
        return node

    def term(self):
        """term : factor ((MUL | DIV | MOD | EQUAL | NOT | LEST | GRET | LESE | GRE) factor)*"""
        node = self.factor()
        while self.current_token.type in (MUL,DIV, MOD,EQUAL,NOT,LEST,GRET,LESE,GRE):
            token = self.current_token
            if token.type == MUL:
                self.eat(MUL)
            elif token.type == DIV:
                self.eat(DIV)
            elif token.type == MOD:
                self.eat(MOD)
            elif token.type == EQUAL:
                self.eat(EQUAL)
            elif token.type == NOT:
                self.eat(NOT)
            elif token.type == LEST:
                self.eat(LEST)
            elif token.type == GRET:
                self.eat(GRET)
            elif token.type == LESE:
                self.eat(LESE)
            elif token.type == GRE:
                self.eat(GRE)
            node = BinOp(node,token,self.factor())

        return node

    def factor(self):
        """factor : PLUS factor
                  | MINUS factor
                  | INTEGER
                  | REAL
                  | LPAREN expr RPAREN
                  | variable
        """
        token = self.current_token
        if token.type == INTEGER:
            self.eat(INTEGER)
            return Num(token)
        elif token.type == REAL:
            self.eat(REAL)
            return Num(token)
        elif token.type == PLUS:
            self.eat(PLUS)
            node = UnaryOp(token, self.factor())
            return node
        elif token.type == MINUS:
            self.eat(MINUS)
            node = UnaryOp(token, self.factor())
            return node
        elif token.type == LPAREN:
            self.eat(LPAREN)
            node = self.expr()
            self.eat(RPAREN)
            return node
        elif token.type == ID:
            self.eat(ID)
            return Var(token)
        elif token.type == STR:
            self.eat(STR)
            return Num(token)
        else:
            node = self.variable()
            return node

    def parse(self):
        """
        program : compound_statement
        compound_statement : statement_list
        statement_list : statement | statement SEMI statement_list
        statement : compound_statement | assignment_statement |  if_statement | elsif_statement| else statement | while statement| empty
        assignment_statement : variable ASSIGN expr
        if_statement : IF conditional_statement  statement_list  (elsif_statement | else_statement | empty) END
        elsif_statement : ELSIF conditional_statement statement_list (else | empty)
        else_statement : ELSE statement_list
        while_statement : WHILE conditional_statement statement_list END
        conditional_statement : expr (EQUAL|GRE|NOT|GRET|LESE|LEST) expr
        expr : term ((PLUS | MINUS) term)*
        term : factor ((MUL | DIV | MOD | EQUAL | NOT | LEST | GRET | LESE | GRE) factor)*
        factor : PLUS factor
                  | MINUS factor
                  | INTEGER
                  | REAL
                  | LPAREN expr RPAREN
                  | variable
        variable : ID

        """
        node = self.program()
        while self.current_token.type != EOF:
            self.error()
        return node


class NodeVisitor(object):
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))