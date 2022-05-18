import random
import time
from Heuristics.solver import _Solver
from Heuristics.solvers.localSearch import LocalSearch



class Solver_Greedy(_Solver):
    
    def _selectCandidate(self, candidateList):
        act_min = max(candidateList)[0]
        index = max(candidateList)[1]
        for code in candidateList:
            if code[0] != 0:
                if act_min != min(act_min, code[0]):
                    act_min = min(act_min, code[0])
                    index = code[1]
        candidate = (act_min, index)
        return candidate



    def construct(self):
        solution = self.instance.createSolution()
        codes = self.instance.getDistances()

        for i in range(0, self.instance.getnumCodes()):
            if i == self.instance.getnumCodes()-1:
                solution.sum_of_codes.append(codes[solution.actual_id_sequence[-1]][0])
                solution.actual_sequence[i+1] = []
                solution.actual_sequence[i+1].append(self.instance.getNode(0))
                solution.actual_id_sequence.append(0)
                continue
            if i == 0:
                candidate_list = solution.findFeasibleAssignment(0)
            else:
                candidate_list = solution.findFeasibleAssignment(solution.actual_id_sequence[-1])

            if not candidate_list:
                solution.makeInfeasible()
                break

            candidate = self._selectCandidate(candidate_list)

            solution.add_node(candidate[0], candidate[1])
         
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
