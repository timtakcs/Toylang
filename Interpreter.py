import Parser as prs
import Lexer as lx

#Visiting pattern

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

#Interpreter

class Interpreter(Visitor):
    def __init__(self, parser):
        self.parser = parser
        self.variables = {}

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
        node.value
        
    def visitAssgnNode(self, node):
        self.variables[self.visit(node.leftChild)] = self.visit(node.rightChild)
        print(self.variables)

    def visitCompNode(self, node):
        results = []

        for stmt in node.statements:
            results.append(self.visit(stmt))
        
        return results     

    def interpret(self):
        self.tree = self.parser.parse()
        return self.visit(self.tree.node)
