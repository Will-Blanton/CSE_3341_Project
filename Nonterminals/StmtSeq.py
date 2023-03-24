from Fun import Fun
from Nonterminals.Nonterminal import Nonterminal
from Nonterminals.Stmt import Stmt
from Util import indentPrint


class StmtSeq(Nonterminal):
    def __init__(self, parent=None):
        super().__init__(parent)

    def parse(self, parser):
        # parse stmt
        parser.parse(Stmt(self))

        # check for <stmt><stmt-seq>
        if parser.currentTok() != Fun.RBRACE:
            # parse stmt-seq
            parser.parse(StmtSeq(self))

    # print contents of parse tree
    def prettyPrint(self, indents=0):
        self.children[0].prettyPrint(indents)

        if len(self.children) == 2:
            self.children[1].prettyPrint(indents)

    # check that variables are in scope and such
    def semanticCheck(self, globalS, localS, declType=""):
        # check stmt
        result = self.children[0].semanticCheck(globalS, localS)

        # check stmt-seq
        if len(self.children) == 2:
            result = result and self.children[1].semanticCheck(globalS, localS)

        return result

    # execute stmt-seq, create new local scope
    def execute(self, declare=False):
        self.children[0].execute()

        if len(self.children) == 2:
            self.children[1].execute()
