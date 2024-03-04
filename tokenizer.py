from error_handling import Errors
from typing import Callable, Any, NoReturn
import errors as errors
from colorama import Fore
from data_types import *

EMPTY = 0
NOT_EMPTY = 1

FILE_TOKENIZATION = 0
LINE_TOKENIZATION = 1

class Tokens:
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = -1

        self.token = None

        self.error_handler = None

    def append_word(self, word: str, line: int, column: int, is_space: bool = True) -> NoReturn:
        if word != "":
            if word in keywords:
                self.append(keywords[word](), line, column - len(word) - is_space + 1, len(word))
            else:
                self.append(Variable(VARIABLE, word), line, column - len(word) - is_space + 1, len(word))

    def append(self, item: Any, line: int, column: int, length: int = 1) -> NoReturn:
        item.line = line
        item.column = column
        item.length = length
        self.tokens.append(item)

    def __getitem__(self, index):
        return self.tokens[index]

    def __len__(self):
        return len(self.tokens)

    def __next__(self):
        try:
            self.index += 1
            self.token = self.tokens[self.index]
            return self.tokens[self.index]
        except IndexError:
            raise StopIteration()

    def previous(self):
        return self.tokens[self.index - 1]

    def __repr__(self):
        representation = ""
        for index, token in enumerate(self.tokens):
            if token.type == ENDL:
                representation += str("\n")
            else:
                representation += str(token)
                if index < len(self.tokens) - 1 and self.tokens[index + 1].type != ENDL:
                    representation += " | "
        return representation

def handle_empty_lines(line_types) -> Callable:
    def get_line(line):
        count = -1
        line_count = -1
        while line_count != line + 1:
            line_count += (line_types[count] is NOT_EMPTY)
            count += 1

        count -= 1
        return count

    return get_line

def _format(text: str) -> str:
    formatted = ""

    empty_lines = []

    for line in text.split("\n"):
        line = line.split("~w~")[0]
        if line.count(" ") != len(line):
            while line[-1] == " ":
                line = line[:-1]
            formatted += f"{line}\n"
            empty_lines.append(NOT_EMPTY)
        else:
            empty_lines.append(EMPTY)

    return handle_empty_lines(empty_lines), formatted[:-1]

def valid_indention(line):
    spaces = 0
    while line[spaces] == ' ':
        spaces += 1


    if spaces % 2 == 1:
        return False
    else:
        return True

character_list = (letters := "qwertyuiopasdfghjklzxcvbnm_") + (digits := "1234567890") + " "
keywords = {
    "takewayz": Subtraction,
    "sumz": Addition,
    "timesiez": Multiplication,
    "divyd": Division,
    "smth": Random,
    "iz": Assign,
    "mor": Increase,
    "less": Decrease,
    "saem": Equals,
    "bigr": Bigger,
    "smolr": Smaller,
    "cuz": Loop,
    "btw": ForLoop,
    "mod": Modulo,
    "divz": IntDivision,
    "mabe this": ElseIf,
    "nuh uh": Else,
    "an": And,
    "or": Or,
    "nu": Not,
    "nah": lambda: Bool(0),
    "ya": lambda: Bool(1)
}

string_delimiters = '""'
list_delimiters = '[]'
dict_delimiters = '{}'

def tokenize(text: str, mode: int = FILE_TOKENIZATION, testing: bool = False) -> Tokens:
    error_handler = Errors(text)

    tokens = Tokens([])
    get_line, text = _format(text)
    error_handler.get_line = get_line
    error_handler.testing = testing
    tokens.error_handler = error_handler

    line_index = 0
    lines = text.split("\n")

    # check if file starts with owo and ends with uwu
    if len(lines) < 2 or (lines[0].rstrip(" ") != 'owo' or lines[-1].rstrip(" ") != 'uwu'):
        err = errors.SyntaxError(f"{Fore.RED}pliz start every file with 'owo' an end it with 'uwu'!!{Fore.RESET}")
        error_handler.throw(err)

    line_count = len(lines)
    word = ""
    while line_index < line_count - 2:
        line_index += 1
        line = lines[line_index]
        if not valid_indention(line):
            error_handler.inconsistent_indentation(line_index)

        spaces = 0
        while line[spaces] == " ":
            spaces += 1
        if spaces:
            tokens.append(Indent(spaces // 2), line_index, 0, spaces)
        word = ""

        line_length = len(line)
        line_end = line_length - 1
        column = -1

        while column < line_end:
            _is_character = False
            column += 1
            char = line[column]
            if char in character_list:
                _is_character = True
                if char in digits and word == "":
                    # get the number
                    number = ""
                    is_float = False
                    while column < line_length and line[column] in digits + '.':
                        char = line[column]
                        if char == '.':
                            if is_float:
                                err = errors.SyntaxError("wai dere 2 pointz in da numbr owo")
                                error_handler.format(err, line_index, column)
                                error_handler.throw(err)

                            is_float = True
                        number += char
                        column += 1
                    column -= 1
                    if is_float:
                        tokens.append(Float(float(number)), line_index, column)
                    else:
                        tokens.append(Int(int(number)), line_index, column)
                elif char in letters + digits:
                    word += char
                if char == " " or column == line_end:
                    # if word == "bigr":
                    #     if column + 3 >= line_length:
                    #         err = errors.SyntaxError("u not finish it ;c its 'bigr bai' silly :3")
                    #         error_handler.format(err, line_index, column - 3 - (char == " "), 4)
                    #         error_handler.throw(err)
                    #     if line[column + 1: column + 4] != "bai":
                    #         err = errors.SyntaxError("u not finish it ;c its 'bigr bai' silly :3")
                    #         error_handler.format(err, line_index, column - 3 - (char == " "), 4)
                    #         error_handler.throw(err)
                    #     column += 3
                    #     tokens.append(Increase())
                    if word == "dis":
                        if column + 3 >= line_length:
                            err = errors.SyntaxError("u not finish it ;c its 'dis tru' silly :3")
                            error_handler.format(err, line_index, column - 2 - (char == " "), 3)
                            error_handler.throw(err)
                        if line[column + 1: column + 4] != "tru":
                            err = errors.SyntaxError("u not finish it ;c its 'dis tru' silly :3")
                            error_handler.format(err, line_index, column - 2 - (char == " "), 3)
                            error_handler.throw(err)
                        if line[-1] != "?":
                            err = errors.SyntaxError("'dis tru' statements mus end wif '?' !!!! >:c")
                            error_handler.format(err, line_index, line_end)
                            error_handler.throw(err)

                        column += 3
                        line_length -= 1
                        line_end -= 1
                        tokens.append(If(), line_index, column - 6, 7)
                    elif word == "nuh":
                        if column + 2 >= line_length:
                            err = errors.SyntaxError("u not finish it ;c its 'nuh uh' silly :3")
                            error_handler.format(err, line_index, column - 2 - (char == " "), 3)
                            error_handler.throw(err)
                        if line[column + 1: column + 3] != "uh":
                            err = errors.SyntaxError("u not finish it ;c its 'nuh uh' silly :3")
                            error_handler.format(err, line_index, column - 2 - (char == " "), 3)
                            error_handler.throw(err)

                        column += 2
                        line_length -= 1
                        line_end -= 1
                        tokens.append(Else(), line_index, column - 5, 6)
                    elif word == "mabe":
                        if column + 4 >= line_length:
                            err = errors.SyntaxError("u not finish it ;c its 'mabe this' silly :3")
                            error_handler.format(err, line_index, column - 3 - (char == " "), 4)
                            error_handler.throw(err)
                        if line[column + 1: column + 5] != "this":
                            err = errors.SyntaxError("u not finish it ;c its 'mabe this' silly :3")
                            error_handler.format(err, line_index, column - 3 - (char == " "), 4)
                            error_handler.throw(err)
                        if line[-1] != "?":
                            err = errors.SyntaxError("'mabe this' statements mus end wif '?' !!!! >:c")
                            error_handler.format(err, line_index, column - 4, 9)
                            error_handler.throw(err)

                        column += 4
                        line_length -= 1
                        line_end -= 1
                        tokens.append(ElseIf(), line_index, column - 8, 9)
                    else:
                        tokens.append_word(word, line_index, column, (char == " "))
                    word = ""
            elif char == string_delimiters[0]:
                _content = ""
                column += 1
                while column < line_length and line[column] != string_delimiters[1]:
                    char = line[column]
                    column += 1

                    _content += char
                tokens.append(String(_content), line_index, column)
            elif char in list_delimiters:
                if char == list_delimiters[0]:
                    tokens.append(Operator(LIST_BEGIN), line_index, column)
                else:
                    tokens.append(Operator(LIST_END), line_index, column)
            elif char in dict_delimiters:
                if char == dict_delimiters[0]:
                    tokens.append(Operator(DICT_BEGIN), line_index, column)
                else:
                    tokens.append(Operator(DICT_END), line_index, column)
            elif char == ",":
                tokens.append(Operator(SEPARATOR), line_index, column)
            elif char == ":":
                tokens.append(Operator(KEY_VALUE_SEPARATOR), line_index, column)
            elif char == "(":
                tokens.append(Operator(BRACKET_OPEN), line_index, column)
            elif char == ")":
                tokens.append(Operator(BRACKET_CLOSE), line_index, column)
            elif char == "-":
                tokens.append(Operator(SUBTRACT), line_index, column)
            else:
                error_handler.unrecognized_character(line_index, column)

            if not _is_character:
                _last = tokens.tokens.pop(-1)
                tokens.append_word(word, line_index, column, False)
                tokens.append(_last, line_index, column)
                word = ""

        tokens.append(Endl(), line_index, column)
    return tokens