# def ifExpression(self):
#         check = ParseChecker()
#         cases = []
#         elseCase = None

#         check.register(self.advance())

#         condition = check.register(self.logicExpression())
#         print(self.curToken)
#         if check.error: 
#             print("1")
#             return check

#         if self.curToken.type != lx.typeLBRACE:
#             return check.failure(err.InvalidSyntaxError("Invalid if statement declaration, expected {"
#             , self.curToken.line))

#         check.register(self.advance())
        
#         if self.curToken.type == lx.typeLine:
#             check.register(self.advance())

#         expression = check.register(self.expression())
#         if check.error: 
#             print("1")
#             return check

#         if self.curToken.type != lx.typeRBRACE:
#             return check.failure(err.InvalidSyntaxError("Invalid if expression declaration, expected }"
#             , self.curToken.line))

#         cases.append((condition, expression))
#         check.register(self.advance())

#         #inside this loop is the same code as the if statement parsin
#         #TODO abstract this to a function so that the code is readable
#         while self.curToken.type == lx.typeElif:
#             check.register(self.logicExpression())
#             check.register(self.advance())
            
#             if self.curToken.type != lx.typeLBRACE:
#                 return check.failure(err.InvalidSyntaxError("Invalid elif statement declaration, expected {"
#                 , self.curToken.line))

#             check.register(self.advance())

#             if self.curToken.type == lx.typeLine:
#                 check.register(self.advance())

#             expression = check.register(self.logicExpression())
#             if check.error: 
#                 print("1")
#                 return check

#             if self.curToken.type != lx.typeRBRACE:
#                 return check.failure(err.InvalidSyntaxError("Invalid elif expression declaration, expected }"
#                 , self.curToken.line))

#             cases.append((condition, expression))
#             check.register(self.advance())
        
#         #same thing as before
#         if self.curToken.type == lx.typeElse:
#             check.register(self.advance())
            
#             if self.curToken.type != lx.typeLBRACE:
#                 return check.failure(err.InvalidSyntaxError("Invalid else statement declaration, expected {"
#                 , self.curToken.line))

#             check.register(self.advance())
#             if self.curToken.type == lx.typeLine:
#                 check.register(self.advance())

#             expression = check.register(self.expression())
#             if check.error: 
#                 print("1")
#                 return check

#             if self.curToken.type != lx.typeRBRACE:
#                 return check.failure(err.InvalidSyntaxError("Invalid else expression declaration, expected }"
#                 , self.curToken.line))

#             elseCase = (condition, expression)
#             check.register(self.advance())

#         return check.success(IfNode(cases, elseCase))

