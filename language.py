from symtable import Symbol
import Lexer as lx
import Parser as prs
import Interpreter as inp
import SymbolTable as smb

#Run

def run(text):
    lexer = lx.Lexer(text)
    tokens, error = lexer.make_tokens()

    if error:
        return None, error

    parser = prs.Parser(tokens)
    interpreter = inp.Interpreter(parser, smb.SymbolTable(None))
    error, result = interpreter.interpret()

    if error:
        return None, error

    return result, interpreter.tree.error