from Fun import Fun
from Nonterminals.Expr import Expr
from Nonterminals.Nonterminal import Nonterminal
from Util import indentPrint


class Cmpr(Nonterminal):
    def __init__(self, parent=None):
        super().__init__(parent)

    def parse(self, parser):
        # parser expr
        parser.parse(Expr(self))

        # check for and add cmpr symbol to parse tree or handle error
        if parser.currentTok() == Fun.EQUAL or parser.currentTok() == Fun.LESS or parser.currentTok() == Fun.LESSEQUAL:
            parser.saveTok(self, parser.currentTok())
        else:
            # end parser and print error message
            expected = [Fun.EQUAL, Fun.LESS, Fun.LESSEQUAL]
            parser.endParse(expected)

        # parser expr
        parser.parse(Expr(self))

    # print contents of parse tree
    def prettyPrint(self, indents=0):
        # print expr
        self.children[0].prettyPrint()

        operator = " <= "
        if self.children[1] == Fun.EQUAL:
            operator = " == "
        elif self.children[1] == Fun.LESS:
            operator = " < "

        indentPrint(0, operator)

        # print expr
        self.children[2].prettyPrint()

    # check that variables are in scope and such
    def semanticCheck(self, globalS, localS, declType=""):
        # check expr
        result = self.children[0].semanticCheck(globalS, localS)

        # check expr2
        result2 = self.children[2].semanticCheck(globalS, localS)
        return result and result2

    # print contents of parse tree
    def execute(self, declare=False):

        # evaluate expressions
        expr1 = self.children[0].execute()
        expr2 = self.children[2].execute()

        if self.children[1] == Fun.EQUAL:
            cmpr = expr1 == expr2
        elif self.children[1] == Fun.LESS:
            cmpr = expr1 < expr2
        else:
            cmpr = expr1 <= expr2

        return cmpr
