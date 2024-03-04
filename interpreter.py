import random
from data_types import *
from parser import AbstractSyntaxTree, SIMPLE_ATOM_TYPES, Node
import math

_builtins = {
    "round": lambda *args: round(*args),
    "floor": lambda *args: math.floor(*args),
    "int": lambda *args: int(*args),
    "tell": lambda *args: input(*args)
}

thingies = {
    ADD: lambda a, b: a + b,
    SUBTRACT: lambda a, b: a - b,
    MULTIPLY: lambda a, b: a * b,
    DIVIDE: lambda a, b: a / b,
    INT_DIVISION: lambda a, b: a // b,
    BIGGER: lambda a, b: a > b,
    SMALLER: lambda a, b: a < b,
    EQUALS: lambda a, b: a == b,
    SMALLER_EQUALS: lambda a, b: a <= b,
    BIGGER_EQUALS: lambda a, b: a >= b,
    MODULO: lambda a, b: a % b,
    AND: lambda a, b: a and b,
    OR: lambda a, b: a or b,
    NOT: lambda a: not a,
    INPUT: lambda: input(),
    RANDOM: lambda: random.random()
}

class Interpreter:
    def __init__(self, ast: AbstractSyntaxTree):
        self.ast = ast
        self.instruction = None

    def advance(self):
        try:
            self.instruction = next(self.ast)
        except StopIteration:
            self.instruction = None

    def interpret(self, variables: dict = None, ast: AbstractSyntaxTree = None) -> None:
        self.ast = ast or self.ast
        variables = variables or {**_builtins}
        self.advance()
        while self.instruction != None:
            if self.instruction.type == OUTPUT:
                print(self.eval(self.instruction.left, variables))
            elif self.instruction.type == ASSIGN:
                variables[self.instruction.left.value] = self.eval(self.instruction.right, variables)
            elif self.instruction.type == WHILE:
                loop = self.instruction
                previous_ast = self.ast
                while self.eval(loop.condition, variables):
                    loop.content.index = -1
                    self.interpret(variables, loop.content)
                self.ast = previous_ast
            elif self.instruction.type == FORLOOP:
                loop = self.instruction
                previous_ast = self.ast
                while self.eval(loop.condition, variables):
                    loop.content.index = -1
                    self.interpret(variables, loop.content)
                    self.eval(loop.repeat, variables)
                self.ast = previous_ast
            elif self.instruction.type == IF:
                statement = self.instruction
                previous_ast = self.ast
                if self.eval(statement.condition, variables):
                    statement.content.index = -1
                    self.interpret(variables, statement.content)
                self.ast = previous_ast

            self.advance()

    def eval(self, expression: Node | Variable, variables: dict = None):
        if expression.type == CALL:
            return self.eval(expression.function, variables)(*(self.eval(i, variables) for i in expression.arguments))
        elif expression.type in SIMPLE_ATOM_TYPES:
            if expression.type == VARIABLE:
                return variables[expression.value]
            elif expression.type in [INPUT, RANDOM]:
                return thingies[expression.type]()
            else:
                return expression.value
        elif expression.type in thingies:
            operation = expression.type
            left_operand = self.eval(expression.left, variables) if expression.left else None
            right_operand = self.eval(expression.right, variables) if expression.right else None
            if right_operand is not None:
                result = thingies[operation](left_operand, right_operand)
            elif left_operand is not None:
                result = thingies[operation](left_operand)
            else:
                result = thingies[operation]()
            return result
        elif expression.type in [INCREASE, DECREASE]:
            var = expression.left.value
            variables[var] += self.eval(expression.right) * (1 - (2 * (expression.type == DECREASE)))
            return variables[var]

def interpret(ast: AbstractSyntaxTree) -> None:
    interpreter = Interpreter(ast)
    interpreter.interpret()
