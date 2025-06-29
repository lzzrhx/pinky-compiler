import sys
from utils import *
from lexer import *
from tokens import *
from parser import *
from interpreter import *
from compiler import *
from vm import *

VERBOSE = True
PRINT_SOURCE = True
PRINT_LEXER = True
PRINT_PARSER = True
PRINT_COMPILER = True
DEBUG_MODE_COMPILER = True

if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('Usage: python3 pinky.py <filename>')
    filename = sys.argv[1]

    # OPEN SOURCE FILE
    with open(filename) as file:
        
        print()
        print(f'{Colors.GREEN}* * * PINKY COMPILER * * *{Colors.WHITE}')
        print(f'{Colors.GREEN}Running {filename}{Colors.WHITE}')

        # SOURCE:
        source = file.read()
        if PRINT_SOURCE:
            print()
            print(f'{Colors.GREEN}--------------------------------------------------------------------------------{Colors.WHITE}')
            print(f'{Colors.GREEN}SOURCE:{Colors.WHITE}')
            print(f'{Colors.GREEN}--------------------------------------------------------------------------------{Colors.WHITE}')
            print(source)
        
        # LEXER:
        tokens = Lexer(source).tokenize()
        if PRINT_LEXER:
            print()
            print(f'{Colors.GREEN}--------------------------------------------------------------------------------{Colors.WHITE}')
            print(f'{Colors.GREEN}LEXER OUTPUT:{Colors.WHITE}')
            print(f'{Colors.GREEN}--------------------------------------------------------------------------------{Colors.WHITE}')
            for tok in tokens: print(tok)
        
        # PARSER:
        ast = Parser(tokens).parse()
        if PRINT_PARSER:
            print()
            print(f'{Colors.GREEN}--------------------------------------------------------------------------------{Colors.WHITE}')
            print(f'{Colors.GREEN}PARSER OUTPUT:{Colors.WHITE}')
            print(f'{Colors.GREEN}--------------------------------------------------------------------------------{Colors.WHITE}')
            print_ast(ast)
        
        # INTERPRETER:
        interpreter = Interpreter()
        print()
        print(f'{Colors.GREEN}--------------------------------------------------------------------------------{Colors.WHITE}')
        print(f'{Colors.GREEN}INTERPRETER OUTPUT:{Colors.WHITE}')
        print(f'{Colors.GREEN}--------------------------------------------------------------------------------{Colors.WHITE}')
        interpreter.interpret_ast(ast)
       
        # COMPILER:
        compiler = Compiler(DEBUG_MODE_COMPILER)
        code = compiler.generate_code(ast)
        if PRINT_COMPILER:
            print()
            print(f'{Colors.GREEN}--------------------------------------------------------------------------------{Colors.WHITE}')
            print(f'{Colors.GREEN}COMPILER OUTPUT:{Colors.WHITE}')
            print(f'{Colors.GREEN}--------------------------------------------------------------------------------{Colors.WHITE}')
            compiler.print()
        
        # VIRTUAL MACHINE
        vm = VM()
        print()
        print(f'{Colors.GREEN}--------------------------------------------------------------------------------{Colors.WHITE}')
        print(f'{Colors.GREEN}RUNNING VIRTUAL MACHINE:{Colors.WHITE}')
        print(f'{Colors.GREEN}--------------------------------------------------------------------------------{Colors.WHITE}')
        vm.run(code)

