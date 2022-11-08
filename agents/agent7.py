from agents.agent1 import Agent1
from environment import Environment
import random
from graph import Graph
from graphEntity import GraphEntity
from util import get_shortest_path
from copy import deepcopy

class Agent7(GraphEntity):
    def __init__(self, graph : Graph) -> None:
        super().__init__()
        self.type = 1
        while True:
            self.position = random.randint(0,Environment.getInstance().node_count-1)
            if not graph.node_states[self.position][0] and not graph.node_states[self.position][2]:
                break
        
        self.node_count = Environment.getInstance().node_count
        # allocating position in the graph
        graph.allocate_pos(self.position,self.type)

        self.prey_belief = [1.0/self.node_count]*self.node_count
        self.predator_belief = [1.0/self.node_count]*self.node_count

        self.alpha = 0.9
        self.theta = 2

        self.first_step = True
    
    def plan(self, graph: Graph, info):
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
                self.predator_belief[node] = 0.0 if node!=info["predator"] else 1.0

        # Updating priors with the fact predator prey is not at current position

        # Predator
        # On all possible previous positions
        sum = 0.0
        for node in range(0,self.node_count):
            c = self.position in graph.info[node] or self.position==node
            # if current position is a possible move
            if c:
                self.predator_belief[node] *= 0.4*((len(graph.info[node]))/(len(graph.info[node])+1)) + 0.6*(1.0/len(close_nodes[node]) if self.position in close_nodes[node] else 0.0)
            # else it is possible always
            sum+= self.predator_belief[node]
        self.predator_belief = [x/sum for x in self.predator_belief]        
        
        # Pre
        # On all possible previous positions
        sum = 0.0
        for node in range(0,self.node_count):
            c = self.position in graph.info[node] or self.position==node
            if c:
                self.prey_belief[node] *= (len(graph.info[node]))/(len(graph.info[node])+1)
            sum+= self.prey_belief[node]
        self.prey_belief = [x/sum for x in self.prey_belief]

        survey_node = -1
        if not 1.0 in self.predator_belief:
            # Use predator beliefs when not certain about predator
            print("Using predator beliefs")
            max_val = max(self.predator_belief)
            max_beliefs = [i for i, v in enumerate(self.predator_belief) if v==max_val]

            survey_node = random.choice(max_beliefs)
        else:
            # Use predator beliefs when certain about predator
            print("Using prey beliefs")
            max_val = max(self.prey_belief)
            max_beliefs = [i for i, v in enumerate(self.prey_belief) if v==max_val]

            survey_node = random.choice(max_beliefs)
        
        survey_node_state = graph.survey(survey_node)

        survey_res = survey_node_state[2]
        # Updating Priors with fact about prey at survey location
        if not survey_res:
            sum = 0.0
            print("No prey ;_;")
            for node in range(0,self.node_count):
                s = survey_node in graph.info[node] or survey_node==node
                if s:
                    self.prey_belief[node] *= (len(graph.info[node]))/(len(graph.info[node])+1)
                sum+= self.prey_belief[node]
            
            self.prey_belief = [x/sum for x in self.prey_belief]
        else:
            print("Found ya prey!")
            if not Environment.getInstance().noisy:
                for node in range(0,self.node_count):
                    self.prey_belief[node] = 0.0 if node!=survey_node else 1.0
            else:
                sum = 0.0
                print("No prey ;_;")
                for node in range(0,self.node_count):
                    s = survey_node in graph.info[node] or survey_node==node
                    if s:
                        self.prey_belief[node] *= (len(graph.info[node]))/(len(graph.info[node])+1)
                    sum+= self.prey_belief[node]
                
                self.prey_belief = [0.1*x/sum for x in self.prey_belief]
                for node in range(0,self.node_count):
                    self.prey_belief[node] += 0.9*(0.0 if node!=survey_node else 1.0)

            
        survey_res = survey_node_state[0]
        # Updating Priors with fact that predator not at survey location
        if not survey_res:
            sum = 0.0
            print("No predator XO")
            for node in range(0,self.node_count):
                s = survey_node in graph.info[node] or survey_node==node
                
                # if survey position is a possible move
                if s:
                    self.predator_belief[node] *= 0.4*((len(graph.info[node]))/(len(graph.info[node])+1)) + 0.6*(1.0/len(close_nodes[node]) if survey_node in close_nodes[node] else 0.0)
                # else it is possible always
                sum+= self.predator_belief[node]
            self.predator_belief = [x/sum for x in self.predator_belief]
        else:
            print("Found predator! RUNN!")
            if not Environment.getInstance().noisy:
                for node in range(0,self.node_count):
                    self.predator_belief[node] = 0.0 if node!=survey_node else 1.0
            else:
                sum = 0.0
                print("No predator XO")
                for node in range(0,self.node_count):
                    s = survey_node in graph.info[node] or survey_node==node
                    
                    # if survey position is a possible move
                    if s:
                        self.predator_belief[node] *= 0.4*((len(graph.info[node]))/(len(graph.info[node])+1)) + 0.6*(1.0/len(close_nodes[node]) if survey_node in close_nodes[node] else 0.0)
                    # else it is possible always
                    sum+= self.predator_belief[node]
                self.predator_belief = [0.1*x/sum for x in self.predator_belief]
                for node in range(0,self.node_count):
                    self.predator_belief[node] += 0.9*(0.0 if node!=survey_node else 1.0)

        # Picking predator & prey positions        
        max_val = max(self.predator_belief)
        max_beliefs = [i for i, v in enumerate(self.predator_belief) if v==max_val]
        Environment.getInstance().expected_predator =  deepcopy(max_beliefs)
        predator = random.choice(max_beliefs)
        
        max_val = max(self.prey_belief)
        max_beliefs = [i for i, v in enumerate(self.prey_belief) if v==max_val]
        Environment.getInstance().expected_prey =  deepcopy(max_beliefs)
        prey = random.choice(max_beliefs)


        # Transitioning priors 
        for node in range(0, self.node_count):
            sum = 0.0
            for pr in range(0, self.node_count):
                if node in graph.info[pr] or node==pr:
                    sum += self.predator_belief[pr]*(0.4/(len(graph.info[pr])+1) + 0.6*(1.0/len(close_nodes[pr]) if node in close_nodes[pr] else 0.0))
            
            self.predator_belief[node] = sum

        for node in range(0, self.node_count):
            sum = 0.0
            for pr in range(0, self.node_count):
                if node in graph.info[pr] or node==pr:
                    sum += self.prey_belief[pr]/(len(graph.info[pr])+1)
            
            self .prey_belief[node] = sum
        
        
        print('Agent Pos Curr:', self.position)
        print('Expected Prey Position:', prey)
        print('Expected Predator Position:', predator)
        if self.first_step:
            self.first_step = False
        self.nextPosition = Agent1.get_next_position(prey,predator, graphInfo, self.position)

        

                    
                

    

        
    
    
    
        