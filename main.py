from lexer import *
from parser_ruby import *
from interpreter import *

def main():
    file = open("./testCases/input_test6.txt", "r")
    text = file.read()
    lex = Lexer(text)
    # for i in range(0,15):
    #     print(lex.get_next_token())
    par = Parser(lex)
    tree = par.parse()
    print(tree)
    inter = Interpreter(tree)
    result = inter.interpret()
    print('Run-time GLOBAL_MEMORY contents:')
    print(inter.GLOBAL_MEMORY)

if __name__ == '__main__':
    main()
