from agents.agent1 import Agent1
from environment import Environment
import random
from graph import Graph
from graphEntity import GraphEntity
from util import get_shortest_path, eprint

class Agent3(GraphEntity):
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

        self.alpha = 0.9
        self.theta = 2
    
    def plan(self, graph: Graph, info):
        # Updating priors with the fact that prey is not at current position
        eprint(" ==== Prob Sum : ",str(sum(self.belief)))

        sums = 0.0
        for node in range(0,self.node_count):
            if node != self.position:
                sums += self.belief[node]
            else:
                self.belief[node]=0
        self.belief = [x/sums for x in self.belief]
        
        # Pick max belief node to survey
        max_val = max(self.belief)
        max_beliefs = [i for i, v in enumerate(self.belief) if v==max_val]
        survey_node = random.choice(max_beliefs)
        survey_res = graph.survey(survey_node)[2]
        print("Surveying : ",survey_node)

        # Updating Priors with fact that prey not at survey location
        if not survey_res:
            sums = 0.0
            print("No prey ;_;")
            for node in range(0,self.node_count):
                if node!=survey_node:
                    sums+= self.belief[node]
                else:
                    self.belief[node]=0
            self.belief = [x/sums for x in self.belief]
        else:
            print("Found ya prey!")
            for node in range(0,self.node_count):
                self.belief[node] = 0.0 if node!=survey_node else 1.0
        
        eprint(" ==== Prob Sum 3 : ",str(sum(self.belief)))

        # Transitioning prior probabilities
        temp_beliefs = [0.0 for x in range(0,self.node_count)]
        for parent in range(0,self.node_count):
            for neigh in (graph.info[parent]+[parent]):
                temp_beliefs[neigh] += self.belief[parent]/(len(graph.info[parent])+1)        
        self.belief  = temp_beliefs

        # Selecting next move
        max_val = max(self.belief)
        max_beliefs = [i for i, v in enumerate(self.belief) if v==max_val]
        prey = random.choice(max_beliefs)
        Environment.getInstance().expected_prey = max_beliefs
        predator = info['predator']
        graphInfo = graph.info
        
        print("New Beliefs : ", self.belief)
        print('Agent Pos Curr:', self.position)
        print('Expected Prey Position:', prey)
        print('Predator Position:', predator)

        self.nextPosition = Agent1.get_next_position(prey,predator, graphInfo, self.position)

        

                    
                

    

        
    
    
    
        