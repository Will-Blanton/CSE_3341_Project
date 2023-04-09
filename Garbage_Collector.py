# print garbage collection message

""" 
    1. reference count based garbage collector
    2. prints #reachable references for each change
    3. doesn't actually collect garbage
"""


class GarbageCollector:
    def __init__(self):
        self._reachable = 0
        self._heap = []

    def increaseRefs(self, heapIndex):
        if heapIndex >= len(self._heap):
            self._heap.append(1)
            self._reachable += 1
            self.output()
        else:
            self._heap[heapIndex] += 1

    def _decrease(self, heapIndex):
        self._heap[heapIndex] -= 1
        if self._heap[heapIndex] == 0:
            self._reachable -= 1
            self.output()

    def decreaseRefs(self, refStore):
        # add scope to stack of scopes for iteration
        valid = isinstance(refStore, list) and len(refStore) > 0
        if not valid:
            refStore = [refStore]

        # decrease counts for references leaving scope
        for scope in refStore:
            for var in scope.values():
                if var is not None and var[1] == "ref":
                    self._decrease(var[0])

    def output(self):
        print("gc:{}".format(self._reachable))
