# CSE 3341 Principles of Programming Languages Project

## Description
The Fun interpreter is a Python-based implementation of the Fun programming language, a basic language developed for this class project by the instructor. The language supports functions with the reference type for parameters and uses call-by-value result. The interpreter includes a garbage collector based on reference counting that prints the number of reachable references every time it changes instead of actual garbage collection.

The language supports reading files containing integer values using the read function, which can be processed and manipulated through Fun's built-in functions and operators. The interpreter includes a just-in-time scanner, allowing for efficient parsing of Fun code.

Fun's recursive descent parsing is implemented using classes, with each nonterminal implemented as a class that inherits from an abstract class for nonterminals, making the interpreter flexible and easy to extend.

## Authors
- Will Blanton

## Files
- Main.py: Accepts input text file from command line with program and text file with data, parses the first text file, and executes the code
- Fun.py: Contains enums for tokens in the Fun language
- Token_Dictionary.py: Contains a dictionary mapping tokens to corresponding strings
- Scanner.py: Converts character stream into tokens in Fun language using token dictionary
- Parser.py: Used to parse token stream using the Fun grammar, print the parse tree, and check for semantic errors
- Executor.py: A singleton used to store the symbol table used in execution. It also has a method to read from the data file and to execute the code starting at the given root node of a parse tree
- Garbage_Collector.py: Contains the garbage collector class which contains fields and methods used for reference count-based garbage collection
- Util.py: Contains methods for printing errors or specific print formats that were frequently used
- tester.sh: Tests Main.py using text files from the Correct directory

## Directories
### Correct: 
- Contains test code in the Fun language and the corresponding data files
### Unit_testing:
- Test.py: Unit tests for garbage collector, executor, execute methods, function execution, and semantic errors in functions
- Test_Files: Contains text files with sentences from the Fun grammar that are used in unit tests

## Special Features
- The executor is a singleton
- The parser implementation uses the strategy design pattern, where the Nonterminal classes are the concrete strategies, the context is the parser, which only interacts with the Nonterminal abstract class, and Main is the client.
- The scanner reads in the character stream one token at a time.

## Testing
- The interpreter was tested using the Python unittest package. The tests from projects 3 and 4 were kept, and test cases were added for different garbage collection cases. The tester.sh scripts were also used for testing.

## Potential Improvements
- The parser could be a singleton to remove the need for the parser parameter in the nonterminal parse methods.
The semantic error checks could be moved from the nonterminal semanticCheck methods to the symbolTable class or executor class depending on the type of the error.

## Bugs
- There are currently no known bugs.
