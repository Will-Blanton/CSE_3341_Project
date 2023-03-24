import sys
from Util import unexpectedTokPrint


class Parser:
    # list of declared functions
    funcDeclared = None

    def __init__(self, root, scanner):
        self.__rootNonterminal = root
        self.__scanner = scanner
        self.parsed = False
        Parser.funcDeclared = {}

    # change root nonterminal
    def set_rootNontermial(self, nonterminal):
        self.__rootNonterminal = nonterminal

    def get_rootNontermial(self):
        return self.__rootNonterminal

    # change scanner
    def set_scanner(self, scanner):
        self.__scanner = scanner

    # parse given nonterminal, output root nonterminal when finished
    def parse(self, nonterminal=None):
        if nonterminal is None:
            # parse root Nonterminal
            self.__rootNonterminal.parse(self)
            self.parsed = True
            return self.__rootNonterminal

        else:
            # add nonterminal as a child to its parent and parse nonterminal
            nonterminal.parent.children.append(nonterminal)
            nonterminal.parse(self)

    '''
        check for semantic errors
        only call after parse
    '''
    def semanticCheck(self):
        if self.parsed:
            if not self.__rootNonterminal.semanticCheck({}, {}):
                # parse error
                self.endParse()

    # return current token from scanner
    def currentTok(self):
        return self.__scanner.currentTok()

    # check if token is expected and consume or respond to error
    def consumeTok(self, expectedTok):
        if self.__scanner.currentTok() == expectedTok:
            self.__scanner.nextTok()
        else:
            self.endParse(expectedTok)

    '''
    check if token is expected and add to parse tree or respond to error
    valid types:
        Default - save token to parse tree
        ID - save token's ID value to parse tree
        CONST - save token's CONST value to parse tree
    '''
    def saveTok(self, nonterminal, expectedTok, type="Token"):
        if self.__scanner.currentTok() == expectedTok:
            # determine which type of token is being added (ID, CONST, Token)
            child = self.__scanner.currentTok()
            if type == "ID":
                child = self.__scanner.getID()

            elif type == "CONST":
                child = self.__scanner.getCONST()

            nonterminal.children.append(child)
            self.__scanner.nextTok()

        else:
            self.endParse(expectedTok)

    # close resources and exit to OS if given expectedTok
    def endParse(self, expectedTok=None):
        # close scanner file
        self.__scanner.close()

        # print error message
        if expectedTok is not None:
            unexpectedTokPrint(expectedTok, self.__scanner.currentTok())

        # exit to OS
        sys.exit()
