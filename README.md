CSE 3341 (Principles of Programming Languages) Project

Description: 
The Fun interpreter is a Python-based implementation of the Fun programming language (a basic language developed for this class project by the instructor), which supports functions with the reference type for parameters and uses call-by-value result. The interpreter includes a garbage collector based reference counting which prints the number of reachable references every time it changes instead of actual garbage collection.

The language supports reading files containing integer values using the read , which can be processed and manipulated through Fun's built-in functions and operators. The interpreter includes a just-in-time scanner, which allows for efficient parsing of Fun code.

Fun's recursive descent parsing is implemented using classes, with each nonterminal implemented as a class that inherits from an abstract class for nonterminals. This makes the interpreter flexible and easy to extend.

Name: Will Blanton

Collaborators: None

Files:
Main.py - accepts input text file from command line with program and text file with data, parses the first text file, and executes the code

Fun.py - contains enums for tokens in the Fun language

Token_Dictionary.py contains a dictionary mapping tokens to corresponding strings

Scanner.py - converts character stream into tokens in Fun language using token dictionary

Parser.py - used to parse token stream using the Fun grammar, print the parse tree, and check for semantic errors

Executor.py - a singleton that is used to store the symbol table used in execution. It also has a method to read from the data file and to execute the code starting at the given root node of a parse tree 

Garbage_Collector.py - contains the garbage collector class which contains fields and methods used for reference count-based garbage collection 

Util.py - contains methods for printing errors or specific print formats that were frequently used

tester.sh - tests Main.py using text files from the Correct directory

Correct - contains test code in the fun language and the corresponding data files 

Unit_testing:
1. Test.py - unit tests for garbage collector, executor, execute methods, function execution, and semantic errors in functions
2. Test_Files - contains text files with sentences from the Fun grammar that are used in unit tests

Nonterminals:
1. Nonterminal.py - an abstract nonterminal class with instance fields for children and a parent and methods for execution, semantic checking, parsing, and pretty printing
2. Others - the rest of the files are each a class for a nonterminal in the fun grammar and implement the nonterminal abstract class

Special Features:
-My executor is a singleton
-For my parser implementation, I used the strategy desing pattern where the Nonterminal classes are the concrete strategies, the context is the parser which only interacts with the Nonterminal abstract class, and Main is the client. 
-My scanner reads in the character stream one token at a time.

Testing:
I tested the interpreter using the Python unittest package. I kept the tests from project 3 and 4 since I modified the symbol table class. I added test cases for different garbage collection cases. I also used the tester.sh scripts after I had finished.

Potential Improvements:
-The parser could be a singleton to remove the need for the parser parameter in the nonterminal parse methods.
-The semantic error checks could be moved from the nonterminal semanticCheck methods to the symbolTable class or executor class depending on the type of the error.

Bugs:
-I am not currently aware of any bugs.
