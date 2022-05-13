

class Instance(object):
    def __init__(self, config, inputData):
        self.config = config
        self.inputData = inputData
        self.sizeCode = inputData.m
        self.numCodes = inputData.n
        sequence = inputData.S

        # Need to implement problem files first
        # self.sequence = [[0 for _ in range(self.sizeCode)] for _ in range(self.numCodes)]
        # for code in range(0, self.sizeCode):
        #     for digit in range(code):
        #         self.sequence[code][digit] =

    def getSizeCode(self):
        return self.sizeCode

    def getnumCodes(self):
        return self.numCodes

    def getSequence(self):
        return self.sequence

    def createSolution(self):
        return

    def checkInstance(self):
        return
