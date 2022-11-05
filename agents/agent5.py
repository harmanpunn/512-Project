from agents.agent1 import Agent1
from environment import Environment
import random
from graph import Graph
from graphEntity import GraphEntity
from util import get_shortest_path

class Agent5(GraphEntity):
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

        self.first_step = True
    
    def plan(self, graph: Graph, info):
        # List to keep track of neighbor with closest path to agent from all possible prey position
        close_nodes = []
        graphInfo = graph.info

        for node in range(0,self.node_count):
            # Finding closest node for each prev position
            neighbor_list = graphInfo[node]
            dsts = [get_shortest_path(graphInfo, el, self.position) for el in neighbor_list]
            min_len = min(dsts)
            equal_dsts = [neighbor_list[i] for i in range(0,len(neighbor_list)) if dsts[i]==min_len  ]
            close_nodes.append(equal_dsts)

        if self.first_step:
            for node in range(0, self.node_count):
                self.belief[node] = 0.0 if node!=info["predator"] else 1.0
            self.first_step= False
        else:
            self.survey_and_update_beliefs(graph,close_nodes)                   
            # Spreading prior probabilities
            for node in range(0, self.node_count):
                sum = 0.0
                for pr in range(0, self.node_count):
                    if node in graph.info[pr] or node==pr:
                        sum += self.belief[pr]*(0.4/(len(graph.info[pr])+1) + 0.6*(1.0/len(close_nodes[pr]) if node in close_nodes[pr] else 0.0))
                
                self.belief[node] = sum

        max_val = max(self.belief)
        max_beliefs = [i for i, v in enumerate(self.belief) if v==max_val]

        predator = random.choice(max_beliefs)
        Environment.getInstance().expected_prey = max_beliefs
        prey = info['prey']
        # neighbor_list = graph[self.position]
        print("New Beliefs : ", self.belief)
        print('Agent Pos Curr:', self.position)
        print('Prey Position:', prey)
        print('Expected Predator Position:', predator)

        self.nextPosition = Agent1.get_next_position(prey,predator, graphInfo, self.position)

    def survey_and_update_beliefs(self,graph:Graph, close_nodes): 
        # Updating priors with the fact predator prey is not at current position

        # On all possible previous positions
        sum = 0.0
        for node in range(0,self.node_count):
            c = self.position in graph.info[node] or self.position==node
            # if current position is a possible move
            if c:
                self.belief[node] *= 0.4*((len(graph.info[node]))/(len(graph.info[node])+1)) + 0.6*(1.0/len(close_nodes[node]) if self.position in close_nodes[node] else 0.0)
            # else it is possible always
            sum+= self.belief[node]
        self.belief = [x/sum for x in self.belief]
        
        max_val = max(self.belief)
        max_beliefs = [i for i, v in enumerate(self.belief) if v==max_val]

        survey_node = random.choice(max_beliefs)
        survey_res = graph.survey(survey_node)
        print("Surveying : ",survey_node)

        # Updating Priors with fact that predator not at survey location
        if not survey_res:
            sum = 0.0
            print("No predator XO")
            for node in range(0,self.node_count):
                s = survey_node in graph.info[node] or survey_node==node
                
                # if survey position is a possible move
                if s:
                    self.belief[node] *= 0.4*((len(graph.info[node]))/(len(graph.info[node])+1)) + 0.6*(1.0/len(close_nodes[node]) if survey_node in close_nodes[node] else 0.0)
                # else it is possible always
                sum+= self.belief[node]
            self.belief = [x/sum for x in self.belief]
        else:
            print("Found predator! RUNN!")
            for node in range(0,self.node_count):
                self.belief[node] = 0.0 if node!=survey_node else 1.0
        
                    
                

    

        
    
    
    
        