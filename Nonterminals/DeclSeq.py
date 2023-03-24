from Nonterminals.FuncDecl import FuncDecl
from Nonterminals.Nonterminal import Nonterminal
from Fun import Fun
from Nonterminals.Decl import Decl
from Util import indentPrint


class DeclSeq(Nonterminal):
    def __init__(self, parent=None):
        super().__init__(parent)

    def parse(self, parser):
        # parse decl or func-decl
        if parser.currentTok() == Fun.ID:
            parser.parse(FuncDecl(self))
        else:
            parser.parse(Decl(self))

        # check if another decl-seq is next
        tok = parser.currentTok()
        if tok == Fun.INT or tok == Fun.REF or tok == Fun.ID:
            # parse decl-seq
            parser.parse(DeclSeq(self))

    # print contents of parse tree
    def prettyPrint(self, indents=0):
        self.children[0].prettyPrint(indents)

        if len(self.children) == 2:
            self.children[1].prettyPrint(indents)

    # check that variables are in scope and such
    def semanticCheck(self, globalS, localS, declType=""):
        # check decl
        result = self.children[0].semanticCheck(localS, globalS)

        # check decl-seq
        if len(self.children) == 2:
            result = result and self.children[1].semanticCheck(globalS, localS)

        return result

    # add vars to global scope
    def execute(self, declare=False):
        self.children[0].execute(True)

        # check decl-seq
        if len(self.children) == 2:
            self.children[1].execute()
