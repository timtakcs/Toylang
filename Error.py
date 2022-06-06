#Error

class Error:
    def __init__(self, name, details):
        self.details = details
        self.name = name

    def asString(self):
        message = f'{self.name}: line {self.details}\n'
        return message

class IllegalCharError(Error):
    def __init__(self, details):
        super().__init__("Illegal Char", details)

class IllegalVariableDeclaration(Error):
    def __init__(self, details):
        super().__init__("Invalid Variable Declaration", details)

class IllegalFloatError(Error):
    def __init__(self, details):
        super().__init__("Illegal Float", details)

class InvalidSyntaxError(Error):
    def __init__(self, message, details):
        super().__init__(message, details)

class InvalidString(Error):
    def __init__(self, details):
        super().__init__("String literal isn't terminated", details)

class MissingVariableError(Error):
    def __init__(self, details):
        super().__init__("Variable has not been declared", details)

class IndexOutOfBoundsError(Error):
    def __init__(self, details):
        super().__init__("Index out of bounds: ", details)