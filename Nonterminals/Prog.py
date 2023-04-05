from Executor import Executor
from Nonterminals.Nonterminal import Nonterminal
from Fun import Fun
from Nonterminals.DeclSeq import DeclSeq
from Nonterminals.StmtSeq import StmtSeq
from Util import indentPrint


class Prog(Nonterminal):
    def __init__(self, parent=None):
        super().__init__(parent)

    def parse(self, parser):
        # check for and consume PROGRAM
        parser.consumeTok(Fun.PROGRAM)

        # check for and consume LBRACE
        parser.consumeTok(Fun.LBRACE)

        # check if decl-seq is next
        tok = parser.currentTok()
        if tok == Fun.INT or tok == Fun.REF or tok == Fun.ID:
            # parse decl-seq
            parser.parse(DeclSeq(self))

        # check for and consume BEGIN
        parser.consumeTok(Fun.BEGIN)

        # check for and consume LBRACE
        parser.consumeTok(Fun.LBRACE)

        # parse stmt-seq
        parser.parse(StmtSeq(self))

        # check for and consume RBRACE
        parser.consumeTok(Fun.RBRACE)

        # check for and consume RBRACE
        parser.consumeTok(Fun.RBRACE)

        # check for EOS
        parser.consumeTok(Fun.EOS)

    # print contents of parse tree
    def prettyPrint(self, indents=0):
        print("program {")

        stmtIndex = 0

        # check for <decl-seq>
        if len(self.children) == 2:
            self.children[0].prettyPrint(1)
            stmtIndex = 1

        indentPrint(0, "begin {\n")

        self.children[stmtIndex].prettyPrint(1)

        print("}}")

    # check that variables are in scope and such
    def semanticCheck(self, globalS, localS, declType=""):
        stmtIndex = 0
        result = True

        # check decl-seq
        if len(self.children) == 2:
            result = self.children[0].semanticCheck(globalS, localS)
            stmtIndex = 1

        # check stmt-seq
        result2 = self.children[stmtIndex].semanticCheck(globalS, {})

        return result and result2

    # execute program
    def execute(self, declare=False):
        stmtIndex = 0

        # check decl-seq
        if len(self.children) == 2:
            self.children[0].execute()
            stmtIndex = 1

        executor = Executor.get_instance()

        # enter new scope for stmt-seq
        executor.scope.enterScope()

        # check stmt-seq
        self.children[stmtIndex].execute()

        executor.scope.exitScope()
