import Lexer as lx
import Error as err

class Function:
    def __init__(self, node) -> None:
        self.args = node.args
        self.body = node.body

    def __repr__(self) -> str:
        return "Function" 

class Array:
    def __init__(self, elements):
        self.elements = elements

    def append(self, element):
        newList = self.copy()
        newList.append(element)
        return newList

    def getElement(self, index):
        if isinstance(index, int):
            try:
                return self.elements[index]
            except:
                return err.IndexOutOfBoundsError(f'{index} out of bounds for length {len(self.elements)}')

    def copy(self):
        newList = Array(self.elements[:])
        return newList

    def __repr__(self) -> str:
        return f'({self.elements})'

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

    def addArr(self, name, array):
        self.variables[name] = Array(array)

    def getFunc(self, name):
        if self.parent:
            return self.parent.variables[name]
        else:
            return self.variables[name]

    def __repr__(self):
        return f'({self.parent}, {self.variables})'