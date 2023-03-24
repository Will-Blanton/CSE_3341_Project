import sys

from Symbol_Table import SymbolTable


class Executor:
    # rootNode of parse tree to be executed
    rootNode = None
    readScanner = None
    scope = None
    # dictionary containing {function name: (formal param ids, stmt-seq)}
    functions = {}

    @classmethod
    def initialize(cls, rootNode, readScanner):
        cls.rootNode = rootNode
        cls.readScanner = readScanner
        cls.scope = SymbolTable()

    @staticmethod
    def execute():
        Executor.rootNode.execute()

    @staticmethod
    def read():
        data = Executor.readScanner.getCONST()
        if type(data) != int:
            print("ERROR: All values in .data file have already been used")
            sys.exit()

        Executor.readScanner.nextTok()
        return data
