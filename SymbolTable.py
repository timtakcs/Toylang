import Lexer as lx

class Function:
    def __init__(self, node) -> None:
        self.args = node.args
        self.body = node.body

    def __repr__(self) -> str:
        return "Function" 

class SymbolTable:
    def __init__(self, parent):
        self.parent = parent
        self.variables = {}

    def addVar(self, name, value):
        self.variables[name] = value

    def getVar(self, name):
        return self.variables[name]

    def incVar(self, name, op):
        if op.type == lx.typeInc:
            self.variables[name] += 1
        else:
            self.variables[name] -= 1

    def addFunc(self, name, function):
        self.variables[name] = Function(function)

    def getFunc(self, name):
        if self.parent:
            return self.parent.variables[name]
        else:
            return self.variables[name]

    def __repr__(self):
        return f'({self.parent}, {self.variables})'