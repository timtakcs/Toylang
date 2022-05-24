from symtable import Symbol
import Lexer as lx
import Parser as prs
import Error as err
import Interpreter as intr
import SymbolTable as smb

#Run

def run(text):
    lexer = lx.Lexer(text)
    tokens, error = lexer.makeTokens()

    if error:
        return None, error

    parser = prs.Parser(tokens)
    interpreter = intr.Interpreter(parser, smb.SymbolTable(None))
    result = interpreter.interpret()

    return result, interpreter.tree.error