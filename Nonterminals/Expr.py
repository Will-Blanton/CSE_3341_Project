from Fun import Fun
from Nonterminals.Nonterminal import Nonterminal
from Nonterminals.Term import Term as T
from Util import indentPrint


class Expr(Nonterminal):
    def __init__(self, parent=None):
        super().__init__(parent)

    def parse(self, parser):
        # parse term
        parser.parse(T(self))

        # choose RHS
        if parser.currentTok() == Fun.ADD:
            # check for ADD and add to parse tree
            parser.saveTok(self, Fun.ADD)

            # parse expr
            parser.parse(Expr(self))

        elif parser.currentTok() == Fun.SUB:
            # check for SUB and add to parse tree
            parser.saveTok(self, Fun.SUB)

            # parse expr
            parser.parse(Expr(self))

    # print contents of parse tree
    def prettyPrint(self, indents=0):
        # print term
        self.children[0].prettyPrint(indents)
        if len(self.children) > 1:
            operator = " + "
            if self.children[1] == Fun.SUB:
                operator = " - "

            indentPrint(0, operator)

            # print expr
            self.children[2].prettyPrint(indents)

    # check that variables are in scope and such
    def semanticCheck(self, globalS, localS, declType=""):
        # check term
        result = self.children[0].semanticCheck(globalS, localS)

        result2 = True
        if len(self.children) == 2:
            # check expr
            result2 = self.children[2].semanticCheck(globalS, localS)
            
        return result and result2

    # evaluate expression
    def execute(self, declare=False):
        # evaluate term
        expr = self.children[0].execute()
        if len(self.children) > 1:
            expr2 = self.children[2].execute()

            # subtract if minus
            if self.children[1] == Fun.SUB:
                expr2 *= -1
            expr += expr2

        return expr
