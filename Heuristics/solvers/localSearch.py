import copy
import time
from Heuristics.solver import _Solver
from AMMMGlobals import AMMMException


class LocalSearch(_Solver):
    def __init__(self, config, instance):
        self.enabled = config.localSearch
        self.nhStrategy = config.neighborhoodStrategy
        self.policy = config.policy
        self.maxExecTime = config.maxExecTime
        super().__init__(config, instance)


    def evaluateNewPair(self, p11, p12, p21, p22):
        # Return if the new pair has lower distance value than the old one (greedy)
        d = self.instance.getDistances()
        d_old_1 = d[p11][p12]
        d_old_2 = d[p21][p22]
        d_new_1 = d[p11][p22]
        d_new_2 = d[p12][p21]

        if d_old_1 + d_old_2 > d_new_1 + d_new_2:
            return True
        return False


    def exploreExchange(self, solution):
        curHighestFlips = solution.total_sum
        bestNeighbor = solution
        nodes = solution.used_code # solution without first node
        sequence = solution.actual_sequence

        # Lin-Kernighan heuristic implementation
        # Exchange non successive edges, if d(a,b) + d(c,d) > d(a,d) + d(b,c)
        for i in range(0, sequence-1):
            return bestNeighbor


    def exploreNeighborhood(self, solution):
        if self.nhStrategy == 'TaskExchange': return self.exploreExchange(solution)
        else: raise AMMMException('Unsupported NeighborhoodStrategy(%s)' % self.nhStrategy)

    def solve(self, **kwargs):
        initialSolution = kwargs.get('solution', None)
        if initialSolution is None:
            raise AMMMException('[local search] No solution could be retrieved')

        if not initialSolution.isFeasible(): return initialSolution
        self.startTime = kwargs.get('startTime', None)
        endTime = kwargs.get('endTime', None)

        incumbent = initialSolution
        incumbentFitness = incumbent.getFitness()
        iterations = 0

        # keep iterating while improvements are found
        while time.time() < endTime:
            iterations += 1
            neighbor = self.exploreNeighborhood(incumbent)
            if neighbor is None: break
            neighborFitness = neighbor.getFitness()
            if incumbentFitness <= neighborFitness: break
            incumbent = neighbor
            incumbentFitness = neighborFitness

        return incumbent
