from typing import NoReturn
from colorama import Fore
import errors
from errors import BaseError

class Errors:
    def __init__(self, prompt: str):
        """
        Made to represent errors and error handling.
        :param prompt: the content of the file
        """
        self.prompt = prompt
        self.get_line = lambda line: line
        self.testing = False

    def throw(self, err: BaseError) -> NoReturn:
        if self.testing:
            raise SyntaxError(str(err))
        else:
            print(err)
            exit(-1)

    def _raise_error(self, err, line, column, length = 1) -> NoReturn:
        self.format(err, line, column, length)
        self.throw(err)

    def unrecognized_character(self, line: int, column: int) -> NoReturn:
        _line = self.get_line(line)
        content = self.prompt.split("\n")[_line]

        character = content[column]
        err = errors.SyntaxError(f"wut iz dis '{character}' owo")
        self._raise_error(err, line, column)

    def inconsistent_indentation(self, line: int) -> NoReturn:
        length = 0
        line_content = self.prompt.split("\n")[line]
        while line_content[length] == " ":
            length += 1

        err = errors.SyntaxError(f"nuh uh meanie ;c me no likies when chu doesnt use double space for indentation hmph")
        self._raise_error(err, line, 0, length)

    def format(self, err: BaseError, line: int, column: int, err_length: int = 1) -> NoReturn:
        """
        Formats the error in more readable way.
        :param err: the error type
        :param line: the line
        :param column: starting character
        :param err_length: size of problem area
        :return:
        """
        line = self.get_line(line)
        text = self.prompt.split('\n')[line]
        line_length = len(text)
        while line_length != 0 and text[-1] == " ":
            text = text[:-1]
            line_length -= 1

        pointer = '-' * column
        if err_length == 1:
            pointer += '^'
        else:
            pointer += '~' * err_length
        pointer += '-' * (line_length - (column + err_length))

        err_message = f"At line {line + 1} column {column + 1}\n"
        err_message += f"{type(err).__name__}: {err.prompt}"
        text = f"{Fore.RED}{text}\n{pointer}\n{err_message}{Fore.RESET}"

        err.prompt = text
