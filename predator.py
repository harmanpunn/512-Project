from environment import Environment
import random
# from random import random
from turtle import distance

from graph import Graph
from graphEntity import GraphEntity
from util import get_shortest_path

class Predator(GraphEntity):
    

    def __init__(self, graph) -> None:
        super().__init__()    
        self.type = 0
        self.position = random.randint(0,Environment.getInstance().node_count-1)
        graph.allocate_pos(self.position,self.type)
    
    '''
    Update the predator's position such that it moves to a neighbor node
    with shortest distance to agent 
    '''
    def plan(self, graph, info):
        
        agent_position = info['agent']
        graphInfo = graph.info
        
        neighbor_list = graphInfo[self.position]
        next_position = random.choice(neighbor_list)
        if (Environment.getInstance().agent>=5 and random.random()<=0.6) or Environment.getInstance().agent<5:
            dsts = [get_shortest_path(graphInfo, el, agent_position) for el in neighbor_list]
            min_len = min(dsts)

            equal_dsts = [neighbor_list[i] for i in range(0,len(neighbor_list)) if dsts[i]==min_len  ]
            next_position = random.choice(equal_dsts)                
            
        # Update position of the predator
        self.nextPosition = next_position
