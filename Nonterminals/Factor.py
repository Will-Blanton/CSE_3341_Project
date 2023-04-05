from Executor import Executor
from Fun import Fun
from Nonterminals.Nonterminal import Nonterminal
from Util import indentPrint, noScopePrint


class Factor(Nonterminal):
    def __init__(self, parent=None):
        super().__init__(parent)

    def parse(self, parser):
        # choose RHS
        if parser.currentTok() == Fun.ID:
            # add ID to parse tree
            parser.saveTok(self, Fun.ID, "ID")

        elif parser.currentTok() == Fun.CONST:
            # add CONST to parse tree
            parser.saveTok(self, Fun.CONST, "CONST")

        elif parser.currentTok() == Fun.LPAREN:
            # add LPAREN to parse tree
            parser.saveTok(self, Fun.LPAREN)

            # avoid circular imports
            from Nonterminals.Expr import Expr

            # parse expr
            parser.parse(Expr(self))

            # consume RPAREN
            parser.consumeTok(Fun.RPAREN)

        elif parser.currentTok() == Fun.READ:
            # add READ to parse tree
            parser.saveTok(self, Fun.READ)

            # consume LPAREN
            parser.consumeTok(Fun.LPAREN)

            # consume RPAREN
            parser.consumeTok(Fun.RPAREN)

        else:
            # end parser and print error message
            expected = [Fun.ID, Fun.CONST, Fun.LPAREN, Fun.READ]
            parser.endParse(expected)

    # print contents of parse tree
    def prettyPrint(self, indents=0):
        # determine RHS
        if self.children[0] == Fun.READ:
            indentPrint(0, "read()")

        elif self.children[0] == Fun.LPAREN:
            indentPrint(0, "(")

            # print expr
            self.children[1].prettyPrint()

            indentPrint(0, ")")
        else:
            indentPrint(0, self.children[0])

    # check that variables are in scope and such
    def semanticCheck(self, globalS, localS, declType=""):
        result = True
        # determine RHS
        if self.children[0] == Fun.LPAREN:
            # check expr
            result = self.children[1].semanticCheck(globalS, localS)
        elif type(self.children[0]) == str:
            # check if ID is in scope
            if not(self.children[0] in globalS or self.children[0] in localS):
                noScopePrint(self.children[0])
                result = False

        return result

    # evaluate factor
    def execute(self, declare=False):
        executor = Executor.get_instance()

        # determine RHS
        if self.children[0] == Fun.READ:
            # read
            factor = executor.read()
        elif self.children[0] == Fun.LPAREN:
            # evaluate expr
            factor = self.children[1].execute()
        elif type(self.children[0]) == str:
            # get stored value
            factor = executor.scope.getValue(self.children[0])
        else:
            factor = self.children[0]

        return factor
