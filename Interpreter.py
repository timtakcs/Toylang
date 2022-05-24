from ast import Pass
from multiprocessing import Condition
from symtable import Symbol
import Parser as prs
import Lexer as lx
import Error as err
import SymbolTable as smb

#Visiting pattern
#this is awful - do some string concetenation for functions
class Visitor(object):
    def visit(self, node):
        if isinstance(node, prs.FactorNode):
            return self.visitNumNode(node)
        elif isinstance(node, prs.OperatorNode):
            return self.visitOpNode(node)
        elif isinstance(node, prs.CompoundStmtNode):
            return self.visitCompNode(node)
        elif isinstance(node, prs.AssignmentNode):
            return self.visitAssgnNode(node)
        elif isinstance(node, prs.VariableNode):
            return self.visitVarNode(node)
        elif isinstance(node, prs.IfNode):
            return self.visitIfNode(node)
        elif isinstance(node, prs.LogicNode):
            return self.visitLogicNode(node)
        elif isinstance(node, prs.ForNode):
            return self.visitForNode(node)
        elif isinstance(node, prs.WhileNode):
            return self.visitWhileNode(node)
        elif isinstance(node, prs.DoubleOpNode):
            return self.visitDoubleOpNode(node)
        elif isinstance(node, prs.FuncNode):
            return self.visitFuncNode(node)
        elif isinstance(node, prs.FuncCallNode):
            return self.visitFuncCallNode(node)

#Interpreter

class Interpreter(Visitor):
    def __init__(self, parser, table):
        self.parser = parser
        self.table = table

    def visitOpNode(self, node):
        if node.operator.type == lx.typePlus:
            return self.visit(node.leftChild) + self.visit(node.rightChild)
        elif node.operator.type == lx.typeMinus:
            return self.visit(node.leftChild) - self.visit(node.rightChild)
        elif node.operator.type == lx.typeMultiply:
            return self.visit(node.leftChild) * self.visit(node.rightChild)
        elif node.operator.type == lx.typeDivide:
            return self.visit(node.leftChild) / self.visit(node.rightChild)

    def visitNumNode(self, node):
        return node.value.value

    def visitVarNode(self, node):
        if self.table.getVar(node.value) == None:
            return None, err.MissingVariableError(node.token.line)
        return self.table.getVar(node.value)
        
    def visitAssgnNode(self, node):
        self.table.addVar(node.leftChild.value, self.visit(node.rightChild))

    def visitDoubleOpNode(self, node):
        self.table.incVar(node.var.value, node.operator)

    #TODO write the processing for non singular or factor increments

    def visitCompNode(self, node):
        results = []

        for stmt in node.statements:
            results.append(self.visit(stmt))
        
        return results     

    #TODO && and || interpreting
    def visitLogicNode(self, node):
        if node.operator.type == lx.typeEQL:
            return self.visit(node.leftChild) == self.visit(node.rightChild)
        elif node.operator.type == lx.typeLessEql:
            return self.visit(node.leftChild) <= self.visit(node.rightChild)
        elif node.operator.type == lx.typeGrtrEql:
            return self.visit(node.leftChild) >= self.visit(node.rightChild)
        elif node.operator.type == lx.typeLess:
            return self.visit(node.leftChild) < self.visit(node.rightChild)
        elif node.operator.type == lx.typeGreater:
            return self.visit(node.leftChild) > self.visit(node.rightChild)

    def visitIfNode(self, node):
        for condition, expr in node.cases:
            if self.visit(condition) == True:
                return self.visit(expr)
        if node.elseCase != None:
            return self.visit(node.elseCase)

    def visitForNode(self, node):
        self.visit(node.counter)

        while self.visit(node.limit) == True:
            self.visit(node.body)
            self.visit(node.step)

    def visitWhileNode(self, node):
        while 1 == 1:
            if self.visit(node.condition) == True:
                self.visit(node.body)
            else:
                break

    def visitFuncNode(self, node):
        self.table.addFunc(node.name, node)

    def execute(self, func, args, table):
        newTable = table
        interpreter = Interpreter(self.parser, newTable)
        argNames = func.args

        if len(argNames) != len(args):
            return f'(Function expected {len(argNames)} arguments, recieved {len(args)})'

        for i in range(len(args)):
            newTable.addVar(argNames[i].value, args[i].value.value)

        return interpreter.visit(func.body)

    def visitFuncCallNode(self, node):
        func = self.table.getFunc(node.funcName.value)
        args = node.args
        newTable = smb.SymbolTable(self.table)
        result = self.execute(func, args, newTable)
        print(newTable)
        return result

    def interpret(self):
        self.tree = self.parser.parse()
        self.visit(self.tree.node)
        return self.table
