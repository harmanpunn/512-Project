from random import random

class Predator:

    def __init__(self) -> None:
        self.position = random.randint(0,49)

    def __update__(self, graph, agent_position):
        


