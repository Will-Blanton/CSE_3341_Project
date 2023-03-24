from Executor import Executor
from Fun import Fun
from Nonterminals.Assign import Assign
from Nonterminals.Cmpr import Cmpr
from Nonterminals.Cond import Cond
from Nonterminals.DeclRef import DeclRef
from Nonterminals.DeclSeq import DeclSeq
from Nonterminals.Decl import Decl
from Nonterminals.DeclInt import DeclInt
from Nonterminals.Expr import Expr
from Nonterminals.Factor import Factor
from Nonterminals.IdList import IdList
from Nonterminals.Out import Out
from Nonterminals.Prog import Prog
from Nonterminals.Stmt import Stmt
from Nonterminals.Term import Term
from Parser import Parser
from Scanner import Scanner
import unittest
from unittest.mock import patch

from Symbol_Table import SymbolTable


class ParserTest(unittest.TestCase):

    def setUp(self) -> None:
        self.P = Parser(None, None)

    def test_expression_execute(self):
        self.P.set_scanner(Scanner("Test_Files\exprExecute"))

        self.P.set_rootNontermial(Expr())
        root = self.P.parse()

        # expected expression value
        expected = 8

        self.assertEqual(expected, root.execute(None))

    def test_condition_execute(self):
        self.P.set_scanner(Scanner("Test_Files\condExecute"))

        self.P.set_rootNontermial(Cond())
        root = self.P.parse()

        # expected expression value
        expected = True

        self.assertEqual(expected, root.execute(None))

    @patch('builtins.print')
    def test_write_execute(self, mock_print):
        self.P.set_scanner(Scanner("Test_Files\writeExecute"))

        self.P.set_rootNontermial(Out())
        root = self.P.parse()

        Executor.initialize(root, None)
        Executor.execute()

        # check that write has been called
        mock_print.assert_called_with(3)

    @patch('builtins.print')
    def test_int_assign(self, mock_print):
        self.P.set_scanner(Scanner("Test_Files\intAssign"))

        self.P.set_rootNontermial(Prog())
        root = self.P.parse()

        Executor.initialize(root, None)
        Executor.execute()

        # check that write has been called
        mock_print.assert_called_with(42)

    @patch('builtins.print')
    def test_ref_assign(self, mock_print):
        self.P.set_scanner(Scanner("Test_Files\\refAssign"))

        self.P.set_rootNontermial(Prog())
        root = self.P.parse()

        Executor.initialize(root, None)
        Executor.execute()

        # check that write has been called
        mock_print.assert_called_with(0)

    @patch('builtins.print')
    def test_if_nesting(self, mock_print):
        self.P.set_scanner(Scanner("Test_Files\ifNesting"))

        self.P.set_rootNontermial(Prog())
        root = self.P.parse()

        Executor.initialize(root, None)
        Executor.execute()

        # check that write has been called
        mock_print.assert_called_with(21)

    @patch('builtins.print')
    def test_while_execute(self, mock_print):
        self.P.set_scanner(Scanner("Test_Files\whileExecute"))

        self.P.set_rootNontermial(Prog())
        root = self.P.parse()

        Executor.initialize(root, None)
        Executor.execute()

        # check that write has been called
        mock_print.assert_called_with(7)

    @patch('builtins.print')
    def test_write_execute(self, mock_print):
        self.P.set_scanner(Scanner("Test_Files\\readExecute"))

        self.P.set_rootNontermial(Prog())
        root = self.P.parse()

        # init scanner for data
        data = Scanner("Test_Files\\readExecuteData")

        Executor.initialize(root, data)
        Executor.execute()

        # check that write has been called
        mock_print.assert_called_with(42)

    def test_read_error(self):
        self.P.set_scanner(Scanner("Test_Files\\readError"))

        self.P.set_rootNontermial(Prog())
        root = self.P.parse()

        # init scanner for data
        data = Scanner("Test_Files\\readErrorData")

        Executor.initialize(root, data)

        with self.assertRaises(SystemExit):
            Executor.execute()

    def test_null_ref_error(self):
        self.P.set_scanner(Scanner("Test_Files\\nullRefError"))

        self.P.set_rootNontermial(Prog())
        root = self.P.parse()

        Executor.initialize(root, None)

        with self.assertRaises(SystemExit):
            Executor.execute()

    # TESTS FOR PROJECT 4
    @patch('builtins.print')
    def test_function_execute(self, mock_print):
        self.P.set_scanner(Scanner("Test_Files\\functionExecute"))

        self.P.set_rootNontermial(Prog())
        root = self.P.parse()

        Executor.initialize(root, None)
        Executor.execute()

        # check that write has been called
        mock_print.assert_called_with(5)

    @patch('builtins.print')
    def test_recursive_execute(self, mock_print):
        self.P.set_scanner(Scanner("Test_Files\\recursiveExecute"))

        self.P.set_rootNontermial(Prog())
        root = self.P.parse()

        Executor.initialize(root, None)
        Executor.execute()

        # check that write has been called
        mock_print.assert_called_with(32)

    def test_duplicate_func_error(self):
        self.P.set_scanner(Scanner("Test_Files\\functionDupError"))

        self.P.set_rootNontermial(Prog())
        self.P.parse()

        with self.assertRaises(SystemExit):
            self.P.semanticCheck()

    def test_no_target_error(self):
        self.P.set_scanner(Scanner("Test_Files\\noTargetError"))

        self.P.set_rootNontermial(Prog())
        self.P.parse()

        with self.assertRaises(SystemExit):
            self.P.semanticCheck()


if __name__ == '__main__':
    unittest.main()
