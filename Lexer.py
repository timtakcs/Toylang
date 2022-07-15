import Error as err

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
typeAnd = "AND"
typeOr = "OR"
typeInc = "INC"
typeDec = "DEC"
typeIncBy = "INCBY"
typeDecBy = "DECBY"
typeReturn = "RETURN"

incOps = [typeInc, typeDec, typeIncBy, typeDecBy]

#Logic operators

typeEQL = "EQLS"
typeLess = "LESS"
typeGreater = "GRTR"
typeGrtrEql = "GRTREQL"
typeLessEql = "LESSEQL"

logicOps = [typeEQL, typeLess, typeGreater, typeLessEql, typeGrtrEql]

#Built in functions
typePrint = "PRINT"
typeLength = "LENGTH"
typeAppend = "APPEND"

builtInFuncs = [typePrint, typeLength, typeAppend]

#Identifiers

typeVar = "VAR"
typeIf = "IF"
typeElif = "ELIF"
typeElse = "ELSE"
typeFunc = "FUNC"

#Loops

typeFor = "FOR"
typeWhile = "WHILE"

#Types

typeIntID = "IDINT"
typeFloatID = "IDFLOAT"
typeStringID = "IDSTRING"
typeBoolID = "IDBOOL"

types = [typeIntID, typeFloatID, typeStringID, typeBoolID]

#Separators

typeColon = "COLON"
typeLPAR = "LPAR"
typeRPAR = "RPAR"
typeLBRACE = "LBRACE"
typeRBRACE = "RBRACE"
typeLSQ = "LSQ"
typeRSQ = "RSQ"
typeSemi = "SEMI"
typeComma = "COMMA"

typeEndOfFile = "EOF"
typeStart = "START"

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

    def skip(self):
        self.pos.advance(self.currentChar)
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

#if the keywords are misspelled it can cause a whole bunch of problems
    def make_var(self, line):
        varID = ''

        while self.currentChar != None and self.currentChar.isalnum() == True or self.currentChar == "_":
            varID += self.currentChar
            self.advance()
            
        if varID.isalnum() == True:
            if varID == "if":
                return Token(typeIf, line, varID)
            elif varID == "elif":
                return Token(typeElif, line, varID)
            elif varID == "else":
                return Token(typeElse, line, varID)
            elif varID == "for":
                return Token(typeFor, line, varID)
            elif varID == "while":
                return Token(typeWhile, line, varID)
            elif varID == "func":
                return Token(typeFunc, line, varID)
            elif varID == "return":
                return Token(typeReturn, line, varID)
            elif varID == "print":
                return Token(typePrint, line, varID)
            elif varID == "len":
                return Token(typeLength, line, varID)
            elif varID == "append":
                return Token(typeAppend, line, varID)
            else:
                return Token(typeVar, line, varID)
        else:
            return None

    def make_number(self, line):
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

    def make_string(self, line):
        self.advance()

        stringToken = '' 

        while self.currentChar not in "\"":
            if self.currentChar == ";":
                return None
            stringToken += self.currentChar
            self.advance()

        return Token(typeString, line, stringToken)

    def make_tokens(self):
        tokenArray = []

        while self.currentChar != None:
            if self.currentChar in ("\t", " ", "\n"):
                self.advance()
            elif self.currentChar == "+" and self.peek() == "+":
                tokenArray.append(Token(typeInc, self.pos.line))
                self.skip()
            elif self.currentChar == "-" and self.peek() == "-":
                tokenArray.append(Token(typeDec, self.pos.line))
                self.skip()
            elif self.currentChar == "+" and self.peek() == "=":
                tokenArray.append(Token(typeIncBy, self.pos.line))
                self.skip()
            elif self.currentChar == "-" and self.peek() == "=":
                tokenArray.append(Token(typeDecBy, self.pos.line))
                self.skip()
            elif self.currentChar == "+" and self.peek() != "+":
                tokenArray.append(Token(tokenType=typePlus, line=self.pos.line))
                self.advance()
            elif self.currentChar == "-" and self.peek() != "-":
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
            elif self.currentChar == "[":
                tokenArray.append(Token(tokenType=typeLSQ, line=self.pos.line))
                self.advance()
            elif self.currentChar == "]":
                tokenArray.append(Token(tokenType=typeRSQ, line=self.pos.line))
                self.advance()
            elif self.currentChar == "{":
                tokenArray.append(Token(tokenType=typeLBRACE, line=self.pos.line))
                self.advance()
            elif self.currentChar == "}":
                tokenArray.append(Token(tokenType=typeRBRACE, line=self.pos.line))
                tokenArray.append(Token(tokenType=typeSemi, line=self.pos.line))
                self.advance()
            elif self.currentChar == ";":
                tokenArray.append(Token(tokenType=typeSemi, line=self.pos.line))
                self.advance()
            elif self.currentChar == ",":
                tokenArray.append(Token(tokenType=typeComma, line=self.pos.line))
                self.advance()
            elif self.currentChar == "\"":
                string = self.make_string(self.pos.line)
                if string != None:
                    tokenArray.append(string)
                    self.advance()
                else:
                    line = self.pos.line
                    self.advance()
                    return [], err.InvalidString(line - 1)
            elif self.currentChar in INTS:
                num = self.make_number(line=self.pos.line)
                if num != None:
                    tokenArray.append(num)
                else:
                    line = self.pos.line
                    self.advance()
                    return [], err.IllegalFloatError(line)
            elif self.currentChar.isalnum():
                var = self.make_var(self.pos.line)
                if var != None:
                    tokenArray.append(var)
                else:
                    line = self.pos.line
                    self.advance()
                    return [], err.IllegalVariableDeclaration(line)
            elif self.currentChar == "&" and self.peek() == "&":
                tokenArray.append(Token(typeAnd, self.pos.line))
                self.skip()
            elif self.currentChar == "|" and self.peek() == "|":
                tokenArray.append(Token(typeOr, self.pos.line))
                self.skip()
            elif self.currentChar == "=" and self.peek() == "=":
                tokenArray.append(Token(typeEQL, self.pos.line))
                self.skip()
            elif self.currentChar == "<" and self.peek() == "=":
                tokenArray.append(Token(typeLessEql, self.pos.line))
                self.skip()
            elif self.currentChar == ">" and self.peek() == "=":
                tokenArray.append(Token(typeGrtrEql, self.pos.line))
                self.skip()
            elif self.currentChar == "<" and self.peek() != "=":
                tokenArray.append(Token(typeLess, self.pos.line))
                self.skip()
            elif self.currentChar == ">" and self.peek() != "=":
                tokenArray.append(Token(typeGreater, self.pos.line))
                self.skip()
            elif self.currentChar == "=" and self.peek() != "=":
                tokenArray.append(Token(typeAssign, self.pos.line))
                self.skip()
            else:
                line = self.pos.line
                self.advance()
                return [], err.IllegalCharError(line)
        tokenArray.append(Token(typeEndOfFile, line = self.pos.line))
        return tokenArray, None
