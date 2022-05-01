import Lexer as lx
import Error as err

#Syntax Tree Nodes

class FactorNode:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f'{self.value}'

class OperatorNode:
    def __init__(self, leftChild, operator, rightChild):
        self.leftChild = leftChild
        self.rightChild = rightChild
        self.operator = operator

    def __repr__(self):
        return f'({self.leftChild}, {self.operator}, {self.rightChild})'

class VariableNode:
    def __init__(self, token):
        self.token = token
        self.value = token.value

class AssignmentNode:
    def __init__(self, name, operator, expression):
        self.leftChild = name
        self.operator = operator
        self.rightChild = expression

    def __repr__(self):
        return f'({self.leftChild}, {self.operator}, {self.rightChild})'

class CompoundStmtNode:
    def __init__(self):
        self.statements = []

class EmptyOpNode:
    pass

#Parse Checker

class ParseChecker:
    def __init__(self):
        self.error = None
        self.node = None

    def register(self, res):
        if isinstance(res, ParseChecker):
            if res.error:
                self.error = res.error
            return res.node
        return res

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        self.error = error
        return self
    
#Parser

class Parser:
    def __init__(self, tokenArray):
        self.tokenArray = tokenArray
        self.pos = -1
        self.advance()
    
    def advance(self):
        self.pos += 1
        if self.pos < len(self.tokenArray):
            self.curToken = self.tokenArray[self.pos]
        return self.curToken

    def factor(self):
        check = ParseChecker()
        token = self.curToken

        if token.type in (lx.typeInt, lx.typeFloat):
            check.register(self.advance())
            return check.success(FactorNode(token))

        elif token.type == lx.typeLPAR:
            check.register(self.advance())
            newExpression = check.register(self.expression())
            if check.error:
                return check
            if self.curToken.type == lx.typeRPAR:
                check.register(self.advance())
                return check.success(newExpression)
            else:
                return check.failure(err.InvalidSyntaxError("Syntax Error: Expected )", token.line))

        else:
            node = check.register(self.variable())
            check.register(self.advance())

            if check.error:
                return check

            return check.success(node)

    def term(self):
        check = ParseChecker()
        left = check.register(self.factor())

        while self.curToken.type in (lx.typeDivide, lx.typeMultiply):
            operator = self.curToken
            check.register(self.advance())
            right = check.register(self.factor())
            left = OperatorNode(left, operator, right)

        return check.success(left)

    def expression(self):
        check = ParseChecker()
        left = check.register(self.term())

        if check.error:
            return check

        while self.curToken.type in (lx.typePlus, lx.typeMinus):
            operator = self.curToken
            check.register(self.advance())
            right = check.register(self.term())
            if check.error:
                return check
            left = OperatorNode(left, operator, right)
        return check.success(left)

    def variable(self):
        check = ParseChecker()
        var = check.register(VariableNode(self.curToken))
        return check.success(var)

    def assignment(self):
        check = ParseChecker()
        left = check.register(self.variable())
        check.register(self.advance())

        if check.error:
            return check

        operator = self.curToken
        check.register(self.advance())
        right = check.register(self.expression())
        if check.error:
            return check

        left = AssignmentNode(left, operator, right)

        return check.success(left)

    def statement(self):
        check = ParseChecker()

        if self.curToken.type == lx.typeVar:
            node = check.register(self.assignment())
            if check.error:
                return check
        elif self.curToken.type in (lx.typeInt, lx.typeFloat):
            node = check.register(self.expression())
            if check.error:
                return check
        else:
            node = check.register(self.empty())
            if check.error:
                return check

        return check.success(node)

    def statementList(self):
        check = ParseChecker()

        if check.error:
            return check

        statements = []

        statements.append(check.register(self.statement()))

        while self.curToken.type == lx.typeLine:
            check.register(self.advance())
            statements.append(check.register(self.statement()))
            if check.error:
                return check

        return statements

    def compStatement(self):
        check = ParseChecker()
        nodes = check.register(self.statementList())

        if check.error:
            return check

        rootStmtNode = CompoundStmtNode()

        for node in nodes:
            rootStmtNode.statements.append(node)

        return check.success(rootStmtNode)

    def program(self):
        check = ParseChecker()

        node = check.register(self.compStatement())
        check.register(self.advance())

        if check.error:
            return check

        return check.success(node)

    def empty(self):
        return EmptyOpNode()
           
#For the parse method I simply call the expression method because it is at the top of the inclusivity hierarchy
#factor() and term() will be called from within expression() when reached
#This is called recursive descent

    def parse(self):
        result = self.program()
        if not result.error and self.curToken.type != lx.typeEndOfFile:
            return result.failure(err.InvalidSyntaxError("Syntax Error: Expected an operator", self.curToken.line))
        return result