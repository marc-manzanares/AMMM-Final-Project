from Heuristics.solution import _Solution


class Solution(_Solution):
    def __init__(self, sequence, distances):
        self.sequence = sequence
        self.distances = distances
        #es defineix com la llista dels nodes(codis) qu el nostre TSP(que es el que es a la practica) ha visitat size = k-1
        #en aquest no posem el primer 0
        self.used_code=[]
        #es defineix om la sequencia actual que s'esta provant size = k
        #en aquest posem el primer 0
        self.actual_sequence=[]
        super().__init__()

    #afegim un node visitat a les llistes
    def add_node(self, node):
        if node not in self.used_code:
            self.used_code.append(node)
            self.actual_sequence.append(node)
            return True
        else: return False

    def add_starter_node(self,node):
        self.actual_sequence.append(node)
        return True


