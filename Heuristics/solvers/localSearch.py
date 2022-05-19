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


    def createNeighborSolution(self, solution, new_):

        newSolution = copy.deepcopy(solution)

        for move in moves:
            newSolution.remove_node(move.taskId, move.curCPUId)

        for move in moves:
            feasible = newSolution.assign(move.taskId, move.newCPUId)
            if not feasible: return None

        return newSolution

    def evaluateNewPair(self, p11, p12, p21, p22, solution):
        # Return if the new pair has lower distance value than the old one (greedy)
        newSolution = copy.deepcopy(solution)
        new_dists = []
        new_nodes = []
        d = solution.distances
        new_dists.append(d[solution.actual_id_sequence[p11]][solution.actual_id_sequence[p12]])
        new_dists.append(d[solution.actual_id_sequence[p21]][solution.actual_id_sequence[p22]])
        new_dists.append(d[solution.actual_id_sequence[p11]][solution.actual_id_sequence[p22]])
        new_dists.append(d[solution.actual_id_sequence[p12]][solution.actual_id_sequence[p21]])

        new_nodes.append(p11)
        new_nodes.append(p12)
        new_nodes.append(p21)
        new_nodes.append(p22)

        if new_dists[0] + new_dists[1] > new_dists[2] + new_dists[3]:
            for i in range(0, 3):
                newSolution.remove_node(new_dists[i], new_nodes[i])
            for i in range(0, 3):
                newSolution.add_node(new_dists[i], new_nodes[i])
        return newSolution


    def exploreExchange(self, solution):
        curHighestFlips = solution.total_sum
        bestNeighbor = solution
        nodes = solution.used_code # solution without first node
        greedy_total_path = solution.actual_sequence
        greedy_sum_path = solution.sum_of_codes

        # Lin-Kernighan heuristic implementation
        # Exchange non successive edges, if d(a,b) + d(c,d) > d(a,d) + d(b,c)

        # We start from node[1] and end on node[n-1] because we can't modify positions of 00..00 codes
        for i in range(1, len(greedy_total_path)):
            for j in range(i+2, len(greedy_total_path)-1):
                neighborHighestFlips = self.evaluateNewPair(i, i+1, j, j+1, solution)
                if neighborHighestFlips.total_sum <= curHighestFlips:
                    # neighbor = self.createNeighborSolution(solution, i, i+1, j, j+1)
                    # if neighbor is None:
                    #     raise AMMMException('[exploreExchange] No neighbouring solution could be created')
                    if self.policy == 'FirstImprovement': return neighborHighestFlips
                    else:
                        bestNeighbor = neighborHighestFlips
                        curHighestFlips = neighborHighestFlips.total_sum

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
        incumbentFlips = incumbent.total_sum
        iterations = 0

        # keep iterating while improvements are found
        while time.time() < endTime:
            iterations += 1
            neighbor = self.exploreNeighborhood(incumbent)
            if neighbor is None: break
            neighborFlips = neighbor.total_sum
            if incumbentFlips <= neighborFlips: break
            incumbent = neighbor
            incumbentFlips = neighborFlips

        return incumbent
