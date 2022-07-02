from ast import Pass
from multiprocessing import Condition
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
        for i in range(len(node.indices)):
            node.indices[i] = self.visit(node.indices[i])

        return self.table.getVar(node.value, node.indices)

    def visitAssignmentNode(self, node):
        check = RunChecker()
        print("fff", node.rightChild)
        self.table.addVar(node.leftChild.value, check.register(self.visit(node.rightChild)))

    def visitDoubleOpNode(self, node):
        check = RunChecker()
        #change the arguments to be visit functions
        self.table.incVar(node.var.value, node.operator)

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
            return check.register(self.visit(node.elseCase))

    def visitArrayNode(self, node):
        check = RunChecker()
        for i in range(len(node.elements)):
            node.elements[i] = check.register(self.visit(node.elements[i]))

        self.table.addArr(node.name, node.elements)

    def visitIndexNode(self, node):
        check = RunChecker()
        print(node.array)
        array = self.table.getVar(node.array.value)
        print("ff", node.index)
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
        while 1 == 1:
            if check.register(self.visit(node.condition)) == True:
                check.register(self.visit(node.body))
                if check.shouldReturn():
                    return check
            else:
                break

    def visitReturnNode(self, node):
        check = RunChecker()
        value = check.register(self.visit(node.expression))
        return check.successReturn(value)

    def visitFuncNode(self, node):
        self.table.addFunc(node.name, node)

    def execute(self, func, args, table):
        check = RunChecker()
        newTable = table
        interpreter = Interpreter(self.parser, newTable)
        argNames = func.args

        if len(argNames) != len(args):
            return f'(Function expected {len(argNames)} arguments, recieved {len(args)})'

        for i in range(len(args)):
            newTable.addVar(argNames[i].value, args[i].value.value)

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
        result = check.register(self.execute(func, args, newTable))
        return result

    def visitEmptyOpNode(self, node):
        pass

    def interpret(self):
        self.tree = self.parser.parse()
        self.visit(self.tree.node)
        return self.table