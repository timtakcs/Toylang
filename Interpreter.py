from requests import delete
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
        self.error = None

    def visitOperatorNode(self, node):
        check = RunChecker()
        left = check.register(self.visit(node.leftChild))
        right = check.register(self.visit(node.rightChild))

        if check.shouldReturn():
            return check 

        if node.operator.type == lx.typePlus:
            return left + right
        elif node.operator.type == lx.typeMinus:
            if right == 0: return left
            return left - right
        elif node.operator.type == lx.typeMultiply:
            if left == 0 or right == 0: return 0
            return left * right
        elif node.operator.type == lx.typeDivide:
            if right == 0: return check.failure(err.InvalidSyntaxError("Math error, can't divide by 0", node.operator.line))
            return left / right
        elif node.operator.type == lx.typeIntDiv:
            if right == 0: return check.failure(err.InvalidSyntaxError("Math error, can't divide by 0", node.operator.line))
            return left // right

    def visitFactorNode(self, node):
        check = RunChecker()
        return check.success(node.value.value)

    def visitVariableNode(self, node):
        check = RunChecker()
        temp_indices = []

        for i in range(len(node.indices)):
            temp_indices.append(check.register(self.visit(node.indices[i])))

        return self.table.get_var(node.value, temp_indices)

    def visitAssignmentNode(self, node):
        check = RunChecker()
        temp_indices = []
        child = node.leftChild

        for i in range(len(child.indices)):
            temp_indices.append(check.register(self.visit(child.indices[i])))

        value = check.register(self.visit(node.rightChild))
        
        if check.shouldReturn():
            return check

        self.table.add_var(child.value, value, temp_indices)

    def visitDoubleOpNode(self, node):
        return self.table.inc_var(node.var.value, node.operator)

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

        left = check.register(self.visit(node.leftChild))
        right = check.register(self.visit(node.rightChild))

        if check.shouldReturn():
            return check 

        if node.operator.type == lx.typeEQL:
            return left == right
        elif node.operator.type == lx.typeLessEql:
            return left <= right
        elif node.operator.type == lx.typeGrtrEql:
            return left >= right
        elif node.operator.type == lx.typeLess:
            return left < right
        elif node.operator.type == lx.typeGreater:
            return left > right

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

        self.table.add_arr(node.name, node.elements)

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
        self.table.add_func(node.name, node)

    def execute_function(self, name, func, args, table):
        check = RunChecker()

        interpreter = Interpreter(self.parser, table)
        argNames = func.args

        if len(argNames) != len(args):
            return f'(Function expected {len(argNames)} arguments, recieved {len(args)})'

        for i in range(len(args)):
            table.add_var(argNames[i].value, check.register(self.visit(args[i])), [])

        table.add_func(name, func)

        check.register(interpreter.visit(func.body))

        if check.shouldReturn():
            return check

    def visitFuncCallNode(self, node):
        check = RunChecker()
        var_name = node.funcName.value
        func = self.table.get_func(var_name)
        args = node.args
        newTable = smb.SymbolTable(self.table)

        if 'recursion_stack_counter' not in self.table.variables:
            newTable.add_var('recursion_stack_counter', 1, [])
        else:
            if self.table.get_var('recursion_stack_counter', []) > 102:
                return check.failure(err.MaxRecursionDepthExceeded(f'function {var_name}'))
            else:
                newTable.variables['recursion_stack_counter'] = self.table.get_var('recursion_stack_counter', []) + 1

        result = check.register(self.execute_function(var_name, func, args, newTable))
        del(newTable)

        if check.shouldReturn(): return check

        return result

    def visitBuiltInFuncNode(self, node):
        check = RunChecker()
        if node.value.value == "print":
            print(check.register(self.visit(node.argument[0])))
        elif node.value.value == "len":
            var = check.register(self.visit(node.argument[0]))
            try:
                if isinstance(var, smb.Array):
                    return var.length
                elif isinstance(var, str):
                    return len(var)
            except:
                return check.failure(err.InvalidFunctionCall(f'len only takes strings or arrays as arguments, provided {type(var)}'))

        elif node.value.value == "append":
            var = check.register(self.visit(node.argument[0]))
            if isinstance(var, smb.Array):
                return self.table.add_arr(node.argument[0].append(check.register(self.visit(node.argument[1]))))
            else:
                return check.failure(err.InvalidFunctionCall(f'append takes in array and value as arguments'))

    def visitEmptyOpNode(self, node):
        pass

    def interpret(self):
        check = RunChecker()
        self.tree = self.parser.parse()

        if self.tree.error:
            return self.tree.error, None

        check.register(self.visit(self.tree.node))
        
        if check.error:
            return check.error, None

        return None, self.table