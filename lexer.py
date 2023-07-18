
#token types
PLUS='PLUS'
MINUS='MINUS'
MUL='MUL'
DIV='DIV'
MOD='MOD'
LPAREN='('
RPAREN=')'
APOS='"'
INTEGER='INTEGER'
REAL='REAL'
EOF='EOF'
STR='STR'
TRUE='TRUE'
FALSE='FALSE'
EQUAL='=='
NOT='!='
GRET='>'
LEST='<'
GRE='>='
LESE='<='
ASSIGN='='
SEMI=';'
ID='ID'
COMMA=','
DOT='.'
FOR='for'
WHILE='while'
IF='if'
ELSE='else'
ELSIF='elsif'
END='end'

class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        """String representation of the class instance.
        Examples:
            Token(INTEGER, 3)
            Token(PLUS, '+')
            Token(EQUAL, '==')
        """
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()


RESERVED_KEYWORDS={
    'if': Token(IF, 'if'),
    'elsif': Token(ELSIF, 'elsif'),
    'else': Token(ELSE, 'else'),
    'while': Token(WHILE, 'while'),
    'end': Token(END, 'end'),
    'true': Token(TRUE, 'true'),
    'false': Token(FALSE, 'false')
}


class Lexer(object):
    def __init__(self, text):
        # string input: "2+3*4"
        self.text = text
        # pos is a pointer to the current character of 'text'
        self.pos = 0
        self.line = 1
        # current token 
        self.current_token = None
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('Invalid syntax')

    def advance(self):
        """Advance the pos pointer and set the current_char variable."""
        self.pos += 1

        if self.pos > len(self.text) - 1:      #This indicates EOF or end of line
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def peek(self, n):
        """Peeks the character n characters away from the current current character."""
        peek_pos = self.pos + n
        if peek_pos > len(self.text) - 1:      #Indicates EOF
            return None
        else:
            return self.text[peek_pos]

    def skip_white_space(self):
        """Skips white space in the input."""
        while self.current_char is not None and self.current_char.isspace():
            if self.current_char == '\n':
                self.line += 1
            self.advance()

    def skip_comment(self):
        """Skips comments in the input."""
        while self.current_char not in ['\n','\x00']:
            self.advance()

    def number(self):
        """Returns an integer(multidigit) or a float that is read from the input"""
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()

        if self.current_char == '.':
            result += self.current_char
            self.advance()

            while self.current_char is not None and self.current_char.isdigit():
                result += self.current_char
                self.advance()

            token = Token('REAL', float(result))

        else:
            token = Token('INTEGER', int(result))

        return token

    def string(self):
        result = ''
        self.advance()
        while self.current_char is not None and self.current_char != '"':
            result += self.current_char
            self.advance()
        self.advance()

        token = Token('STR', result)
        return token

    def _id(self):
        """Handle identifiers and reserved keywords"""
        result = ''
        while self.current_char is not None and self.current_char.isalnum() or self.current_char=='_':
            result += self.current_char
            self.advance()

        token = RESERVED_KEYWORDS.get(result, Token(ID, result))
        return token

    def get_next_token(self):
        """Lexical analyzer (also known as scanner or tokenizer)
        This method is responsible for breaking a sentence
        apart into tokens. One token at a time."""
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_white_space()
                continue

            if self.current_char == '#':
                self.advance()
                self.skip_comment()
                continue

            if self.current_char.isalpha():
                return self._id()

            if self.current_char.isdigit():
                return self.number()

            if self.current_char == '=' and self.peek(1)!='=':
                self.advance()
                return Token(ASSIGN, '=')

            if self.current_char == '=' and self.peek(1)=='=':
                self.advance()
                self.advance()
                return Token(EQUAL, '==')

            if self.current_char == '!' and self.peek(1)=='=':
                self.advance()
                self.advance()
                return Token(NOT, '!=')

            if self.current_char == '>' and self.peek(1)!='=':
                self.advance()
                return Token(GRET, '>')

            if self.current_char == '<' and self.peek(1) == '=':
                self.advance()
                self.advance()
                return Token(LESE, '<=')

            if self.current_char == '>' and self.peek(1) == '=':
                self.advance()
                self.advance()
                return Token(GRE, '>=')

            if self.current_char == '<' and self.peek(1) != '=':
                self.advance()
                return Token(LEST, '<')

            if self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')

            if self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')

            if self.current_char == '*':
                self.advance()
                return Token(MUL, '*')

            if self.current_char == '/':
                self.advance()
                return Token(DIV, '/')

            if self.current_char == '%':
                self.advance()
                return Token(MOD, '%')

            if self.current_char == ';':
                self.advance()
                return Token(SEMI, ';')

            if self.current_char == ',':
                self.advance()
                return Token(COMMA, ',')

            if self.current_char == 'i' and self.peek(1) == 'f':
                self.advance()
                self.advance()
                return Token(IF, 'if')

            if self.current_char == 'e' and self.peek(1) == 'l' and self.peek(2) == 's' and self.peek(3) == 'e':
                for x in range (0,4):
                    self.advance()
                return Token(ELSE,'else')

            if self.current_char == 'e' and self.peek(1) == 'l' and self.peek(2) == 's' and self.peek(3) == 'i' and self.peek(4) == 'f':
                for x in range (0,5):
                    self.advance()
                return Token(ELSIF,'elsif')

            if self.current_char == 'w' and self.peek(1) == 'h' and self.peek(2) == 'i' and self.peek(3) == 'l' and self.peek(4) == 'e' and self.peek(5):
                for x in range (0,5):
                    self.advance()
                return Token(WHILE, 'while')

            if self.current_char == 'e' and self.peek(1) == 'n' and self.peek(2) == 'd':
                for x in range (0, 3):
                    self.advance()
                return Token(END, 'end')

            if self.current_char == 't' and self.peek(1) == 'r' and self.peek(2)=='u' and self.peek(3)=='e':
                for x in range (0,4):
                    self.advance()
                return Token(TRUE, 'true')

            if self.current_char == 'f' and self.peek(1) == 'a' and self.peek(2)=='l' and self.peek(3)=='s' and self.peek(4)=='e':
                for x in range (0,5):
                    self.advance()
                return Token(FALSE, 'false')

            if self.current_char == ')':
                self.advance()
                return Token(RPAREN, ')')

            if self.current_char == '(':
                self.advance()
                return Token(LPAREN, '(')

            if self.current_char == '.':
                self.advance()
                return Token(DOT, '.')

            if self.current_char == '"':
                self.advance()
                return Token(APOS,'"')

            self.error()

        return Token(EOF, None)