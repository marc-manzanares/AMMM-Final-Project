import copy
import time
from Heuristics.solver import _Solver
from AMMMGlobals import AMMMException


# Implementation of a local search using two neighborhoods and two different policies.
class LocalSearch(_Solver):
    def __init__(self, config, instance):
        self.enabled = config.localSearch
        self.nhStrategy = config.neighborhoodStrategy
        self.policy = config.policy
        self.maxExecTime = config.maxExecTime
        super().__init__(config, instance)

    def exploreExchange(self, solution):
        curHighestLoad = solution.getFitness()
        bestNeighbor = solution

        # Lin-Kernighan heuristic implementation
        # Exchange non successive edges, if d(a,b) + d(c,d) > d(a,d) + d(b,c)
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
