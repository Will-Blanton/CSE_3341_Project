from Executor import Executor
from Fun import Fun
from Nonterminals.Expr import Expr
from Nonterminals.Nonterminal import Nonterminal
from Util import indentPrint, noScopePrint, incompatibleTypePrint


class Assign(Nonterminal):
    def __init__(self, parent=None):
        super().__init__(parent)

    def parse(self, parser):
        # check for ID and add to parse tree
        parser.saveTok(self, Fun.ID, "ID")

        # check for and consume ASSIGN
        parser.consumeTok(Fun.ASSIGN)

        # choose RHS
        if parser.currentTok() == Fun.NEW:
            # check for and add NEW to parse tree
            parser.saveTok(self, Fun.NEW)

            # check for and consume INSTANCE
            parser.consumeTok(Fun.INSTANCE)

        elif parser.currentTok() == Fun.SHARE:
            # check for and add SHARE to parse tree
            parser.saveTok(self, Fun.SHARE)

            # check for ID and add to parse tree
            parser.saveTok(self, Fun.ID, "ID")

        else:
            # parse expr
            parser.parse(Expr(self))

        # check for and consume SEMICOLON
        parser.consumeTok(Fun.SEMICOLON)

    # print contents of parse tree
    def prettyPrint(self, indents=0):
        # print ID
        indentPrint(indents, self.children[0] + " = ")

        # determine RHS
        if self.children[1] == Fun.NEW:
            indentPrint(0, "new inst")
        elif self.children[1] == Fun.SHARE:
            indentPrint(0, "share " + self.children[2])
        else:
            self.children[1].prettyPrint()

        print(";")

    # check that variables are in scope and such
    def semanticCheck(self, globalS, localS, declType=""):
        result = True
        properType = "reference"

        # check if ID is in scope
        scope = globalS.copy()
        scope.update(localS)

        if self.children[0] not in scope:
            noScopePrint(self.children[0])
            result = False
        else:
            # determine RHS
            if self.children[1] == Fun.NEW or self.children[1] == Fun.SHARE:
                # check if id proper type
                if scope[self.children[0]] != properType:
                    incompatibleTypePrint(self.children[0], properType)
                    result = False

                # check for id2 and if it is proper type
                if self.children[1] == Fun.SHARE:
                    if self.children[2] not in scope:
                        noScopePrint(self.children[2])
                        result = False
                    else:
                        if scope[self.children[2]] != properType:
                            incompatibleTypePrint(self.children[2], properType)
                            result = False

            else:
                # check expr
                result = result and self.children[1].semanticCheck(globalS, localS)

        return result

    # evaluate assign
    def execute(self, declare=False):
        executor = Executor.get_instance()

        # determine RHS
        if self.children[1] == Fun.NEW:
            # allocate on heap
            executor.scope.initRef(self.children[0])
        elif self.children[1] == Fun.SHARE:
            # copy ref value
            executor.scope.copyRef(self.children[0], self.children[2])
        else:
            # evaluate expr and store in id
            exprVal = self.children[1].execute()
            executor.scope.assignInt(self.children[0], exprVal)
