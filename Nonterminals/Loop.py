from Executor import Executor
from Fun import Fun
from Nonterminals.Cond import Cond
from Nonterminals.Nonterminal import Nonterminal
from Nonterminals.StmtSeq import StmtSeq
from Util import indentPrint


class Loop(Nonterminal):
    def __init__(self, parent=None):
        super().__init__(parent)

    def parse(self, parser):
        # check for and consume while
        parser.consumeTok(Fun.WHILE)

        # parse cond
        parser.parse(Cond(self))

        # check for and consume LBRACE
        parser.consumeTok(Fun.LBRACE)

        # parse stmt-seq
        parser.parse(StmtSeq(self))

        # check for and consume RBRACE
        parser.consumeTok(Fun.RBRACE)

    # print contents of parse tree
    def prettyPrint(self, indents=0):
        indentPrint(indents, "while ")

        # print cond
        self.children[0].prettyPrint()

        indentPrint(0, " {\n")

        # print stmt-seq
        self.children[1].prettyPrint(indents + 1)

        indentPrint(indents, " }\n")

    # check that variables are in scope and such
    def semanticCheck(self, globalS, localS, declType=""):
        # check cond
        result = self.children[0].semanticCheck(globalS, localS)

        nested = globalS.copy()
        nested.update(localS)

        # check stmt-seq
        return result and self.children[1].semanticCheck(nested, {})

    # execute while loop
    def execute(self, declare=False):
        executor = Executor.get_instance()

        # enter new scope for stmt-seq
        executor.scope.enterScope()

        while self.children[0].execute():
            # execute stmt loop
            self.children[1].execute()

        executor.scope.exitScope()
