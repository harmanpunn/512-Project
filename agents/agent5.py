from agents.agent1 import Agent1
from environment import Environment
import random
from graph import Graph
from graphEntity import GraphEntity
from util import get_shortest_path , eprint
from collections import deque

class Agent5(GraphEntity):
    def __init__(self, graph : Graph) -> None:
        super().__init__()
        self.type = 1
        while True:
            self.position = random.randint(0,Environment.getInstance().node_count-1)
            if not graph.node_states[self.position][0] and not graph.node_states[self.position][2]:
                break
        
        # allocating position in the graph
        graph.allocate_pos(self.position,self.type)

        self.belief = [1.0/self.node_count]*self.node_count

    def plan(self, graph: Graph, info):
        # List to keep track of neighbor with closest path to agent from all possible prey position
        eprint("============= Sum of Probs : "+str(sum(self.belief))+" ===============")
        close_nodes = []
        graphInfo = graph.info

        for node in range(0,self.node_count):
            # Finding closest node for each prev position
            neighbor_list = graphInfo[node]
            dsts = [get_shortest_path(graphInfo, el, self.position) for el in neighbor_list]
            min_len = min(dsts)
            equal_dsts = [neighbor_list[i] for i in range(0,len(neighbor_list)) if dsts[i]==min_len  ]
            close_nodes.append(equal_dsts)

        self.survey_and_update_beliefs(graph,close_nodes)                   
        
        # Spreading prior probabilities
        new_belief = [0.0 for _ in range(0, self.node_count)]
        for pr in range(0,self.node_count):
            for x in graphInfo[pr]:
                new_belief[x] += self.belief[pr]*(0.6*(1/len(close_nodes[pr]) if x in close_nodes[pr] else 0.0) + 0.4/(len(graphInfo[pr])))
        self.belief = new_belief
        
        max_val = max(self.belief)
        max_beliefs = [i for i, v in enumerate(self.belief) if v==max_val]
        Environment.getInstance().expected_predator = max_beliefs
        predator = random.choice(max_beliefs)
        
        prey = info['prey']
        print('Agent Pos Curr:', self.position)
        print('Prey Position:', prey)
        print('Expected Predator Position:', predator)
        self.nextPosition = Agent1.get_next_position(prey,predator, graphInfo, self.position)

    def get_node(self):
        max_val = max(self.belief)
        max_beliefs = [i for i, v in enumerate(self.belief) if v==max_val]
        Environment.getInstance().expected_predator = max_beliefs
        return  random.choice(max_beliefs)

    def survey_and_update_beliefs(self,graph:Graph, close_nodes): 
        # Updating priors with the fact predator prey is not at current position
        sums = 0.0
        for node in range(0,self.node_count):
            if node != self.position:
                sums += self.belief[node]
            else:
                self.belief[node]=0
        self.belief = [x/sums for x in self.belief]
        
        if True or not Environment.getInstance().careful:        
            max_val = max(self.belief)
            max_beliefs = [i for i, v in enumerate(self.belief) if v==max_val]
        else:
            t = self.get_max_chunk(graph,self.chunk_size)
            max_val = max(self.belief[t:t+self.chunk_size-1])
            max_beliefs = [i for i, v in enumerate(self.belief[t:t+self.chunk_size-1]) if v==max_val]
        
        survey_node = random.choice(max_beliefs)
        survey_res = graph.survey(survey_node)[0]    
        print("Surveying : ",survey_node)

        # Updating Priors with fact that predator not at survey location
        if not survey_res:
            sums = 0.0
            print("No predator XO")
            for node in range(0,self.node_count):
                if node != survey_node:
                    sums += self.belief[node]
                else:
                    self.belief[node]=0
            self.belief = [x/sums for x in self.belief]
        else:
            print("Found predator! RUNN!")
            for node in range(0,self.node_count):
                self.belief[node] = 0.0 if node!=survey_node else 1.0
                    
                

    

        
    
    
    
        