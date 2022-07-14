from ast import Pass
from distutils.log import error
from multiprocessing import Condition
import string
from symtable import Symbol
import Parser as prs
import Lexer as lx
import Error as err
import SymbolTable as smb

#Visiting pattern

class Visitor(object):
    def visit(self, node):
        method_name = 'visit' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception('No visit{} method'.format(type(node).__name__))

#Run Time Result

class RunChecker:
    def __init__(self) -> None:
        self.reset()

    def reset(self):
        self.funcReturn = False
        self.error = None
        self.value = None

    def register(self, check):
        if isinstance(check, RunChecker):
            self.error = check.error
            self.funcReturn = check.funcReturn
            self.value = check.value
            return check.value
        return check

    def success(self, value):
        self.reset()
        self.value = value
        return self

    def successReturn(self, value):
        self.reset()
        self.funcReturn = True
        self.value = value
        return self

    def shouldReturn(self):
        return (self.error or self.funcReturn)

    def failure(self, error):
        self.reset()
        self.error = error
        return self

#Interpreter

class Interpreter(Visitor):
    def __init__(self, parser, table):
        self.parser = parser
        self.table = table

    def visitOperatorNode(self, node):
        check = RunChecker()
        if node.operator.type == lx.typePlus:
            return check.register(self.visit(node.leftChild)) + check.register(self.visit(node.rightChild))
        elif node.operator.type == lx.typeMinus:
            return check.register(self.visit(node.leftChild)) - check.register(self.visit(node.rightChild))
        elif node.operator.type == lx.typeMultiply:
            return check.register(self.visit(node.leftChild)) * check.register(self.visit(node.rightChild))
        elif node.operator.type == lx.typeDivide:
            return check.register(self.visit(node.leftChild)) / check.register(self.visit(node.rightChild))

    def visitFactorNode(self, node):
        check = RunChecker()
        return check.success(node.value.value)

    def visitVariableNode(self, node):
        check = RunChecker()
        temp_indices = []

        for i in range(len(node.indices)):
            temp_indices.append(check.register(self.visit(node.indices[i])))

        return self.table.getVar(node.value, temp_indices)

    def visitAssignmentNode(self, node):
        check = RunChecker()
        temp_indices = []

        for i in range(len(node.leftChild.indices)):
            temp_indices.append(check.register(self.visit(node.leftChild.indices[i])))

        self.table.addVar(node.leftChild.value, check.register(self.visit(node.rightChild)), temp_indices)

    def visitDoubleOpNode(self, node):
        check = RunChecker()
        #change the arguments to be visit functions
        check.register(self.table.incVar(node.var.value, node.operator))
        if check.shouldReturn(): return check

    #TODO write the processing for non singular or factor increments

    def visitCompoundStmtNode(self, node):
        check = RunChecker()
        results = []

        for stmt in node.statements:
            results.append(check.register(self.visit(stmt)))
            if check.shouldReturn():
                return check
        
        return check.success(results)   

    #TODO && and || interpreting
    def visitLogicNode(self, node):
        check = RunChecker()
        if node.operator.type == lx.typeEQL:
            return check.register(self.visit(node.leftChild)) == check.register(self.visit(node.rightChild))
        elif node.operator.type == lx.typeLessEql:
            return check.register(self.visit(node.leftChild)) <= check.register(self.visit(node.rightChild))
        elif node.operator.type == lx.typeGrtrEql:
            return check.register(self.visit(node.leftChild)) >= check.register(self.visit(node.rightChild))
        elif node.operator.type == lx.typeLess:
            return check.register(self.visit(node.leftChild)) < check.register(self.visit(node.rightChild))
        elif node.operator.type == lx.typeGreater:
            return check.register(self.visit(node.leftChild)) > check.register(self.visit(node.rightChild))

    def visitIfNode(self, node):
        check = RunChecker()
        for condition, expr in node.cases:
            if check.register(self.visit(condition)) == True:
                expr = check.register(self.visit(expr))
                if check.shouldReturn():
                    return check
                else:
                    return check.success(expr)
        if node.elseCase != None:
            else_expr = check.register(self.visit(node.elseCase))
            if check.shouldReturn():
                return check
            else:
                return check.success(else_expr)

    def visitArrayNode(self, node):
        check = RunChecker()
        for i in range(len(node.elements)):
            node.elements[i] = check.register(self.visit(node.elements[i]))

        self.table.addArr(node.name, node.elements)

    def visitIndexNode(self, node):
        check = RunChecker()
        array = self.table.getVar(node.array.value)
        return check.register(self.visit(array.elements[check.register(self.visit(node.index))]))

    def visitForNode(self, node):
        check = RunChecker()
        check.register(self.visit(node.counter))

        while check.register(self.visit(node.limit)) == True:
            check.register(self.visit(node.body))
            if check.shouldReturn():
                return check
            check.register(self.visit(node.step))

    def visitWhileNode(self, node):
        check = RunChecker()
        
        while check.register(self.visit(node.condition)) == True:
            check.register(self.visit(node.body))
            if check.shouldReturn():
                return check

    def visitReturnNode(self, node):
        check = RunChecker()
        value = check.register(self.visit(node.expression))
        return check.successReturn(value)

    def visitFuncNode(self, node):
        self.table.addFunc(node.name, node)

    def execute(self, name, func, args, table):
        check = RunChecker()
        newTable = table
        interpreter = Interpreter(self.parser, newTable)
        argNames = func.args

        if len(argNames) != len(args):
            return f'(Function expected {len(argNames)} arguments, recieved {len(args)})'

        for i in range(len(args)):
            newTable.addVar(argNames[i].value, check.register(self.visit(args[i])), [])

        newTable.addFunc(name, func)

        check.register(interpreter.visit(func.body))

        if check.shouldReturn():
            return check

        return newTable

    def visitFuncCallNode(self, node):
        check = RunChecker()
        varName = node.funcName.value
        func = self.table.getFunc(varName)
        args = node.args
        newTable = smb.SymbolTable(self.table)
        result = check.register(self.execute(varName, func, args, newTable))
        return result

    def visitBuiltInFuncNode(self, node):
        check = RunChecker()
        if node.value.value == "print":
            print(check.register(self.visit(node.argument[0])))
        elif node.value.value == "len":
            var = check.register(self.visit(node.argument[0]))
            if isinstance(var, smb.Array):
                return var.length
            elif isinstance(var, string):
                return len(var)
            else:
                print("error handling code")
        elif node.value.value == "append":
            var = check.register(self.visit(node.argument[0]))
            if not isinstance(var, smb.Array):
                print("error handling code")
            else:
                self.table.addArr(node.argument[0].append(check.register(self.visit(node.argument[1]))))
        
    def visitEmptyOpNode(self, node):
        pass

    def interpret(self):
        check = RunChecker()
        self.tree = self.parser.parse()
        if self.tree.error:
            return error
        check.register(self.visit(self.tree.node))

        if check.error:
            print("fff")
            return check

        return self.table