import sys
from Symbol_Table import SymbolTable


class Executor:
    # Singleton instance
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = Executor()
        return cls._instance

    def __init__(self):
        # rootNode of parse tree to be executed
        self.rootNode = None
        self.readScanner = None
        self.scope = None
        # dictionary containing {function name: (formal param ids, stmt-seq)}
        self.functions = {}

    def initialize(self, rootNode, readScanner):
        self.rootNode = rootNode
        self.readScanner = readScanner
        self.scope = SymbolTable()

    def execute(self):
        self.rootNode.execute()

    def read(self):
        data = self.readScanner.getCONST()
        if type(data) != int:
            print("ERROR: All values in .data file have already been used")
            sys.exit()

        self.readScanner.nextTok()
        return data
