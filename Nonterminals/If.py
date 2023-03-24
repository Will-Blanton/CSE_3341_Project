from Executor import Executor
from Fun import Fun
from Nonterminals.Cond import Cond
from Nonterminals.Nonterminal import Nonterminal
from Nonterminals.StmtSeq import StmtSeq
from Util import indentPrint


class If(Nonterminal):
    def __init__(self, parent=None):
        super().__init__(parent)

    def parse(self, parser):
        # check for and consume IF
        parser.consumeTok(Fun.IF)

        # parse cond
        parser.parse(Cond(self))

        # check for and consume THEN
        parser.consumeTok(Fun.THEN)

        # check for and consume LBRACE
        parser.consumeTok(Fun.LBRACE)

        # parse stmt-seq
        parser.parse(StmtSeq(self))

        # check for and consume RBRACE
        parser.consumeTok(Fun.RBRACE)

        # check for if else
        if parser.currentTok() == Fun.ELSE:
            parser.consumeTok(Fun.ELSE)

            # check for and consume LBRACE
            parser.consumeTok(Fun.LBRACE)

            # parse stmt-seq
            parser.parse(StmtSeq(self))

            # check for and consume RBRACE
            parser.consumeTok(Fun.RBRACE)

    # print contents of parse tree
    def prettyPrint(self, indents=0):
        indentPrint(indents, "if ")

        # print cond
        self.children[0].prettyPrint()

        indentPrint(0, " then {\n")

        # print stmt-seq
        self.children[1].prettyPrint(indents + 1)

        if len(self.children) == 3:
            indentPrint(indents, " } else {\n")
            self.children[2].prettyPrint(indents + 1)

        indentPrint(indents, " }\n")

    # check that variables are in scope and such
    def semanticCheck(self, globalS, localS, declType=""):
        # check cond
        result = self.children[0].semanticCheck(globalS, localS)

        # check stmt-seq
        nested = globalS.copy()
        nested.update(localS)
        result = result and self.children[1].semanticCheck(nested, {})

        # check else stmt-seq
        if len(self.children) == 3:
            result = result and self.children[2].semanticCheck(nested, {})

        return result

    # execute if statement
    def execute(self, declare=False):
        # enter new scope for stmt-seq
        Executor.scope.enterScope()

        # evaluate cond
        if self.children[0].execute():
            self.children[1].execute()
        elif len(self.children) == 3:
            self.children[2].execute()

        Executor.scope.exitScope()
