from Executor import Executor
from Nonterminals.Nonterminal import Nonterminal
from Fun import Fun
from Nonterminals.DeclInt import DeclInt
from Nonterminals.DeclRef import DeclRef


class Decl(Nonterminal):
    def __init__(self, parent=None):
        super().__init__(parent)

    def parse(self, parser):
        # check if decl-int or decl-seq
        if parser.currentTok() == Fun.INT:
            # parse decl-int
            parser.parse(DeclInt(self))

        elif parser.currentTok() == Fun.REF:
            # parse decl-ref
            parser.parse(DeclRef(self))

        else:
            # end parser and print error message
            expected = [Fun.INT, Fun.REF]
            parser.endParse(expected)

    # print contents of parse tree
    def prettyPrint(self, indents=0):
        self.children[0].prettyPrint(indents)

    # check that variables are in scope and such
    def semanticCheck(self, globalS, localS, declType=""):
        return self.children[0].semanticCheck(globalS, localS)

    # add vars to scope
    def execute(self, declare=False):
        ids = self.children[0].execute()
        varType = ids[1]
        ids = ids[0]

        # add ids to scope
        for id in ids:
            # if in decl-seq, add to global
            if declare:
                Executor.scope.declareGlobal(id, varType)
            else:
                Executor.scope.declareLocal(id, varType)
