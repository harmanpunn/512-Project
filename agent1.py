    
from util import get_shortest_path


class Agent1:
    def __init__(self, graph, prey, predator) -> None:

        while True:
            self.position = graph.allocate_pos();
            if (self.position != prey.prey_position() and 
                self.position != predator.predator_position()):
                break
    

    def __update__(self, graph, prey, predator) -> None:
        
        # neighbor_list = graph[self.position]
        print('Agent Pos Curr:', self.position)
        print('Prey Position:', prey.prey_position())
        print('Predator Position:', predator.predator_position())
        
        curr_agent = self.position
        agent_shortest_dist_prey = get_shortest_path(graph, curr_agent, prey.prey_position())
        print('agent_shortest_dist_prey:', agent_shortest_dist_prey)
        agent_shortest_dist_predator = get_shortest_path(graph, curr_agent, predator.predator_position())
        print('agent_shortest_dist_predator:', agent_shortest_dist_predator)

        neighbor_list = graph[self.position]
        lookup_table = dict()
        for el in neighbor_list:
            # Shortest Path to prey
            path_len_to_prey = get_shortest_path(graph, el, prey.prey_position())
            # Shortest Path to predator
            path_len_to_predator = get_shortest_path(graph, el, predator.predator_position())
            # Updating the lookup table
            lookup_table[el] = [path_len_to_predator, path_len_to_prey]

        next_position = self.get_next_position(lookup_table, agent_shortest_dist_prey, agent_shortest_dist_predator)
        print('next_position',next_position)
        self.position = next_position 
    

    def get_next_position(self, lookup_table, agent_shortest_dist_prey, agent_shortest_dist_predator):
        next_position = self.position
        for key in lookup_table:
            print(key ,'->',lookup_table[key] ) 
            # Neighbor that is closer to Prey and farther from the Predator.
            if (lookup_table[key][1] < agent_shortest_dist_prey and  
                lookup_table[key][0] > agent_shortest_dist_predator):
                next_position = key
                break

            # Neighbors that are closer to the Prey and not closer to the Predator.
            elif (lookup_table[key][1] < agent_shortest_dist_prey and
                lookup_table[key][0] == agent_shortest_dist_predator):    
                next_position = key
                break

            # Neighbors that are not farther from the Prey and farther from the Predator.
            elif (lookup_table[key][1] == agent_shortest_dist_prey and 
                lookup_table[key][0] > agent_shortest_dist_predator):
                next_position = key
                break

            # Neighbors that are not farther from the Prey and not closer to the Predator.
            elif (lookup_table[key][1] == agent_shortest_dist_prey and
                lookup_table[key][0] == agent_shortest_dist_predator):
                next_position = key
                break

            # Neighbors that are farther from the Predator.
            elif (lookup_table[key][0] > agent_shortest_dist_predator):
                next_position = key 
                break

            # Neighbors that are not closer to the Predator.
            elif (lookup_table[key][0] == agent_shortest_dist_predator):
                next_position = key
                break  


        return next_position

    def agent_postion(self):
        return self.position