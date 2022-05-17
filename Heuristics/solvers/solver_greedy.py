import random
import time
from Heuristics.solver import _Solver
from Heuristics.solvers.localSearch import LocalSearch



class Solver_Greedy(_Solver):
    
    def _selectCandidate(self, candidateList):
        sortedList = sorted(candidateList, key=lambda x: x.highests_changes)
        return sortedList[0]



    def construct(self):
        solution = self.instance.createSolution()

        #aixo ens hauria de trnar els codis amb ordre invers de feina a realitzar entre codi
        codes = self.instance.getDistances()
        #aquesta part mereix més estudi
        sortedCodes= sorted(codes, key=lambda t: t.getChanges(), reverse=True)

        for code in sortedCodes:
            codeID = code.getId()

            ##tocaria mirar si es feasible la solució no?, podem reaprofitar encara més codi?
            candidat = solution.findFeasivleAssignments(codeID)

            if not candidat:
                solution.makeInfeasible()
                break

            # select assignment
            candidate = self._selectCandidate(candidat)

            # assign the current task to the CPU that resulted in a minimum highest load
            solution.assign(codeID)
         
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
