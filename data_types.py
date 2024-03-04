ENDL = 0
INT = 1
FLOAT = 2
STRING = 3
LIST = 4
ADD = 5
SUBTRACT = 6
MULTIPLY = 7
DIVIDE = 8
VARIABLE = 9
DICT = 10
LIST_BEGIN = 11
LIST_END = 12
SEPARATOR = 13
DICT_BEGIN = 14
DICT_END = 15
KEY_VALUE_SEPARATOR = 16
INPUT = 17
BRACKET_OPEN = 18
BRACKET_CLOSE = 19
NEGATIVE = 20
ASSIGN = 21
OUTPUT = 22
INDENT = 23
RANDOM = 24
INCREASE = 25
IF = 26
BIGGER = 27
SMALLER = 28
EQUALS = 29
LOOP = 30
BIGGER_EQUALS = 31
SMALLER_EQUALS = 32
FORLOOP = 33
WHILE = 34
INDEX = 35
CALL = 36
MODULO = 37
INT_DIVISION = 38
ELSE_IF = 39
ELSE = 40
DECREASE = 41
AND = 42
OR = 43
NOT = 44
BOOL = 45

TYPES = {
    ENDL: "ENDL",
    INT: "INT",
    FLOAT: "FLOAT",
    STRING: "STRING",
    LIST: "LIST",
    DICT: "DICT",
    ADD: "ADD",
    SUBTRACT: "SUBTRACT",
    MULTIPLY: "MULTIPLY",
    DIVIDE: "DIVIDE",
    VARIABLE: "VARIABLE",
    LIST_BEGIN: "LIST_BEGIN",
    LIST_END: "LIST_END",
    SEPARATOR: "SEPARATOR",
    DICT_BEGIN: "DICT_BEGIN",
    DICT_END: "DICT_END",
    KEY_VALUE_SEPARATOR: "KEY_VALUE_SEPARATOR",
    INPUT: "INPUT",
    RANDOM: "RANDOM",
    INDENT: "INDENT",
    BRACKET_OPEN: "BRACKET_OPEN" ,
    BRACKET_CLOSE: "BRACKET_CLOSE",
    NEGATIVE: "NEG",
    ASSIGN: "ASSIGN",
    OUTPUT: "OUTPUT",
    INCREASE: "INCREASE",
    IF: "IF",
    BIGGER: "BIGGER",
    SMALLER: "SMALLER",
    EQUALS: "EQUALS",
    LOOP: "LOOP",
    BIGGER_EQUALS: "BIGGER/EQUALS",
    SMALLER_EQUALS: "SMALLER/EQUALS",
    FORLOOP: "FOR",
    WHILE: "WHILE",
    INDEX: "INDEX",
    CALL: "CALL",
    MODULO: "MOD",
    INT_DIVISION: "INT_DIVISION",
    ELSE_IF: "ELSE_IF",
    ELSE: "ELSE",
    DECREASE: "DECREASE",
    AND: "AND",
    OR: "OR",
    NOT: "NOT",
    BOOL: "BOOL"
}

class Operator:
    def __init__(self, type: int):
        self.type = type

    def __repr__(self):
        return f"{TYPES[self.type]}"

class Indent:
    def __init__(self, value: int):
        self.type = INDENT
        self.value = value

    def __repr__(self):
        return f"INDENT: {self.value}"
class Addition(Operator):
    def __init__(self):
        super().__init__(ADD)

class Subtraction(Operator):
    def __init__(self):
        super().__init__(SUBTRACT)

class Multiplication(Operator):
    def __init__(self):
        super().__init__(MULTIPLY)

class Division(Operator):
    def __init__(self):
        super().__init__(DIVIDE)

class Modulo(Operator):
    def __init__(self):
        super().__init__(MODULO)

class IntDivision(Operator):
    def __init__(self):
        super().__init__(INT_DIVISION)

class Equals(Operator):
    def __init__(self):
        super().__init__(EQUALS)

class Bigger(Operator):
    def __init__(self):
        super().__init__(BIGGER)

class Smaller(Operator):
    def __init__(self):
        super().__init__(SMALLER)

class Equals(Operator):
    def __init__(self):
        super().__init__(EQUALS)

class And(Operator):
    def __init__(self):
        super().__init__(AND)

class Or(Operator):
    def __init__(self):
        super().__init__(OR)

class Not(Operator):
    def __init__(self):
        super().__init__(NOT)

class Input(Operator):
    def __init__(self):
        super().__init__(INPUT)

class Random(Operator):
    def __init__(self):
        super().__init__(RANDOM)

class Assign(Operator):
    def __init__(self):
        super().__init__(ASSIGN)

class Increase(Operator):
    def __init__(self):
        super().__init__(INCREASE)

class Decrease(Operator):
    def __init__(self):
        super().__init__(DECREASE)

class Index(Operator):
    def __init__(self):
        super().__init__(INDEX)

class Call(Operator):
    def __init__(self):
        super().__init__(CALL)

class Statement:
    def __init__(self, type):
        self.type = type

    def __repr__(self):
        return TYPES[self.type]

class If(Statement):
    def __init__(self):
        super().__init__(IF)

class Loop(Statement):
    def __init__(self):
        super().__init__(LOOP)

class ForLoop(Statement):
    def __init__(self):
        super().__init__(FORLOOP)

class While(Statement):
    def __init__(self):
        super().__init__(WHILE)


class Else(Statement):
    def __init__(self):
        super().__init__(ELSE)

class ElseIf(Statement):
    def __init__(self):
        super().__init__(ELSE_IF)

class Variable:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"{TYPES[self.type]}: {self.value}"

class Int(Variable):
    def __init__(self, value):
        super().__init__(INT, value)

class Bool(Variable):
    def __init__(self, value):
        super().__init__(BOOL, (value == 1))

class Float(Variable):
    def __init__(self, value):
        super().__init__(FLOAT, value)

class String(Variable):
    def __init__(self, value):
        super().__init__(STRING, value)

    def __repr__(self):
        return f"{TYPES[self.type]}: '{self.value}'"

class List(Variable):
    def __init__(self, value):
        super().__init__(LIST, value)

    def __repr__(self):
        return f"{TYPES[self.type]}: [{', '.join([str(i) for i in self.value])}]"


class Dict(Variable):
    def __init__(self, value):
        super().__init__(DICT, value)

    def __repr__(self):
        return f"{TYPES[self.type]}: {'{'}'{', '.join(['(' + str(i) + ')' + ': ' + '(' + str(v) + ')' for i, v in self.value.items()])}{'}'}"

class Endl:
    def __init__(self):
        self.type = ENDL

    def __repr__(self):
        return f"END LINE"