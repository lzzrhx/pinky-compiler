import sys
from utils import *
from lexer import *
from tokens import *
from parser import *

if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('Usage: python3 pinky.py <filename>')
    filename = sys.argv[1]
    print(filename)

    with open(filename) as file:
        source = file.read()
        
        print("--------------------------------------------------------------------------------")
        print("SOURCE:")
        print("--------------------------------------------------------------------------------")
        print(source)

        print()
        print("--------------------------------------------------------------------------------")
        print("LEXER:")
        print("--------------------------------------------------------------------------------")
        tokens = Lexer(source).tokenize()
        for tok in tokens: print(tok)

        print()
        print("--------------------------------------------------------------------------------")
        print("PARSED AST:")
        print("--------------------------------------------------------------------------------")
        ast = Parser(tokens).parse()
        print_pretty_ast(ast)

