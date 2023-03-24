from Fun import Fun
from Nonterminals.Factor import Factor
from Nonterminals.Nonterminal import Nonterminal
from Util import indentPrint


class Term(Nonterminal):
    def __init__(self, parent=None):
        super().__init__(parent)

    def parse(self, parser):
        # parse factor
        parser.parse(Factor(self))

        # check for <factor> * <term>
        if parser.currentTok() == Fun.MULT:
            # consume MULT
            parser.consumeTok(Fun.MULT)

            # parse term
            parser.parse(Term(self))

    # print contents of parse tree
    def prettyPrint(self, indents=0):
        # print factor
        self.children[0].prettyPrint(indents)

        if len(self.children) == 2:

            indentPrint(0, " * ")

            # print term
            self.children[1].prettyPrint(indents)

    # check that variables are in scope and such
    def semanticCheck(self, globalS, localS, declType=""):
        # check factor
        result = self.children[0].semanticCheck(globalS, localS)

        if len(self.children) == 2:
            # check term
            result = result and self.children[1].semanticCheck(globalS, localS)

        return result

    # evaluate term
    def execute(self, declare=False):
        # evaluate factor
        term = self.children[0].execute()
        if len(self.children) > 1:
            term2 = self.children[1].execute()
            term *= term2

        return term
