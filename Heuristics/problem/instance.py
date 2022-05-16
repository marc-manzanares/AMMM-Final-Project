from Heuristics.problem.solution import Solution

class Instance(object):
    def __init__(self, config, inputData):
        self.config = config
        self.inputData = inputData
        self.sizeCode = inputData.m
        self.numCodes = inputData.n
        self.sequence = inputData.S

        # Construct distance matrix
        self.distances = [[0 for _ in range(self.numCodes)] for _ in range(self.numCodes)]
        for i in range(0, self.numCodes):
            for j in range(0, self.numCodes):
                num_flips = 0
                for k in range(0, self.sizeCode):
                    if i == 0 and j == 0:
                        self.distances[i][j] = 0
                    else:
                        if self.sequence[i][k] != self.sequence[j][k]:
                            num_flips += 1
                self.distances[i][j] = num_flips

    def getSizeCode(self):
        # Returns length of each code (m paremeter)
        return self.sizeCode

    def getnumCodes(self):
        # Returns the number of codes in S
        return self.numCodes

    def getNode(self, index):
        # Returns the code of S[index]
        return self.sequence[index]

    def getDistances(self):
        # Returns the distance matrix of S
        return self.distances

    def getSequence(self):
        # Returns matrix S of the input instance
        return self.sequence

    def createSolution(self):
        solution = Solution(self.sequence, self.distances)
        solution.setVerbose(self.config.verbose)
        return solution

    def checkInstance(self):
        return True
