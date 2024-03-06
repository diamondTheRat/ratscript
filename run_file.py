import os.path
import lexer
import parser
import interpreter
from colorama import Fore
import sys

path = sys.argv[1]

try:
    with open(path) as f:
        text = f.read()

    tokens = lexer.lex(text)
    ast = parser.parse(tokens)

    interpreter.interpret(ast)
except FileNotFoundError:
    print(f"{Fore.RED}Couldn't find specified path{Fore.RESET}")