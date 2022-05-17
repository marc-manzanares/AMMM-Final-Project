import random
import time
from Heuristics.solver import _Solver
from Heuristics.solvers.localSearch import LocalSearch



class Solver_Greedy(_Solver):
    
    def _selectCandidate(self, candidateList):
        act_min =max(candidateList)
        for i in range(len(candidateList)):
            if candidateList[i]!= 0:
                act_min=min(act_min,candidateList[i])
        return act_min



    def construct(self):
        solution = self.instance.createSolution()

        #aixo ens hauria de trnar els codis amb ordre invers de feina a realitzar entre codi
        codes = self.instance.getDistances()
        #aquesta part mereix més estudi
         
        #hem faltaria dafirmar k no hauria de ser 0, pero aixo auria de servir crec
        node_actual=0
        for i in range(0, self.instance.getnumCodes()):
            node_actual = self._selectCandidate(node_actual)
            # assign the current task to the CPU that resulted in a minimum highest load
            solution.add_node(self.instance.getNode(node_actual))
         
        return solution

        
    def solve(self, **kwargs):
        self.startTimeMeasure()

        solver = kwargs.get('solver', None)
        if solver is not None:
            self.config.solver = solver
        localSearch = kwargs.get('localSearch', None)
        if localSearch is not None:
            self.config.localSearch = localSearch

        self.writeLogLine(float('inf'), 0)

        solution = self.construct()
        if self.config.localSearch:
            localSearch = LocalSearch(self.config, None)
            endTime= self.startTime + self.config.maxExecTime
            solution = localSearch.solve(solution=solution, startTime=self.startTime, endTime=endTime)

        self.elapsedEvalTime = time.time() - self.startTime
        self.writeLogLine(solution.getFitness(), 1)
        self.numSolutionsConstructed = 1
        self.printPerformance()

        return solution
