from Nonterminals.Nonterminal import Nonterminal
from Fun import Fun
from Nonterminals.IdList import IdList
from Util import indentPrint


class DeclRef(Nonterminal):
    def __init__(self, parent=None):
        super().__init__(parent)

    def parse(self, parser):
        # check for and consume INT
        parser.consumeTok(Fun.REF)

        # parse id-list
        parser.parse(IdList(self))

        # check for and consume SEMICOLON
        parser.consumeTok(Fun.SEMICOLON)

    # print contents of parse tree
    def prettyPrint(self, indents=0):
        indentPrint(indents, "reference ")
        self.children[0].prettyPrint()
        indentPrint(0, ";\n")

    # check that variables are in scope and such
    def semanticCheck(self, globalS, localS, declType=""):
        return self.children[0].semanticCheck(globalS, localS, "reference")

    # return ids for decl to add to scope
    def execute(self, declare=False):
        ids = self.children[0].execute()
        return ids, "ref"
