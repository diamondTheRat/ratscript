from lexer import Tokens
from typing import Any
from data_types import *
from error_handling import Errors
import errors

class Node:
    def __init__(self, type: Any, left: Any = None, right: Any = None):
        self.type = type
        self.left = left
        self.right = right

    def __repr__(self):
        if self.left is None:
            return f"{TYPES[self.type]}"
        elif self.right is None:
            return f"{TYPES[self.type]}({self.left})"
        else:
            return f"{TYPES[self.type]}({self.left}, {self.right})"

SIMPLE_ATOM_TYPES = [VARIABLE, FLOAT, INT, STRING, BOOL, RANDOM, INPUT]

class AbstractSyntaxTree:
    def __init__(self, tree):
        self.tree = tree
        self.index = -1
        self.instruction = None

    def __next__(self):
        try:
            self.index += 1
            self.instruction = self.tree[self.index]
            return self.instruction
        except IndexError:
            raise StopIteration()

    def append(self, node: Node):
        self.tree.append(node)

    def __repr__(self):
        return "\n".join([str(i) for i in self.tree])

    def __len__(self):
        return len(self.tree)

    def __getitem__(self, item):
        return self.tree[item]

class FunctionNode():
    def __init__(self, args: list, ast: AbstractSyntaxTree):
        self.args = args
        self.content = ast
        self.type = FUNCTION

    def __repr__(self):
        representation = f"Function ("
        representation += ", ".join([str(argument) for argument in self.args])

        representation += ') {\n\t'
        representation += "\n\t".join(str(self.content).split("\n"))
        representation += '\n}'

        return representation


class StatementNode:
    def __init__(self, type: Any, condition: Any, content: AbstractSyntaxTree, repeat: Any = None):
        self.type = type
        self.condition = condition
        self.content = content
        self.repeat = repeat
        self.other = []

    def __repr__(self):
        representation = f"{TYPES[self.type]} ({self.condition}"
        if self.repeat is not None:
            representation += f"; {self.repeat}"
        representation += ') {\n\t'
        representation += "\n\t".join(str(self.content).split("\n"))
        representation += '\n}'
        if len(self.other) != 0:
            for thing in self.other:
                representation += f"ELSE {thing}"

        return representation


class CallNode:
    def __init__(self, function: Any, arguments: list[Any]):
        self.type = CALL
        self.function = function
        self.arguments = arguments

    def __repr__(self):
        representation = f"CALL({self.function}"
        if len(self.arguments) != 0:
            representation += f", {self.arguments}"
        representation += ")"
        return representation

class Parser:
    def __init__(self, tokens: Tokens):
        self.tokens = tokens
        self.err_handler: Errors = tokens.error_handler

    def throw(self, prompt: str) -> None:
        if self.current_token is None:
            self.go_back()
        if self.current_token.type in [ENDL, INDENT]:
            self.go_back()

        err = errors.SyntaxError(prompt)
        self.err_handler.format(err, self.current_token.line, self.current_token.column, self.current_token.length)
        self.err_handler.throw(err)

    def advance(self) -> None:
        try:
            self.current_token = self.tokens.__next__()
        except StopIteration:
            self.current_token = None

    def go_back(self, steps: int = 1) -> None:
        for i in range(steps):
            self.current_token = self.tokens.previous()
        self.tokens.index -= steps


    def parse(self, indent: int = 0) -> AbstractSyntaxTree:
        tree = AbstractSyntaxTree([])
        self.advance()
        while self.current_token != None:
            output = False
            if indent != 0 and self.current_token.type not in (INDENT, ENDL):
                return tree
            elif self.current_token.type == INDENT:
                if self.current_token.value < indent:
                    return tree
                elif self.current_token.value != indent:
                    self.throw("you did done the silly with the indents :3")
                self.advance()

            if self.current_token.type == VARIABLE:
                var = self.current_token
                self.advance()
                output = False
                if self.current_token is None:
                    output = True
                    self.go_back(2)
                else:
                    previous_index = self.tokens.index
                    while self.current_token is not None and self.current_token.type == LIST_BEGIN:
                        var = Node(INDEX, var, self.expression())
                        self.advance()

                    if self.current_token.type == ASSIGN:
                        exp = self.expression()
                        if exp is None:
                            self.throw(f"idk wat to assign to '{var.value}' ;c")
                        tree.append(Node(ASSIGN, var, exp))
                    else:
                        output = True
                        self.tokens.index = previous_index
                        self.go_back(2)
            elif self.current_token.type == IF:
                exp = self.expression()
                if exp is None:
                    self.go_back()
                    self.throw("why dere no condition >:c")
                _ast = self.parse(indent + 1)
                if len(_ast) == 0:
                    self.go_back()
                    self.throw("why dere nuthin after dis statement hmph")
                tree.append(StatementNode(IF, exp, _ast))
            elif self.current_token.type == ELSE:
                if tree[-1].type != IF:
                    self.throw("'nuh uh' can onli be uzd on 'dis tru' statements u silly rat :3")
                _ast = self.parse(indent + 1)
                if len(_ast) == 0:
                    self.throw("why dere nuthin after dis statement hmph")
                tree[-1].other.append(StatementNode(IF, Bool(1), _ast))
            elif self.current_token.type == ELSE_IF:
                if tree[-1].type != IF:
                    self.throw("'mabe dis' can onli be uzd on 'dis tru' statements u silly rat :3")

                exp = self.expression()
                if exp is None:
                    self.go_back()
                    self.throw("why dere no condition >:c")

                _ast = self.parse(indent + 1)
                if len(_ast) == 0:
                    self.throw("why dere nuthin after dis statement hmph")
                tree[-1].other.append(StatementNode(IF, exp, _ast))
            elif self.current_token.type == LOOP:
                exp = self.expression()
                if exp is None:
                    self.throw("why dere no condition >:c")
                is_for = False
                if self.current_token.type == FORLOOP:
                    is_for = True
                    repeat_exp = self.expression()
                    if repeat_exp is None:
                        self.throw("why dere nothing in da repeat thingy hmph")

                _ast = self.parse(indent + 1)
                if len(_ast) == 0:
                    self.throw("why dere no code after dis statement hmph")
                if is_for:
                    tree.append(StatementNode(FORLOOP, exp, _ast, repeat_exp))
                else:
                    tree.append(StatementNode(WHILE, exp, _ast))
            elif self.current_token.type in SIMPLE_ATOM_TYPES + [LIST_BEGIN, DICT_BEGIN, BRACKET_OPEN]:
                output = True
                self.go_back(1)
            elif self.current_token.type == DEFINE:
                self.advance()
                func = self.current_token

                if func is None:
                    self.throw("chu must put a function thingy after 'maek' silly :3")
                if func.type != VARIABLE:
                    self.throw("it haz to be '<name>(<args>)' not wutever u did owo")

                self.advance()

                err = False
                if self.current_token.type is None:
                    err = True
                if self.current_token.type != BRACKET_OPEN:
                    err = True

                if err:
                    self.throw("it haz to be '<name>(<args>)' not wutever u did owo")

                args = []
                self.advance()
                while self.current_token is not None and self.current_token.type != BRACKET_CLOSE:
                    if self.current_token.type == VARIABLE:
                        args.append(self.current_token)
                        self.advance()
                    elif self.current_token.type in [SEPARATOR, ENDL, INDENT]:
                        self.advance()
                    elif self.current_token.type != BRACKET_CLOSE:
                        self.throw("wut")

                if self.current_token.type != BRACKET_CLOSE:
                    self.throw("hmph u iz meant to close the bracket >:c")

                self.advance()
                err = False
                if self.current_token.type is None:
                    err = True
                if self.current_token.type != DEFINE_END:
                    err = True

                if err:
                    self.throw("u forgor the 'do' at the end uwu")
                _ast = self.parse(indent + 1)
                if len(_ast) == 0:
                    self.throw("why dere no code after dis statement hmph")
                else:
                    tree.append(Node(ASSIGN, func, FunctionNode(args, _ast)))
            elif self.current_token.type == RETURN:
                tree.append(Node(RETURN, self.expression()))
            elif self.current_token.type == ENDL:
                self.advance()
            elif self.current_token.type == NO_OUTPUT:
                exp = self.expression()
                if exp:
                    tree.append(Node(NO_OUTPUT, exp))
            else:
                self.throw("wut u do on this line me no understand")

            if output:
                exp = self.expression()
                if exp is not None:
                    tree.append(Node(OUTPUT, exp))

        return tree

    def expression(self):
        left = self.comparison_expression()
        while self.current_token is not None and self.current_token.type in (AND, OR):
            left = Node(self.current_token.type, left, self.comparison_expression())
        return left

    def comparison_expression(self) -> Node:
        left = self.arithmetic_expression()
        while self.current_token is not None and self.current_token.type in (SMALLER, BIGGER, EQUALS):
            token = self.current_token.type
            self.advance()
            if token in (SMALLER, BIGGER) and self.current_token.type == EQUALS:
                # bigger/equals ID is 4 bigger than bigger
                # same for smaller/equals and smaller
                # please dont change the ids im begging u
                self.current_token.type = token + 4
                self.advance()
            self.go_back()
            left = Node(self.current_token.type, left, self.arithmetic_expression())
        return left

    def arithmetic_expression(self) -> Node:
        left = self.term()
        while self.current_token is not None and self.current_token.type in (SUBTRACT, ADD):
            left = Node(self.current_token.type, left, self.term())
        return left

    def term(self) -> Node:
        left = self.atom()
        self.advance()
        found = False
        while self.current_token and self.current_token.type in (MULTIPLY, DIVIDE, MODULO, INT_DIVISION, INCREASE, DECREASE):
            found = True
            left = Node(self.current_token.type, left, self.atom())
            self.advance()

        return left

    def atom(self):
        self.advance()
        if self.current_token == None:
            return None
        elif self.current_token.type == SUBTRACT:
            return Node(NEGATIVE, self.atom())
        elif self.current_token.type in SIMPLE_ATOM_TYPES:
            if self.current_token.type == VARIABLE:
                variable = self.current_token
                self.advance()
                if self.current_token is not None:
                    if self.current_token.type is LIST_BEGIN:
                        _index = None
                        while self.current_token is not None and self.current_token.type == LIST_BEGIN:
                            variable = Node(INDEX, variable, (_index := self.expression()))
                            if _index is None:
                                self.throw("idk wut index u wants me to taek >:c")
                            self.advance()
                        self.go_back()
                        err = False
                        if self.current_token is None:
                            err = True
                        elif self.current_token.type != LIST_END:
                            err = True
                        elif _index is None:
                            self.throw("idk wut index u wants me to taek >:c")

                        if err:
                            self.throw("where iz da ']'?!?! dum dum")
                        return Node(INDEX, variable.left, variable.right)
                    elif self.current_token.type is BRACKET_OPEN:
                        args = []
                        self.advance()
                        err = False
                        if self.current_token is None:
                            err = True
                        elif self.current_token.type is BRACKET_CLOSE:
                            return CallNode(variable, args)

                        if err:
                            self.throw("u no close da function call with ')' >:c")
                        self.go_back()
                        while self.current_token is not None and self.current_token.type != BRACKET_CLOSE:
                            if self.current_token.type is ENDL:
                                self.advance()
                                if self.current_token.type != INDENT:
                                    self.go_back()
                            args.append(self.expression())
                            if self.current_token.type != SEPARATOR and self.current_token.type != BRACKET_CLOSE:
                                self.throw("where iz da ',' separator hmph")

                        err = False
                        if self.current_token is None:
                            err = True
                        elif self.current_token.type != BRACKET_CLOSE:
                            err = True

                        if err:
                            self.throw("u no close da function call with ')' >:c")

                        return CallNode(variable, args)
                self.go_back()

            return self.current_token
        elif self.current_token.type == BRACKET_OPEN:
            result = self.expression()
            err = False
            if self.current_token is None:
                err = True
            elif self.current_token.type != BRACKET_CLOSE:
                err = True
            if err:
                self.throw("Expected closing parenthesis ')'")
            return result
        elif self.current_token.type == LIST_BEGIN:
            elements = []
            self.advance()
            if self.current_token is None:
                self.throw("u no close da list thingy i think")

            if self.current_token.type is LIST_END:
                return List([])

            if self.current_token.type != ENDL:
                self.go_back()

            while self.current_token is not None and self.current_token.type != LIST_END:
                found = False
                while self.current_token is not None and self.current_token.type in [SEPARATOR, ENDL, INDENT]:
                    found = True
                    self.advance()

                if self.current_token is None:
                    break

                if self.current_token is not None and self.current_token.type == LIST_END:
                    break

                if found:
                    self.go_back()

                elements.append(self.expression())
                if elements[-1] is None:
                    err = False
                    if self.current_token is None:
                        err = True
                    elif self.current_token.type != LIST_END:
                        err = True

                    if err:
                        self.throw("u no close da list thingy i think")


            err = False
            if self.current_token is None:
                err = True
            elif self.current_token.type != LIST_END:
                err = True
            if err:
                self.throw("u no close da list thingy i think")

            return List(elements)
        elif self.current_token.type == DICT_BEGIN:
            elements = {}

            self.advance()
            if self.current_token.type != ENDL:
                self.go_back()

            while self.current_token is not None and self.current_token.type != DICT_END:
                found = False
                while self.current_token is not None and self.current_token.type in [SEPARATOR, ENDL, INDENT]:
                    found = True
                    self.advance()

                if self.current_token is not None and self.current_token.type == DICT_END:
                    break

                if found:
                    self.go_back()

                key = self.expression()

                err = False
                if self.current_token is None:
                    err = True
                elif self.current_token.type != KEY_VALUE_SEPARATOR:
                    err = True

                if err:
                    self.throw("where da ':' separator owo")
                value = self.expression()
                elements[key] = value
            err = False
            if self.current_token is None:
                err = True
            elif self.current_token.type != DICT_END:
                err = True

            if err:
                self.throw("Expected closing list '}'")
            return Dict(elements)
        elif self.current_token.type == NOT:
            self.advance()
            if self.current_token is None:
                self.throw("wut iz u trying to use 'nu' on?")
            self.go_back()
            comp = self.comparison_expression()
            self.go_back()
            return Node(NOT, comp)


def parse(tokens: Tokens) -> AbstractSyntaxTree:
    parser = Parser(tokens)
    return parser.parse()
