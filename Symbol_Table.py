import sys

from Garbage_Collector import GarbageCollector


class SymbolTable:
    def __init__(self):
        # dictionary of strings (variables) to ints
        self.globVars = {}
        # stack of frames
        # frames[-1] contains current local scope
        self.frames = [[{}]]
        # array of ints
        self.heap = []
        # garbage collector
        self._garbage = GarbageCollector()

    def enterScope(self):
        self.frames[-1].append({})

    def exitScope(self):
        self._garbage.decreaseRefs(self.frames[-1][-1])
        self.frames[-1].pop()

    def enterFrame(self):
        self.frames.append([{}])

    def exitFrame(self):
        self._garbage.decreaseRefs(self.frames[-1])
        self.frames.pop()

    def exitProg(self):
        self.exitScope()
        self._garbage.decreaseRefs(self.globVars)

    # declare int by default
    def __declareVar(self, var, varType, varContainer):
        if varType == "ref":
            # if var has already been declared in current statement, decreaseRef for old reference
            if var in self.frames[-1][-1].keys():
                self._garbage.decreaseRefs(self.frames[-1][-1][var][0])

            varContainer[var] = [None, varType]
        else:
            varContainer[var] = [0, "int"]

    def declareGlobal(self, var, varType):
        self.__declareVar(var, varType, self.globVars)

    def declareLocal(self, var, varType):
        self.__declareVar(var, varType, self.frames[-1][-1])

    # find and return the scope var is in
    def __getScope(self, var):
        # check local scopes
        i = len(self.frames[-1]) - 1
        while i >= 0:
            if var in self.frames[-1][i].keys():
                return self.frames[-1][i]
            i -= 1

        # check global
        if var in self.globVars.keys():
            return self.globVars

    def getValue(self, var):
        scope = self.__getScope(var)
        if scope[var][1] == "ref":
            heapIndex = scope[var][0]
            value = self.heap[heapIndex]
        else:
            value = scope[var][0]

        return value

    # get reference value
    def getRefValue(self, var):
        scope = self.__getScope(var)
        return scope[var][0]

    # assign int rValue to var
    def assignInt(self, var, rValue):
        scope = self.__getScope(var)
        if scope[var][1] == "ref":
            heapIndex = scope[var][0]
            # check if ref has been declared
            if heapIndex is None:
                print("ERROR: Cannot assign to '{}'. Ref '{}' is null".format(var, var))
                sys.exit()
            else:
                self.heap[heapIndex] = rValue
        else:
            scope[var][0] = rValue

    # create a new pos in the heap
    def initRef(self, var):
        self.__getScope(var)[var][0] = len(self.heap)
        self._garbage.increaseRefs(len(self.heap))
        self.heap.append(None)

    '''
     copy heap index from rVar to lVar
     if rIndex = True, rVal is a heapIndex instead of a var
    '''
    def copyRef(self, lVar, rVal, rIndex=False, out=False):
        lScope = self.__getScope(lVar)
        lIndex = lScope[lVar][0]
        if rIndex:
            index = rVal
            if not out:
                self._garbage.increaseRefs(index)
            elif lIndex != index:
                self._garbage.switchRefs(lIndex, rIndex)
        else:
            rScope = self.__getScope(rVal)
            index = rScope[rVal][0]

            if lIndex is not None:
                self._garbage.decreaseRefs(lIndex)
            self._garbage.increaseRefs(index)

        lScope[lVar][0] = index
