

import random
# from random import random
from graph import Graph

class Prey:
   
    def __init__(self) -> None:
        # Prey Spawn Position
        self.position = random.randint(0,49)

    def __update__(self,graph):
        lst = list()
        lst.append(self.position)
        for el in graph[self.position]:
            lst.append(el)

        x = random.choice(lst)
        self.position = x 

    def prey_position(self):
        return self.position   
        
p = Prey()
g = Graph().generate_graph()

print(p.__update__(g))
print(p.prey_position(g))

        