from abc import ABC, abstractmethod
from Symbol_Table import SymbolTable


# Abstract class for nonterminals
class Nonterminal(ABC):
    def __init__(self, parent):
        self.children = []
        self.parent = parent

    # check for equality of nonterminals
    def __eq__(self, other):
        equal = False

        # check for type equality
        if type(self) == type(other):
            # check for equality among children
            equal = self.children == other.children

        return equal

    @abstractmethod
    def parse(self, scanner):
        pass

    @abstractmethod
    def prettyPrint(self, indents=0):
        pass

    @abstractmethod
    def semanticCheck(self, globalS, localS, declType=""):
        pass

    @abstractmethod
    def execute(self, declare=False):
        pass
