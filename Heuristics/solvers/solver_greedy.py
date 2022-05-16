import random
import time
from Heuristics.solver import _Solver
from Heuristics.solvers.localSearch import LocalSearch



class Solver_Greedy(object):
    
    def _selectCandidate(self, candidateList):
        sortedList = sorted(candidateList, key=lambda x: x.highests_changes)
        return sortedList[0]



    def construct(self):
        solution = self.instance.createSolution()

        #aixo ens hauria de trnar els codis amb ordre invers de feina a realitzar entre codi
        codes = self.instance.getCodes()
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

        
