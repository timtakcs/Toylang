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
        self.length = len(elements)

    #rewrite this so that it works for a dictionary
    def append(self, element):
        newList = self.copy()
        newList.append(element)
        return newList

    def get_element(self, index):
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

    def addVar(self, name, value, indices):
        if len(indices) > 0:
            self.descend_to_index(self.variables[name], indices, value, 0)
        else:
            self.variables[name] = value

    def descend_to_index(self, var, indices, value, level):
        if level == len(indices) - 1:
            var.elements[indices[level]] = value
        else:
            self.descend_to_index(var.elements[indices[level]], indices, value, level + 1)

    def getVar(self, name, indices):
        var = self.variables[name]

        #the if statement is used for future implementation of a dictionary
        if isinstance(var, Array):
            for i in range(len(indices)):
                var = var.elements[indices[i]]

        return var

    def incVar(self, name, op):
        if op.type == lx.typeInc:
            self.variables[name] += 1
        else:
            self.variables[name] -= 1

    def addFunc(self, name, function):
        self.variables[name] = Function(function)

    def addArr(self, name, array):
        dict_array = {}
        for i in range(len(array)):
            dict_array[i] = array[i]

        self.variables[name] = Array(dict_array)

    def getFunc(self, name):
        if self.parent:
            return self.parent.variables[name]
        else:
            return self.variables[name]

    def __repr__(self):
        return f'({self.parent}, {self.variables})'