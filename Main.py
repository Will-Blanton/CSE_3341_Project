from Executor import Executor
from Scanner import Scanner
from Parser import Parser
from Nonterminals.Prog import Prog
import sys


def main():
    # Initialize the scanners with input files
    S = Scanner(sys.argv[1])
    D = None
    if len(sys.argv) > 2:
        D = Scanner(sys.argv[2])

    # Initialize the parser with the root nonterminal and the scanner
    P = Parser(Prog(), S)

    # Build parse tree
    root = P.parse()

    P.semanticCheck()

    # root.prettyPrint()

    # Initialize executor with parse tree root and data file scanner
    Executor.initialize(root, D)

    # Execute code
    Executor.execute()


if __name__ == "__main__":
    main()