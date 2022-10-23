

import random
# from random import random
from graph import Graph

class Prey:
   
    def __init__(self, graph) -> None:
        # Prey Spawn Position
        # self.position = random.randint(0,49)
        self.position = graph.allocate_pos()

    def __update__(self,graph):
        lst = list()
        lst.append(self.position)
        for el in graph[self.position]:
            lst.append(el)

        x = random.choice(lst)
        self.position = x 

    def prey_position(self):
        return self.position   
        
        