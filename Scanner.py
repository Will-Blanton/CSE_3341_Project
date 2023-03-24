import sys
from Fun import Fun

from Token_Dictionary import tokenDictionary


class Scanner:
    # Constructor should open the file and find the first token
    def __init__(self, filename):
        self.__currentTokenString = ""
        self.__nextTokStartChar = " "
        self.__currentToken = None
        self.__inputFile = open(filename)
        self.nextTok()

    # convert string to token
    def __tokenize(self):
        lower = self.__currentTokenString.lower()
        if lower in tokenDictionary.keys():
            token = tokenDictionary[lower]
            if lower is "":
                # close file after EOS found
                self.close()
        elif self.__currentTokenString.isalnum() and not self.__currentTokenString[0].isdigit():
                token = tokenDictionary["id"]
        elif self.__currentTokenString.isdigit() and int(self.__currentTokenString) <= 255:
            # check if token is valid const
            token = tokenDictionary["const"]
        else:
            # print error message depending on type of error
            if self.__currentTokenString.isdigit():
                print("ERROR: Const \'" + self.__currentTokenString + "\' is out of bounds (" +
                      self.__currentTokenString + " > 255)")
            else:
                print("ERROR: Invalid character input \'" + self.__currentTokenString + "\'")
            token = tokenDictionary["error"]

            # close file after error found
            self.close()

            # exit to OS
            sys.exit()

        return token

    # nextTok should advance the scanner to the next token
    def nextTok(self):
        if self.currentTok() != Fun.EOS:
            tokenFound = False

            # get first character of next token
            while self.__nextTokStartChar.isspace():
                self.__nextTokStartChar = self.__inputFile.read(1)

            tokenString = self.__nextTokStartChar

            # don't check closed
            if not self.__inputFile.closed:
                while not tokenFound:
                    currentChar = self.__inputFile.read(1)

                    # determine if currentChar is part of token
                    is_id_or_key = self.__nextTokStartChar.isalpha() and currentChar.isalnum()
                    is_const = self.__nextTokStartChar.isdigit() and currentChar.isdigit()
                    is_equality = (tokenString == "=" or tokenString == "<") and currentChar == "="

                    # update token
                    if is_id_or_key or is_const or is_equality:
                        tokenString = tokenString + currentChar
                    else:
                        # save start of next token
                        self.__nextTokStartChar = currentChar
                        tokenFound = True

                self.__currentTokenString = tokenString
                self.__currentToken = self.__tokenize()

    # currentTok should return the current token
    def currentTok(self):
        return self.__currentToken

    # If the current token is ID, return the string value of the identifier
    # Otherwise, return value does not matter
    def getID(self):
        out = "Not an id\n"
        if self.__currentToken == Fun.ID:
            out = self.__currentTokenString
        return out

    # If the current token is CONST, return the numerical value of the constant
    # Otherwise, return value does not matter
    def getCONST(self):
        out = False
        if self.__currentToken == Fun.CONST:
            out = int(self.__currentTokenString)
        return out

    # close the scanner's input file
    def close(self):
        if not self.__inputFile.closed:
            self.__inputFile.close()
