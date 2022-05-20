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


    def exchangePair(self, old_dists, new_dists, nodes_id, solution):
        # Update solution.total_sum (remove old distances, add new distances)
        # Exchange nodes on solution.actual_sequence and actual_id_sequence

        # Update total_sum
        # for dist in old_dists:
        #     solution.total_sum -= dist
        # for dist in new_dists:
        #     solution.total_sum += dist

        # Update actual_id_sequence (a list with the new solution path)
        new_sequence = {}
        new_id_sequence = []
        reverse = False
        i = 0
        while not reverse:
            # Add nodes while not having to change the first node
            new_id_sequence.append(solution.actual_id_sequence[i])
            new_sequence[solution.actual_id_sequence[i]] = []
            new_sequence[solution.actual_id_sequence[i]].append(solution.sequence[solution.actual_id_sequence[i]])
            if solution.actual_id_sequence[i] == nodes_id[0]:
                new_id_sequence.append(nodes_id[2])
                new_sequence[nodes_id[2]] = []
                new_sequence[nodes_id[2]].append(solution.sequence[nodes_id[2]])
                reverse = True
            i += 1
        i = solution.actual_id_sequence.index(nodes_id[2])-1
        while reverse:
            new_id_sequence.append(solution.actual_id_sequence[i])
            new_sequence[solution.actual_id_sequence[i]] = []
            new_sequence[solution.actual_id_sequence[i]].append(solution.sequence[solution.actual_id_sequence[i]])
            if solution.actual_id_sequence[i] == nodes_id[1]:
                new_id_sequence.append(nodes_id[3])
                new_sequence[nodes_id[3]] = []
                new_sequence[nodes_id[3]].append(solution.sequence[nodes_id[3]])
                reverse = False
            i -= 1
        for i in range(solution.actual_id_sequence.index(nodes_id[3])+1, len(solution.actual_id_sequence)):
            new_id_sequence.append(solution.actual_id_sequence[i])
            new_sequence[solution.actual_id_sequence[i]] = []
            new_sequence[solution.actual_id_sequence[i]].append(solution.sequence[solution.actual_id_sequence[i]])

        # Update total_sum
        new_total_sum = 0
        for i in range(0, len(new_id_sequence)-1):
            if i == len(new_id_sequence)-2:
                new_total_sum += solution.distances[new_id_sequence[i]][0]
            else:
                new_total_sum += solution.distances[new_id_sequence[i]][new_id_sequence[i+1]]

        solution.actual_id_sequence = new_id_sequence
        solution.actual_sequence = new_sequence
        solution.total_sum = new_total_sum

        return solution


    def evaluateNewPair(self, p11, p12, p21, p22, solution):
        # Return if the new pair has lower distance value than the old one (greedy)
        newSolution = copy.deepcopy(solution)
        new_dists = []
        old_dists = []
        nodes_id = []
        d = solution.distances
        old_dists.append(d[solution.actual_id_sequence[p11]][solution.actual_id_sequence[p12]])
        old_dists.append(d[solution.actual_id_sequence[p21]][solution.actual_id_sequence[p22]])
        new_dists.append(d[solution.actual_id_sequence[p11]][solution.actual_id_sequence[p22]])
        new_dists.append(d[solution.actual_id_sequence[p12]][solution.actual_id_sequence[p21]])

        nodes_id.append(solution.actual_id_sequence[p11])
        nodes_id.append(solution.actual_id_sequence[p12])
        nodes_id.append(solution.actual_id_sequence[p21])
        nodes_id.append(solution.actual_id_sequence[p22])

        if old_dists[0] + old_dists[1] > new_dists[0] + new_dists[1]:
            # exchange pairs
            return self.exchangePair(old_dists, new_dists, nodes_id, newSolution)
        return solution


    def exploreExchange(self, solution):
        curHighestFlips = solution.total_sum
        bestNeighbor = solution
        greedy_total_path = solution.actual_sequence

        # Lin-Kernighan heuristic implementation
        # Exchange non successive edges, if d(a,b) + d(c,d) > d(a,d) + d(b,c)

        for i in range(0, len(greedy_total_path)):
            # We probably have to change it to i+3 (non successive edge)
            for j in range(i+3, len(greedy_total_path)-1):
                neighborHighestFlips = self.evaluateNewPair(i, i+1, j, j+1, solution)
                if neighborHighestFlips.total_sum <= curHighestFlips:
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
            self.writeLogLine(neighborFlips, iterations)
            if incumbentFlips <= neighborFlips:
                if iterations == 5:
                    break
            incumbent = neighbor
            incumbentFlips = neighborFlips

        return incumbent
