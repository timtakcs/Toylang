import Lexer as lx
import Parser as prs
import Error as err
import Interpreter as intr

#Run

def run(text):
    lexer = lx.Lexer(text)
    tokens, error = lexer.makeTokens()

    if error:
        return None, error

    parser = prs.Parser(tokens)
    interpreter = intr.Interpreter(parser)
    result = interpreter.interpret()
    
    return result, interpreter.tree.error