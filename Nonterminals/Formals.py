from Executor import Executor
from Fun import Fun
from Nonterminals.Nonterminal import Nonterminal
from Util import indentPrint


class Formals(Nonterminal):
    def __init__(self, parent=None):
        super().__init__(parent)

    def parse(self, parser):
        # save id
        parser.saveTok(self, Fun.ID, "ID")

        # check for id, <formals>
        if parser.currentTok() == Fun.COMMA:
            parser.consumeTok(Fun.COMMA)

            # expand formals
            parser.parse(Formals(self))

    # print contents of parse tree
    def prettyPrint(self, indents=0):
        indentPrint(0, self.children[0])

        if len(self.children) == 2:
            indentPrint(0, ", ")
            self.children[1].prettyPrint()

    # check that variables are in scope and such
    def semanticCheck(self, globalS, localS, declType=""):
        # count formals
        formals = [self.children[0]]

        if len(self.children) == 2:
            formals += self.children[1].semanticCheck(self, globalS, localS)

        return formals

    # save formalss
    def execute(self, declare=False):
        if declare:
            # save formal id for func declaration
            formals = [self.children[0]]
        else:
            # copy formal values for function call
            fId = self.children[0]
            formals = [(fId, Executor.get_instance().scope.getRefValue(fId))]

        if len(self.children) == 2:
            formals += self.children[1].execute(declare)

        # return formal param ids
        return formals
