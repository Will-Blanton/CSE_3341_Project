from Nonterminals.Nonterminal import Nonterminal
from Fun import Fun
from Util import indentPrint, doublyDeclaredPrint


class IdList(Nonterminal):
    def __init__(self, parent=None):
        super().__init__(parent)

    def parse(self, parser):
        # check for ID and add to parse tree
        parser.saveTok(self, Fun.ID, "ID")

        # check if id, id-list
        if parser.currentTok() == Fun.COMMA:
            # consume COMMA
            parser.consumeTok(Fun.COMMA)

            # parse id-list
            parser.parse(IdList(self))

    # print contents of parse tree
    def prettyPrint(self, indents=0):
        indentPrint(0, self.children[0])

        if len(self.children) == 2:
            indentPrint(0, ", ")
            self.children[1].prettyPrint()

    # check that variables are in scope and such
    def semanticCheck(self, globalS, localS, declType=""):
        # check if ID is already declared in local scope
        result = not self.children[0] in localS
        if result:
            # add ID to scope
            localS[self.children[0]] = declType
        else:
            doublyDeclaredPrint(self.children[0])

        # check <id-list>
        if len(self.children) == 2:
            result = result and self.children[1].semanticCheck(globalS, localS, declType)

        return result

    # add vars to scope
    def execute(self, declare=False):
        ids = [self.children[0]]

        if len(self.children) == 2:
            ids += self.children[1].execute()

        return ids
