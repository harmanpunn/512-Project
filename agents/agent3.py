from msilib.schema import Environment
import random
from graph import Graph
from graphEntity import GraphEntity

class Agent3(GraphEntity):
    def __init__(self, graph : Graph) -> None:
        self.type = 1
        while True:
            self.position = random.randint(0,Environment.getInstance().node_count-1)
            if not graph.node_states[self.position][0] and not graph.node_states[self.position][2]:
                break
        