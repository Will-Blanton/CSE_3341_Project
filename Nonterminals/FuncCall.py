from Executor import Executor
from Fun import Fun
from Nonterminals.Nonterminal import Nonterminal
from Parser import Parser
from Util import indentPrint, noTargetPrint


class FuncCall(Nonterminal):
    def __init__(self, parent=None):
        super().__init__(parent)

    def parse(self, parser):
        parser.consumeTok(Fun.BEGIN)

        # save id
        parser.saveTok(self, Fun.ID, "ID")
        parser.consumeTok(Fun.LPAREN)

        # expand formals
        from Nonterminals.Formals import Formals
        parser.parse(Formals(self))

        parser.consumeTok(Fun.RPAREN)
        parser.consumeTok(Fun.SEMICOLON)

    # print contents of parse tree
    def prettyPrint(self, indents=0):
        indentPrint(indents, "begin ")

        # print id
        indentPrint(0, self.children[0])
        indentPrint(0, "(")

        # print formals
        self.children[1].prettyPrint()

        print(");")

    # check that function call has a target
    def semanticCheck(self, globalS, localS, declType=""):
        result = True
        formals = self.children[1].semanticCheck(globalS, localS)
        if (self.children[0], formals) not in Parser.funcDeclared.items():
            noTargetPrint(self.children[0], formals)
            result = False

        return result

    # execute function call
    def execute(self, declare=False):

        # returns pairs of formal id and their heap index in the current scope
        actuals = self.children[1].execute()

        Executor.scope.enterFrame()

        function = Executor.functions[self.children[0]]
        formals = function[0]

        # copy values in
        for i in range(0, len(actuals)):
            Executor.scope.declareLocal(formals[i], "ref")
            Executor.scope.copyRef(formals[i], actuals[i][1], rIndex=True)

        # execute stmt-seq
        function[1].execute()

        # save final values of formal params
        finalVals = []
        for f in formals:
            finalVals.append(Executor.scope.getRefValue(f))

        Executor.scope.exitFrame()

        # copy values out
        for i in range(0, len(actuals)):
            Executor.scope.copyRef(actuals[i][0], finalVals[i], rIndex=True)
