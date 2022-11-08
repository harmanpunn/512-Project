import os
import sys
import random
from graph import Graph
from graphEntity import GraphEntity
from util import get_shortest_path
from environment import Environment


class Agent1(GraphEntity):
    def __init__(self, graph : Graph) -> None:
        super().__init__()
        self.type = 1
        while True:
            self.position = random.randint(0,Environment.getInstance().node_count-1)
            if not graph.node_states[self.position][0] and not graph.node_states[self.position][2]:
                break
        
        graph.allocate_pos(self.position, self.type)
    

    def plan(self, graph, info) -> None:
        prey = info['prey']
        predator = info['predator']
        graphInfo = graph.info
        # neighbor_list = graph[self.position]
        print('Agent Pos Curr:', self.position)
        print('Prey Position:', prey)
        print('Predator Position:', predator)
        self.nextPosition = Agent1.get_next_position(prey, predator, graphInfo, self.position)
        
        # self.move(graph)

    @staticmethod
    def get_next_position(prey, predator, graphInfo, curr_agent, silent = True):
        if silent:
            sys.stdout = open(os.devnull, 'w')
    
        agent_shortest_dist_prey = get_shortest_path(graphInfo, curr_agent, prey)
        print('agent_shortest_dist_prey:', agent_shortest_dist_prey)
        agent_shortest_dist_predator = get_shortest_path(graphInfo, curr_agent, predator)
        print('agent_shortest_dist_predator:', agent_shortest_dist_predator)

        neighbor_list = graphInfo[curr_agent]
        lookup_table = dict()
        min_neighbor_dist_to_prey = 9999
        min_list = list()
        for el in neighbor_list:
            # Shortest Path to prey
            path_len_to_prey = get_shortest_path(graphInfo, el, prey)
            min_list.append(path_len_to_prey)
            # Shortest Path to predator
            path_len_to_predator = get_shortest_path(graphInfo, el, predator)
            # Updating the lookup table
            lookup_table[el] = [path_len_to_predator, path_len_to_prey]

        print('curr_agent_pos:',curr_agent)
        print('lookup_table: ', lookup_table)    
        
        if Environment.getInstance().careful and agent_shortest_dist_predator >= 5:
            mn = min(min_list)
            possible_moves = [neighbor_list[i] for i in range(0,len(neighbor_list)) if min_list[i]==mn]
            print('No worries! Predator is too far way!')
            return random.choice(possible_moves)
            
        print("RUNNNNNNN!")
        order_list = [None]*6
        for key in lookup_table:
            print(key ,'->',lookup_table[key] ) 
            # Neighbor that is closer to Prey and farther from the Predator.
            if (lookup_table[key][1] < agent_shortest_dist_prey and  
                lookup_table[key][0] > agent_shortest_dist_predator):
                order_list.insert(0,key);

            # Neighbors that are closer to the Prey and not closer to the Predator.
            elif (lookup_table[key][1] < agent_shortest_dist_prey and
                lookup_table[key][0] == agent_shortest_dist_predator):    
                order_list.insert(1,key);

            # Neighbors that are not farther from the Prey and farther from the Predator.
            elif (lookup_table[key][1] == agent_shortest_dist_prey and 
                lookup_table[key][0] > agent_shortest_dist_predator):
                order_list.insert(2,key);

            # Neighbors that are not farther from the Prey and not closer to the Predator.
            elif (lookup_table[key][1] == agent_shortest_dist_prey and
                lookup_table[key][0] == agent_shortest_dist_predator):
                order_list.insert(3,key);

            # Neighbors that are farther from the Predator.
            elif (lookup_table[key][0] > agent_shortest_dist_predator):
                order_list.insert(4,key);

            # Neighbors that are not closer to the Predator.
            elif (lookup_table[key][0] == agent_shortest_dist_predator):
                order_list.insert(5,key);
        
        ls = [item for item in order_list if item is not None]
        if silent:
            sys.stdout = sys.__stdout__
        if len(ls)==0:
            return curr_agent
        # print('order_list:', order_list)
        # print('first item:', ls[0])
        return ls[0]