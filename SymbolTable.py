import Lexer as lx
import Error as err
import Interpreter as inp

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

    def append(self, element):
        newList = self.copy()
        newList.append(element)
        return newList

    def copy(self):
        newList = Array(self.elements[:])
        return newList

    def __repr__(self) -> str:
        return f'({self.elements})'

class SymbolTable:
    def __init__(self, parent):
        self.parent = parent
        self.variables = {}

    def add_var(self, name, value, indices):
        check = inp.RunChecker()
        if len(indices) > 0:
            check.register(self.descend_to_index(name, self.variables[name], indices, value, 0))
        else:
            self.variables[name] = value

        if check.shouldReturn():
            return check

    def descend_to_index(self, name, var, indices, value, level):
        check = inp.RunChecker()

        if indices[level] not in var.elements.keys():
            return check.failure(err.IndexOutOfBoundsError(f'{name}, index {indices[level]} for length {len(var.elements)}'))
        
        if level == len(indices) - 1:
            var.elements[indices[level]] = value
        else:
            check.register(self.descend_to_index(name, var.elements[indices[level]], indices, value, level + 1))
        
    def get_var(self, name, indices):
        check = inp.RunChecker()

        if name not in self.variables.keys():
            print("catch")
            return check.failure(err.MissingVariableError(name))
        
        var = self.variables[name]

        #the if statement is used for future implementation of a dictionary
        if isinstance(var, Array):
            for i in range(len(indices)):
                if indices[i] not in var.elements.keys():
                    return check.failure(err.IndexOutOfBoundsError(f'{name}, index {indices[i]} for length {len(var.elements)}'))
                var = var.elements[indices[i]]

        return var

    def inc_var(self, name, op):
        check = inp.RunChecker()

        if name not in self.variables.keys():
            return check.failure(err.MissingVariableError(name))
        
        if op.type == lx.typeInc:
            self.variables[name] += 1
        else:
            self.variables[name] -= 1
        
    def add_func(self, name, function):
        self.variables[name] = Function(function)

    def add_arr(self, name, array):
        dict_array = {}
        for i in range(len(array)):
            dict_array[i] = array[i]

        self.variables[name] = Array(dict_array)

    def get_func(self, name):
        check = inp.RunChecker()

        if name not in self.variables.keys():
            return check.failure(err.MissingVariableError(name))
        
        return self.variables[name]
    

    def __repr__(self):
        return f'({self.parent}, {self.variables})'