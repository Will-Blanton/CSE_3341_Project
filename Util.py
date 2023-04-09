# print error message for unexpected token(s)
def unexpectedTokPrint(expected, actual):
    if type(expected) != list:
        expected = [expected]

    if len(expected) == 1:
        print("ERROR: Expected {}, but got {}".format(expected[0], actual))
    else:
        print("ERROR: Expected one of {}, but got {}".format(expected, actual))


# print error message for unexpected token(s)
def doublyDeclaredPrint(var):
    print("ERROR: {} declared multiple times in same scope".format(var))


# print error message when variable is out of scope
def noScopePrint(var):
    i = 0
    # print("ERROR: {} not in scope".format(var))


# print error message when the function call has no target
def noTargetPrint(var, formals):
    print("ERROR: '{}' was called with '{}' parameters but the target does not exist".format(var, formals))


# print error message when a function with the same name has already been declared
def duplicateFunctionPrint(var):
    print("ERROR: The function '{}' has been declared multiple times".format(var))


# print error message when a function with the multiple formals with the same name has been declared
def duplicateFormalPrint(var):
    print("ERROR: The function '{}' has been declared with duplicate formal parameters".format(var))


# print error message for unexpected token(s)
def incompatibleTypePrint(var, type):
    print("ERROR: {} is not type({})".format(var, type))


# print given text with specified # of tab indents
def indentPrint(indents, text):
    print("{}{}".format("\t" * indents, text), end="")
