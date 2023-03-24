from Fun import Fun
from Nonterminals.Assign import Assign
from Nonterminals.Decl import Decl
from Nonterminals.FuncCall import FuncCall
from Nonterminals.Nonterminal import Nonterminal
from Nonterminals.Out import Out


class Stmt(Nonterminal):
    def __init__(self, parent=None):
        super().__init__(parent)

    def parse(self, parser):
        # choose RHS
        if parser.currentTok() == Fun.ID:
            # parse assign
            parser.parse(Assign(self))
        elif parser.currentTok() == Fun.IF:
            from Nonterminals.If import If
            # parse if
            parser.parse(If(self))
        elif parser.currentTok() == Fun.WHILE:
            from Nonterminals.Loop import Loop
            # parse loop
            parser.parse(Loop(self))
        elif parser.currentTok() == Fun.WRITE:
            # parse out
            parser.parse(Out(self))
        elif parser.currentTok() == Fun.INT or parser.currentTok() == Fun.REF:
            # parse decl
            parser.parse(Decl(self))
        elif parser.currentTok() == Fun.BEGIN:
            # parse func Call
            parser.parse(FuncCall(self))
        else:
            # end parser and print error message
            parser.endParse("statement body")

    # print contents of parse tree
    def prettyPrint(self, indents=0):
        self.children[0].prettyPrint(indents)

    # check that variables are in scope and such
    def semanticCheck(self, globalS, localS, declType=""):
        return self.children[0].semanticCheck(globalS, localS)

    # execute stmt
    def execute(self, declare=False):
        self.children[0].execute()
