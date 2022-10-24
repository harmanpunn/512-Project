

import random
# from random import random
from graph import Graph
from graphEntity import GraphEntity

"""

Prey class extends GraphEntity

"""
class Prey(GraphEntity):
   
    def __init__(self, graph : Graph) -> None:
        # Prey Spawn Position
        self.type = 2
        self.position = random.randint(0,49)

        # Allocate Node in graph
        graph.allocate_pos(self.position, self.type)

    def plan(self,graph : Graph, info):
        lst = list()
        lst.append(self.position)
        for el in graph.info[self.position]:
            lst.append(el)

        x = random.choice(lst)
        self.nextPosition = x
        
        