import random
import time
from Heuristics.solver import _Solver
from Heuristics.solvers.localSearch import LocalSearch


# Inherits from the parent abstract solver.
class Solver_GRASP(_Solver):

    def _selectCandidate(self, candidateList, alpha):

        # sort candidate assignments by highestLoad in ascending order
        act_min = max(candidateList)[0]
        act_max = min(candidateList)[0]
        index = max(candidateList)[1]

        # compute boundary highest load as a function of the minimum and maximum highest loads and the alpha parameter
        """
        minHLoad = sortedCandidateList[0].highestLoad
        maxHLoad = sortedCandidateList[-1].highestLoad
        """
        boundaryHLoad = act_max + (act_min - act_max) * alpha

        # find elements that fall into the RCL
        maxIndex = 0
        for candidate in candidateList:
            if candidate[0] <= boundaryHLoad:
                maxIndex += 1

        # create RCL and pick an element randomly
        rcl = candidateList[0:maxIndex]  # pick first maxIndex elements starting from element 0
        if not rcl: return None
        return random.choice(rcl)  # pick a candidate from rcl at random

    def _greedyRandomizedConstruction(self, alpha):
        # get an empty solution for the problem
        solution = self.instance.createSolution()

        # get tasks and sort them by their total required resources in descending order
        codes = self.instance.getDistances()

        # for each task taken in sorted order
        for i in range(0, self.instance.getnumCodes()):
            if i == self.instance.getnumCodes() - 1:
                solution.sum_of_codes.append(codes[solution.actual_id_sequence[-1]][0])
                solution.total_sum += codes[solution.actual_id_sequence[-1]][0]
                solution.actual_sequence[i + 1] = []
                solution.actual_sequence[i + 1].append(self.instance.getNode(0))
                solution.actual_id_sequence.append(0)
                continue
            if i == 0:
                candidate_list = solution.findFeasibleAssignment(0)
            else:
                candidate_list = solution.findFeasibleAssignment(solution.actual_id_sequence[-1])

            if not candidate_list:
                solution.makeInfeasible()
                break

            # select an assignment,must pass a tuple {id,dist}
            candidate = self._selectCandidate(candidate_list, alpha)

            solution.add_node(candidate[0], candidate[1])

        return solution

    def stopCriteria(self):
        self.elapsedEvalTime = time.time() - self.startTime
        return time.time() - self.startTime > self.config.maxExecTime

    def solve(self, **kwargs):
        self.startTimeMeasure()
        incumbent = self.instance.createSolution()
        incumbent.makeInfeasible()
        bestHighestLoad = incumbent.getFitness()
        self.writeLogLine(bestHighestLoad, 0)

        iteration = 0
        while not self.stopCriteria():
            iteration += 1

            # force first iteration as a Greedy execution (alpha == 0)
            alpha = 0 if iteration == 1 else self.config.alpha

            solution = self._greedyRandomizedConstruction(alpha)
            if self.config.localSearch:
                localSearch = LocalSearch(self.config, None)
                endTime = self.startTime + self.config.maxExecTime
                solution = localSearch.solve(solution=solution, startTime=self.startTime, endTime=endTime)

            if solution.isFeasible():
                solutionHighestLoad = solution.getFitness()
                if solutionHighestLoad < bestHighestLoad:
                    incumbent = solution
                    bestHighestLoad = solutionHighestLoad
                    self.writeLogLine(bestHighestLoad, iteration)

        self.writeLogLine(bestHighestLoad, iteration)
        self.numSolutionsConstructed = iteration
        self.printPerformance()
        return incumbent
