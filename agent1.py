    
from util import get_shortest_path


class Agent1:
    def __init__(self, graph, prey, predator) -> None:

        while True:
            self.position = graph.allocate_pos();
            if (self.position != prey.prey_position and 
                self.position != predator.predator_position):
                break
    

    def __update__(self, graph, prey, predator) -> None:
        
        # neighbor_list = graph[self.position]
        print('Agent Pos Curr:', self.position)
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

        
            




        print('lookup_table:', lookup_table)    



        




    def agent_postion(self):
        return self.position