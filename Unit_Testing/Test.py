from Executor import Executor
from Nonterminals.Cond import Cond
from Nonterminals.Expr import Expr
from Nonterminals.Out import Out
from Nonterminals.Prog import Prog
from Parser import Parser
from Scanner import Scanner
import unittest
from unittest.mock import patch, call


class Test(unittest.TestCase):

    def setUp(self) -> None:
        self.P = Parser(None, None)

    def initInterpreter(self, scannerFile, root=Prog(), data=None):
        self.P.set_scanner(Scanner(scannerFile))
        self.P.set_rootNontermial(root)

        executor = Executor.get_instance()

        if data is not None:
            data = Scanner(data)

        executor.initialize(self.P.parse(), data)

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
        self.initInterpreter("Test_Files\writeExecute", Out())

        executor = Executor.get_instance()
        executor.execute()

        # check that write has been called
        mock_print.assert_called_with(3)

    @patch('builtins.print')
    def test_int_assign(self, mock_print):
        self.initInterpreter("Test_Files\intAssign", Prog())

        executor = Executor.get_instance()
        executor.execute()

        # check that write has been called
        mock_print.assert_called_with(42)

    @patch('builtins.print')
    def test_ref_assign(self, mock_print):
        self.initInterpreter("Test_Files\\refAssign", Prog())

        executor = Executor.get_instance()
        executor.execute()

        # check that 49 is printed in the output
        mock_print.assert_called()
        output_string = ''.join([str(call[0][0]) for call in mock_print.call_args_list])
        self.assertIn("49", output_string)

    @patch('builtins.print')
    def test_if_nesting(self, mock_print):
        self.initInterpreter("Test_Files\ifNesting", Prog())

        executor = Executor.get_instance()
        executor.execute()

        # check that write has been called
        mock_print.assert_called_with(21)

    @patch('builtins.print')
    def test_while_execute(self, mock_print):
        self.initInterpreter("Test_Files\whileExecute", Prog())

        executor = Executor.get_instance()
        executor.execute()

        # check that write has been called
        mock_print.assert_called_with(7)

    @patch('builtins.print')
    def test_read_execute(self, mock_print):
        self.initInterpreter("Test_Files\\readExecute", Prog(), "Test_Files\\readExecuteData")

        executor = Executor.get_instance()
        executor.execute()

        # check that write has been called
        mock_print.assert_called_with(42)

    def test_read_error(self):
        self.initInterpreter("Test_Files\\readError", Prog(), "Test_Files\\readErrorData")

        executor = Executor.get_instance()

        with self.assertRaises(SystemExit):
            executor.execute()

    def test_null_ref_error(self):
        self.initInterpreter("Test_Files\\nullRefError", Prog())

        executor = Executor.get_instance()

        with self.assertRaises(SystemExit):
            executor.execute()

    # TESTS FOR PROJECT 4
    @patch('builtins.print')
    def test_function_execute(self, mock_print):
        self.initInterpreter("Test_Files\\functionExecute", Prog())

        executor = Executor.get_instance()
        executor.execute()

        # check that 5 is printed in the output
        mock_print.assert_called()
        output_string = ''.join([str(call[0][0]) for call in mock_print.call_args_list])
        self.assertIn("5", output_string)

    @patch('builtins.print')
    def test_recursive_execute(self, mock_print):
        self.initInterpreter("Test_Files\\recursiveExecute", Prog())

        executor = Executor.get_instance()
        executor.execute()

        # check that 32 is printed in the output
        mock_print.assert_called()
        output_string = ''.join([str(call[0][0]) for call in mock_print.call_args_list])
        self.assertIn("32", output_string)

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

    # TESTS FOR PROJECT 5
    @patch('builtins.print')
    def test_ref_increase(self, mock_print):
        self.initInterpreter("Test_Files\\refIncrease", Prog())

        executor = Executor.get_instance()
        executor.execute()

        expected = [call("gc:1"), call("gc:2")]

        # check that garbage collector is counting reachable
        mock_print.assert_has_calls(expected)

    @patch('builtins.print')
    def test_ref_decrease(self, mock_print):
        self.initInterpreter("Test_Files\\refDecrease", Prog())

        executor = Executor.get_instance()
        executor.execute()

        expected = [call("gc:1"), call("gc:2"), call("gc:3"), call("gc:2"), call(12), call("gc:1"), call("gc:0")]

        # check that garbage collector is counting reachable
        mock_print.assert_has_calls(expected)

    @patch('builtins.print')
    def test_ref_copy(self, mock_print):
        self.initInterpreter("Test_Files\\refCopy", Prog())

        executor = Executor.get_instance()
        executor.execute()

        expected = [call("gc:1"), call("gc:2"), call("gc:1"), call("gc:0")]

        # check that garbage collector is decreasing reachable when reference value is switched
        mock_print.assert_has_calls(expected)


if __name__ == '__main__':
    unittest.main()
