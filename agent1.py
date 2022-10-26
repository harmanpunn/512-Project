import random
from graph import Graph
from graphEntity import GraphEntity
from util import get_shortest_path


class Agent1(GraphEntity):
    def __init__(self, graph : Graph) -> None:
        self.type = 1
        while True:
            self.position = random.randint(0,49)
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
        
        curr_agent = self.position
        agent_shortest_dist_prey = get_shortest_path(graphInfo, curr_agent, prey)
        print('agent_shortest_dist_prey:', agent_shortest_dist_prey)
        agent_shortest_dist_predator = get_shortest_path(graphInfo, curr_agent, predator)
        print('agent_shortest_dist_predator:', agent_shortest_dist_predator)

        neighbor_list = graphInfo[self.position]
        lookup_table = dict()
        for el in neighbor_list:
            # Shortest Path to prey
            path_len_to_prey = get_shortest_path(graphInfo, el, prey)
            # Shortest Path to predator
            path_len_to_predator = get_shortest_path(graphInfo, el, predator)
            # Updating the lookup table
            lookup_table[el] = [path_len_to_predator, path_len_to_prey]

        self.nextPosition = self.get_next_position(lookup_table, agent_shortest_dist_prey, agent_shortest_dist_predator)
        
        # self.move(graph)

    def get_next_position(self, lookup_table, agent_shortest_dist_prey, agent_shortest_dist_predator):
        next_position = self.position
        order_list = [None]*6
        for key in lookup_table:
            print(key ,'->',lookup_table[key] ) 
            # Neighbor that is closer to Prey and farther from the Predator.
            if (lookup_table[key][1] < agent_shortest_dist_prey and  
                lookup_table[key][0] > agent_shortest_dist_predator):
                next_position = key
                order_list.insert(0,key);

            # Neighbors that are closer to the Prey and not closer to the Predator.
            elif (lookup_table[key][1] < agent_shortest_dist_prey and
                lookup_table[key][0] == agent_shortest_dist_predator):    
                next_position = key
                order_list.insert(1,key);

            # Neighbors that are not farther from the Prey and farther from the Predator.
            elif (lookup_table[key][1] == agent_shortest_dist_prey and 
                lookup_table[key][0] > agent_shortest_dist_predator):
                next_position = key
                order_list.insert(2,key);

            # Neighbors that are not farther from the Prey and not closer to the Predator.
            elif (lookup_table[key][1] == agent_shortest_dist_prey and
                lookup_table[key][0] == agent_shortest_dist_predator):
                next_position = key
                order_list.insert(3,key);

            # Neighbors that are farther from the Predator.
            elif (lookup_table[key][0] > agent_shortest_dist_predator):
                next_position = key 
                order_list.insert(4,key);

            # Neighbors that are not closer to the Predator.
            elif (lookup_table[key][0] == agent_shortest_dist_predator):
                next_position = key
                order_list.insert(5,key);

        print('order_list:', order_list)
        print('first item:', next(item for item in order_list if item is not None))
        return next(item for item in order_list if item is not None)