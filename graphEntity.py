from environment import Environment
from graph import Graph

"""

Parent class for all entities in the graph

"""
class GraphEntity:

    def __init__(self) -> None:
        # Position of the entity
        self.position = -1
        # Next planned position of the entity
        self.nextPosition = None
        # Type of the entity to allocate position
        self.type = -1
        # Node count 
        self.node_count = Environment.getInstance().node_count

    # Called to update the entity in the game loop
    """
    Parameters: 
        graph -> Graph object
        info -> Environment Information
    """
    # DO NOT OVERRIDE
    def __update__(self, graph : Graph, info = None):
        self.plan(graph, info)
        self.move(graph)
    
    # Generic move logic
    # DO NOT OVERRIDE
    def move(self, graph : Graph):
        if self.nextPosition!=None:
            graph.deallocate_pos(self.position,self.type)
            graph.allocate_pos(self.nextPosition,self.type)
            self.position = self.nextPosition
        pass
    
    # Implements the core logic of the entity
    def plan(self, graph : Graph, info):
        pass

    # Getter for position
    def getPosition(self):
        return self.position
