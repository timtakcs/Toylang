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
    
    def __repr__(self):
        return f'({self.token}, {self.value})'

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

    def __repr__(self):
        return f'({self.statements})'

class IfNode:
    def __init__(self, cases, elseCase):
        self.cases = cases
        self.elseCase = elseCase
    
    def __repr__(self) -> str:
        return f'({self.cases}, {self.elseCase})'

class ForNode:
    def __init__(self, counter, limit, step, body):
        self.counter = counter
        self.limit = limit
        self.step = step
        self.body = body
    
    def __repr__(self):
        return f'({self.counter}, {self.limit}, {self.step}, {self.body})'

class WhileNode:
    def __init__(self, condition, body):
        pass

class LogicNode:
    def __init__(self, left, operator, right):
        self.leftChild = left
        self.rightChild = right
        self.operator = operator

    def __repr__(self):
        return f'({self.leftChild}, {self.operator}, {self.rightChild})'

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

        if token.type in (lx.typeInt, lx.typeFloat, lx.typeString):
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

        if self.curToken.type in lx.logicOps:
            left = check.register(self.logicExpression(left))

        return check.success(left)

    #TODO && and || parsing
    def logicExpression(self, left):
        check = ParseChecker()
        if check.error: 
            return check

        operator = self.curToken
        check.register(self.advance())

        right = check.register(self.expression())
        return check.success(LogicNode(left, operator, right))

    def ifExpression(self):
        check = ParseChecker()
        cases = []
        elseCase = None

        check.register(self.advance())

        condition = check.register(self.expression())
        if check.error: 
            return check

        if self.curToken.type != lx.typeLBRACE:
            return check.failure(err.InvalidSyntaxError("Invalid if statement declaration, expected {"
            , self.curToken.line))

        check.register(self.advance())
        
        if self.curToken.type == lx.typeSemi:
            check.register(self.advance())

        expression = check.register(self.compStatement())
        if check.error: 
            print("1")
            return check

        if self.curToken.type == lx.typeSemi:
            check.register(self.advance())

        if self.curToken.type != lx.typeRBRACE:
            return check.failure(err.InvalidSyntaxError("Invalid if expression declaration, expected }"
            , self.curToken.line))

        cases.append((condition, expression))
        check.register(self.advance())

        #TODO abstract this to a function so that the code is readable
        while self.curToken.type == lx.typeElif:
            check.register(self.advance())

            condition = check.register(self.expression())
            
            if self.curToken.type != lx.typeLBRACE:
                return check.failure(err.InvalidSyntaxError("Invalid elif statement declaration, expected {"
                , self.curToken.line))

            check.register(self.advance())

            expression = check.register(self.compStatement())
            if check.error: 
                return check

            if self.curToken.type != lx.typeRBRACE:
                return check.failure(err.InvalidSyntaxError("Invalid elif expression declaration, expected }"
                , self.curToken.line))

            cases.append((condition, expression))
            check.register(self.advance())
        
        #same thing as before but without the condition
        if self.curToken.type == lx.typeElse:
            check.register(self.advance())
            
            if self.curToken.type != lx.typeLBRACE:
                return check.failure(err.InvalidSyntaxError("Invalid else statement declaration, expected {"
                , self.curToken.line))

            check.register(self.advance())

            expression = check.register(self.compStatement())
            if check.error: 
                return check

            if self.curToken.type != lx.typeRBRACE:
                return check.failure(err.InvalidSyntaxError("Invalid else expression declaration, expected }"
                , self.curToken.line))

            elseCase = expression
            check.register(self.advance())

        return check.success(IfNode(cases, elseCase))

    def forExpression(self):
        check = ParseChecker()
        check.register(self.advance())

        if self.curToken.type != lx.typeLPAR:
            return check.failure(err.InvalidSyntaxError("Invalid for expression declaration, expected ("
            , self.curToken.line))

        check.register(self.advance())

        counter = check.register(self.assignment())
        if check.error:
            return check

        if self.curToken.type != lx.typeSemi:
            print(1)
            return check.failure(err.InvalidSyntaxError("Invalid for declaration, expected counter, limit, and step"
            , self.curToken.line))

        check.register(self.advance())

        limit = check.register(self.expression())
        if check.error:
            return check

        if self.curToken.type != lx.typeSemi:
            print(2)
            return check.failure(err.InvalidSyntaxError("Invalid for declaration, expected counter, limit, and step"
            , self.curToken.line))

        check.register(self.advance())

        step = check.register(self.assignment())
        if check.error:
            return check

        if self.curToken.type != lx.typeRPAR:
            return check.failure(err.InvalidSyntaxError("Expected )"
            , self.curToken.line))

        check.register(self.advance())

        if self.curToken.type != lx.typeLBRACE:
            return check.failure(err.InvalidSyntaxError("Invalid for body declaration, expected {"
            , self.curToken.line))

        check.register(self.advance())

        body = check.register(self.compStatement())
        if check.error:
            return check

        print("token = ",self.curToken)

        if self.curToken.type != lx.typeRBRACE:
            return check.failure(err.InvalidSyntaxError("Invalid for body declaration, expected }"
            , self.curToken.line))
        
        return check.success(ForNode(counter, limit, step, body))

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
        elif self.curToken.type == lx.typeIf:
            node = check.register(self.ifExpression())
            if check.error:
                return check
        elif self.curToken.type == lx.typeFor:
            node = check.register(self.forExpression())
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

        while self.curToken.type == lx.typeSemi:
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

    def parse(self):
        result = self.program()
        if not result.error and self.curToken.type != lx.typeEndOfFile:
            return result.failure(err.InvalidSyntaxError("Syntax Error: Expected an operator", self.curToken.line))
        return result