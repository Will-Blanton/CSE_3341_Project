from Executor import Executor
from Fun import Fun
from Nonterminals.Formals import Formals
from Nonterminals.Nonterminal import Nonterminal
from Nonterminals.StmtSeq import StmtSeq
from Parser import Parser
from Util import indentPrint, duplicateFunctionPrint, duplicateFormalPrint


class FuncDecl(Nonterminal):
    def __init__(self, parent=None):
        super().__init__(parent)

    def parse(self, parser):
        # save id
        parser.saveTok(self, Fun.ID, "ID")

        # consume LParen
        parser.consumeTok(Fun.LPAREN)

        # consume reference
        parser.consumeTok(Fun.REF)

        # expand formals
        parser.parse(Formals(self))

        # consume RParen
        parser.consumeTok(Fun.RPAREN)

        # consume LBrace
        parser.consumeTok(Fun.LBRACE)

        # expand stmt-seq
        parser.parse(StmtSeq(self))

        # consume RBrace
        parser.consumeTok(Fun.RBRACE)

    # print contents of parse tree
    def prettyPrint(self, indents=0):
        indentPrint(indents, self.children[0])
        indentPrint(0, "(reference ")

        # print formals
        self.children[1].prettyPrint()

        print(") {")

        # print stmt-seq
        self.children[2].prettyPrint(indents + 1)

        indentPrint(indents, "}\n")

    # check that functions have unique names
    def semanticCheck(self, globalS, localS, declType=""):
        formals = self.children[1].semanticCheck(self, globalS, localS)
        formalCount = len(formals)

        result = self.children[0] not in Parser.funcDeclared.keys()
        if result:
            # save function declaration (name, parameter count)
            Parser.funcDeclared[self.children[0]] = formalCount
        else:
            duplicateFunctionPrint(self.children[0])

        # check for duplicate formals
        if formalCount != len(set(formals)):
            duplicateFormalPrint(self.children[0])
            result = False

        return result

    # declare function
    def execute(self, declare=False):
        funcName = self.children[0]
        formals = self.children[1].execute(True)

        # save function info
        Executor.functions[funcName] = formals, self.children[2]
