from environment import Environment
import random
from graph import Graph
from graphEntity import GraphEntity
from util import get_shortest_path

class Agent3(GraphEntity):
    def __init__(self, graph : Graph) -> None:
        self.type = 1
        while True:
            self.position = random.randint(0,Environment.getInstance().node_count-1)
            if not graph.node_states[self.position][0] and not graph.node_states[self.position][2]:
                break
        
        self.node_count = Environment.getInstance().node_count
        # allocating position in the graph
        graph.allocate_pos(self.position,self.type)

        self.belief = [1.0/self.node_count]*self.node_count

        self.alpha = 0.9
        self.theta = 2
    
    def plan(self, graph: Graph, info):
        max_val = max(self.belief)
        max_beliefs = [i for i, v in enumerate(self.belief) if v==max_val]

        survey_node = random.choice(max_beliefs)
        survey_res = graph.survey(survey_node)
        print("Surveying : ",survey_node)
        if not survey_res:
            sum = 0.0
            print("No prey ;_;")
            for node in range(0,self.node_count):
                c = self.position in graph.info[node] or self.position==node
                s = survey_node in graph.info[node] or survey_node==node
                if ( c and not s) or (s and not c):
                    self.belief[node] *= (len(graph.info[node]))/(len(graph.info[node])+1)
                elif c and s:
                    self.belief[node] *= (len(graph.info[node])-1)/(len(graph.info[node])+1)
                
                sum+= self.belief[node]
            
            self.belief = [x/sum for x in self.belief]
        else:
            print("Found ya prey!")
            gamma = (1-self.alpha)/(1+ len(graph.info[survey_node])*self.theta)
            beta = self.theta * gamma
            for node in range(0, self.node_count):
                if node == survey_node:
                    self.belief[node] = self.alpha
                elif node in graph.info[survey_node]:
                    self.belief[node] = beta
                else:
                    self.belief[node] = gamma
                
        max_val = max(self.belief)
        max_beliefs = [i for i, v in enumerate(self.belief) if v==max_val]

        prey = random.choice(max_beliefs)
        predator = info['predator']
        graphInfo = graph.info
        # neighbor_list = graph[self.position]
        print("New Beliefs : ", self.belief)
        print('Agent Pos Curr:', self.position)
        print('Prey Position:', prey)
        print('Predator Position:', predator)
        
        curr_agent = self.position
        agent_shortest_dist_prey = get_shortest_path(graphInfo, curr_agent, prey)
        # print('agent_shortest_dist_prey:', agent_shortest_dist_prey)
        agent_shortest_dist_predator = get_shortest_path(graphInfo, curr_agent, predator)
        # print('agent_shortest_dist_predator:', agent_shortest_dist_predator)

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
            # print(key ,'->',lookup_table[key] ) 
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
        
        ls = [item for item in order_list if item is not None]
        if len(ls)==0:
            return self.position
        # print('order_list:', order_list)
        # print('first item:', ls[0])
        return ls[0]
        

                    
                

    

        
    
    
    
        