#Token Types

#Literals

typeInt = "INT"
typeString = "STRING"
typeFloat = "FLOAT"

#Operators

typeDivide = "DIV"
typeMultiply = "MULT"
typePlus = "PLUS"
typeMinus = "MINUS"
typeAssign = "ASSGN"
typeEQL = "EQLS"

#Identifiers

typeVar = "VAR"

#Separators

typeSemi = "SEMI"
typeColon = "COLON"
typeLPAR = "LPAR"
typeRPAR = "RPAR"
typeLine = "LINE"

typeEndOfFile = "EOF"

INTS = "0123456789"

#Token

class Token:
    def __init__(self, tokenType, line, value=None):
        self.value = value
        self.type = tokenType
        self.line = line

    def __repr__(self):
        result = f'{self.type}: {self.value}'
        return result

#Error

class Error:
    def __init__(self, name, details):
        self.details = details
        self.name = name

    def asString(self):
        message = f'{self.name}: line {self.details}\n'
        return message

class IllegalCharError(Error):
    def __init__(self, details):
        super().__init__("Illegal Char", details)

class IllegalVariableDeclaration(Error):
    def __init__(self, details):
        super().__init__("Invalid Variable Declaration", details)

class IllegalFloatError(Error):
    def __init__(self, details):
        super().__init__("Illegal Float", details)

class InvalidSyntaxError(Error):
    def __init__(self, message, details):
        super().__init__(message, details)

#Position

class Position:
    def __init__(self, index, line, column):
        self.index = index
        self.line = line
        self.column = column
    
    def advance(self, char=None):
        self.index += 1
        self.column += 1

        if char == "\n":
            self.column = 0
            self.line += 1

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
    
class StmtNode:
    pass

class CompoundStmtNode:
    pass

#Lexer

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = Position(-1, 0, -1)
        self.currentChar = None
        self.advance()

    def advance(self):
        self.pos.advance(self.currentChar)
        if self.pos.index < len(self.text):
            self.currentChar = self.text[self.pos.index]
        else:
            self.currentChar = None
    
    def peek(self):
        peekPos = self.pos.index + 1

        if peekPos > len(self.text):
            return None
        
        return self.text[peekPos]

    def makeVar(self, line):
        varID = ''

        while self.currentChar != None and self.currentChar.isalnum() == True:
            varID += self.currentChar
            self.advance()
            
        if varID.isalnum() == True:
            return Token(typeVar, line, varID)
        else:
            return None

    def makeNumber(self, line):
        numString = ""
        dotCount = 0

        while self.currentChar != None and self.currentChar in INTS + ".":
            if self.currentChar == "." and dotCount == 0:
                dotCount += 1
                numString += self.currentChar
                self.advance()
            elif self.currentChar == "." and dotCount != 0:
                return None
            else:
                numString += self.currentChar
                self.advance()

        if dotCount > 0:
            numToken = Token(typeFloat, line, float(numString))
        else:
            numToken = Token(typeInt, line, int(numString))
        
        return numToken

    def makeString(self, line):
        self.advance()

        stringToken = '' 

        while self.currentChar not in "\"":
            stringToken += self.currentChar
            self.advance()

        return Token(typeString, line, stringToken)

#GOAL FOR IMPROVEMENT: Rewrite the token identifier as a finite state machine when you add more token types
#This is too redundant

    def makeTokens(self):
        tokenArray = []

        while self.currentChar != None:
            if self.currentChar in " \t":
                self.advance()
            elif self.currentChar == "+":
                tokenArray.append(Token(tokenType=typePlus, line=self.pos.line))
                self.advance()
            elif self.currentChar == "-":
                tokenArray.append(Token(tokenType=typeMinus, line=self.pos.line))
                self.advance()
            elif self.currentChar == "*":
                tokenArray.append(Token(tokenType=typeMultiply, line=self.pos.line))
                self.advance()
            elif self.currentChar == "/":
                tokenArray.append(Token(tokenType=typeDivide, line=self.pos.line))
                self.advance()
            elif self.currentChar == "(":
                tokenArray.append(Token(tokenType=typeLPAR, line=self.pos.line))
                self.advance()
            elif self.currentChar == ")":
                tokenArray.append(Token(tokenType=typeRPAR, line=self.pos.line))
                self.advance()
            elif self.currentChar == "\"":
                tokenArray.append(self.makeString(line=self.pos.line))
                self.advance()
            elif self.currentChar in INTS:
                num = self.makeNumber(line=self.pos.line)
                if num != None:
                    tokenArray.append(num)
                else:
                    line = self.pos.line
                    self.advance()
                    return [], IllegalFloatError(line)

            elif self.currentChar.isalnum():
                var = self.makeVar(self.pos.line)
                if var != None:
                    tokenArray.append(var)
                    self.advance()
                else:
                    line = self.pos.line
                    self.advance()
                    return [], IllegalVariableDeclaration(line)

            elif self.currentChar == "=" and self.peek == "=":
                tokenArray.append(Token(typeEQL, self.pos.line))
                self.advance()
            elif self.currentChar == "=" and self.peek != "=":
                tokenArray.append(Token(typeAssign, self.pos.line))
            else:
                line = self.pos.line
                self.advance()
                return [], IllegalCharError(line)
        tokenArray.append(Token(typeEndOfFile, line = self.pos.line))
        return tokenArray, None

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

        if token.type in (typeInt, typeFloat):
            check.register(self.advance())
            return check.success(FactorNode(token))

        elif token.type == typeLPAR:
            check.register(self.advance())
            newExpression = check.register(self.expression())
            if check.error:
                return check
            if self.curToken.type == typeRPAR:
                check.register(self.advance())
                return check.success(newExpression)
            else:
                return check.failure(InvalidSyntaxError("Syntax Error: Expected )", token.line))

        return check.failure(InvalidSyntaxError("Syntax Error: Expected INT or FLOAT", token.line))

    def term(self):
        check = ParseChecker()
        left = check.register(self.factor())

        while self.curToken.type in (typeDivide, typeMultiply):
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

        while self.curToken.type in (typePlus, typeMinus):
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
        return var

    def assignment(self):
        check = ParseChecker()
        left = check.register(self.variable())

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
        pass

    def compStatement(self):
        pass

    def program(self):
        pass
           
#For the parse method I simply call the expression method because it is at the top of the inclusivity hierarchy
#factor() and term() will be called from within expression() when reached

    def parse(self):
        result = self.expression()
        if not result.error and self.curToken.type != typeEndOfFile:
            return result.failure(InvalidSyntaxError("Syntax Error: Expected an operator", self.curToken.line))
        return result

#Visiting pattern

class Visitor(object):
    def visit(self, node):
        if isinstance(node, FactorNode):
            return self.visitNumNode(node)
        elif isinstance(node, OperatorNode):
            return self.visitOpNode(node)

#Interpreter

class Interpreter(Visitor):
    def __init__(self, parser):
        self.parser = parser

    def visitOpNode(self, node):
        if node.operator.type == typePlus:
            return self.visit(node.leftChild) + self.visit(node.rightChild)
        elif node.operator.type == typeMinus:
            return self.visit(node.leftChild) - self.visit(node.rightChild)
        elif node.operator.type == typeMultiply:
            return self.visit(node.leftChild) * self.visit(node.rightChild)
        elif node.operator.type == typeDivide:
            return self.visit(node.leftChild) / self.visit(node.rightChild)

    def visitNumNode(self, node):
        return node.value.value

    def interpret(self):
        self.tree = self.parser.parse()
        return self.visit(self.tree.node)

#Run

def run(text):
    lexer = Lexer(text)
    tokens, error = lexer.makeTokens()

    if error:
        return None, error

    parser = Parser(tokens)
    interpreter = Interpreter(parser)
    result = interpreter.interpret()
    
    return result, interpreter.tree.error