from Fun import Fun
from Nonterminals.Cmpr import Cmpr
from Nonterminals.Nonterminal import Nonterminal
from Util import indentPrint


class Cond(Nonterminal):
    def __init__(self, parent=None):
        super().__init__(parent)

    def parse(self, parser):
        # choose RHS
        if parser.currentTok() == Fun.NEGATION:
            parser.saveTok(self, Fun.NEGATION)

            # check for and consume LPAREN
            parser.consumeTok(Fun.LPAREN)

            # parse cond
            parser.parse(Cond(self))

            # check for and consume RPAREN
            parser.consumeTok(Fun.RPAREN)

        else:
            # parse cmpr
            parser.parse(Cmpr(self))

            # check for <cmpr> or <cond>
            if parser.currentTok() == Fun.OR:
                parser.consumeTok(Fun.OR)

                # parse cond
                parser.parse(Cond(self))

    # print contents of parse tree
    def prettyPrint(self, indents=0):
        # print !(cond)
        if self.children[0] == Fun.NEGATION:
            indentPrint(0, "!(")
            self.children[1].prettyPrint()
            indentPrint(0, ")")
        else:
            self.children[0].prettyPrint()

            if len(self.children) == 2:
                indentPrint(0, " or ")
                self.children[1].prettyPrint()

    # check that variables are in scope and such
    def semanticCheck(self, globalS, localS, declType=""):
        if self.children[0] == Fun.NEGATION:
            result = self.children[1].semanticCheck(globalS, localS)
        else:
            result = self.children[0].semanticCheck(globalS, localS)

            if len(self.children) == 2:
                result = result and self.children[1].semanticCheck(globalS, localS)

        return result

    # evaluate condition
    def execute(self, declare=False):
        # !(cond)
        if self.children[0] == Fun.NEGATION:
            cond = not self.children[1].execute()
        else:
            cond = self.children[0].execute()

            # cond or cond
            if len(self.children) == 2:
                cond = cond or self.children[1].execute()

        return cond
