import os.path
import tokenizer
import parser
import interpreter
from colorama import Fore
import sys

path = sys.argv[1]

try:
    with open(path) as f:
        text = f.read()

    tokens = tokenizer.tokenize(text)
    ast = parser.parse(tokens)

    interpreter.interpret(ast)
except FileNotFoundError:
    print(f"{Fore.RED}Couldn't find specified path{Fore.RESET}")