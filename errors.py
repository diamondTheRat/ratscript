class BaseError:
    def __init__(self, prompt: str):
        """
        The building block for all errors.
        :param prompt: error message
        """
        self.prompt = prompt

    def __repr__(self):
        return self.prompt


class SyntaxError(BaseError): ...

