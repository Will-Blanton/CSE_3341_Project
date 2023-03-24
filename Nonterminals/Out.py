from Fun import Fun
from Nonterminals.Expr import Expr
from Nonterminals.Nonterminal import Nonterminal
from Util import indentPrint


class Out(Nonterminal):
    def __init__(self, parent=None):
        super().__init__(parent)

    def parse(self, parser):
        # check for and consume WRITE
        parser.consumeTok(Fun.WRITE)

        # check for and consume LPAREN
        parser.consumeTok(Fun.LPAREN)

        # parse expr
        parser.parse(Expr(self))

        # check for and consume RPAREN
        parser.consumeTok(Fun.RPAREN)

        # check for and consume SEMICOLON
        parser.consumeTok(Fun.SEMICOLON)

    # print contents of parse tree
    def prettyPrint(self, indents=0):
        indentPrint(indents, "write(")

        # print expr
        self.children[0].prettyPrint()

        print(");")

    # check that variables are in scope and such
    def semanticCheck(self, globalS, localS, declType=""):
        # check expr
        return self.children[0].semanticCheck(globalS, localS)

    # execute write
    def execute(self, declare=False):
        # print expression
        print(self.children[0].execute())
