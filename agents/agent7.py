from agents.agent1 import Agent1
from environment import Environment
import random
from graph import Graph
from graphEntity import GraphEntity
from util import get_shortest_path, eprint
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

        self.first_step = True
    
    def plan(self, graph: Graph, info):
        eprint("Predator prob sums: ",str(sum(self.predator_belief)))
        eprint("Prey     prob sums: ",str(sum(self.prey_belief)))
        eprint("Pred: ",self.predator_belief)
        close_nodes = []
        graphInfo = graph.info

        for node in range(0,self.node_count):
            # Finding closest node for each prev position
            neighbor_list = graphInfo[node]
            dsts = [get_shortest_path(graphInfo, el, self.position) for el in neighbor_list]
            min_len = min(dsts)
            equal_dsts = [neighbor_list[i] for i in range(0,len(neighbor_list)) if dsts[i]==min_len  ]
            close_nodes.append(equal_dsts)

        # Updating priors with the fact predator / prey is not at current position
        # Predator
        sums = 0.0
        for node in range(0,self.node_count):
            if node != self.position:
                sums += self.predator_belief[node]
            else:
                self.predator_belief[node]=0
        self.predator_belief = [x/sums for x in self.predator_belief]
        # Prey
        sums = 0.0
        for node in range(0,self.node_count):
            if node != self.position:
                sums += self.prey_belief[node]
            else:
                self.prey_belief[node]=0
        self.prey_belief = [x/sums for x in self.prey_belief]

        survey_node = -1
        if (Environment.getInstance().agent==9 and max(self.predator_belief)<0.7) or (Environment.getInstance().agent!=9 and not 1.0 in self.predator_belief):
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
            print("No prey ;_;")
            sums = 0.0
            for node in range(0,self.node_count):
                if node != survey_node:
                    sums += self.prey_belief[node]
                else:
                    self.prey_belief[node]=0
            self.prey_belief = [x/sums for x in self.prey_belief]
        else:
            print("Found ya prey!")
            if not (Environment.getInstance().noisy_agent and Environment.getInstance().noisy):
                for node in range(0,self.node_count):
                    self.prey_belief[node] = 0.0 if node!=survey_node else 1.0
            else:
                sums = 0.0
                for node in range(0,self.node_count):
                    if node != survey_node:
                        sums += self.prey_belief[node]
                    else:
                        self.prey_belief[node]=0
                self.prey_belief = [0.9*(0.0 if i!=survey_node else 1.0) + 0.1*self.prey_belief[i]/sums for i in range(0,self.node_count)]
                

        if not 1.0 in self.predator_belief:
            survey_res = survey_node_state[0]
            # Updating Priors with fact that predator not at survey location
            if not survey_res:
                print("No predator XO")
                sums = 0.0
                prev = deepcopy(self.predator_belief)
                # eprint(prev," : ",survey_node)
                for node in range(0,self.node_count):
                    if node != survey_node:
                        sums += self.predator_belief[node]
                    else:
                        self.predator_belief[node]=0
                try:
                    self.predator_belief = [x/sums for x in self.predator_belief]
                except ZeroDivisionError:
                    eprint(prev," : ",survey_node)
                    raise ZeroDivisionError()
            else:
                print("Found predator! RUNN!")
                if not (Environment.getInstance().noisy_agent and Environment.getInstance().noisy):
                    for node in range(0,self.node_count):
                        self.predator_belief[node] = 0.0 if node!=survey_node else 1.0
                else:
                    temp_beliefs = [0.0 for _ in range(0,self.node_count)]
                    for node in range(0,self.node_count):
                        temp_beliefs[node] = 0.9*(0.0 if node!=survey_node else 1.0)
                    
                    temp_beliefs1 = [0.0 for _ in range(0,self.node_count)]
                    for node in range(0,self.node_count):
                        if node != survey_node:
                            sums += self.predator_belief[node]
                        else:
                            temp_beliefs1[node]=0.0
                    temp_beliefs1 = [0.1*x/sums for x in self.prey_belief]

                    self.predator_belief = [temp_beliefs[node] + temp_beliefs1[node] for node in range(0, self.node_count)]
        # Transitioning priors 
        # Predator
        new_belief = [0.0 for _ in range(0, self.node_count)]
        for pr in range(0,self.node_count):
            for x in graphInfo[pr]:
                new_belief[x] += self.predator_belief[pr]*(0.6*(1/len(close_nodes[pr]) if x in close_nodes[pr] else 0.0) + 0.4/(len(graphInfo[pr])))
        self.predator_belief = new_belief
        # Prey
        # Transitioning prior probabilities
        temp_beliefs = [0.0 for _ in range(0,self.node_count)]
        for parent in range(0,self.node_count):
            for neigh in (graph.info[parent]+[parent]):
                temp_beliefs[neigh] += self.prey_belief[parent]/(len(graph.info[parent])+1)        
        self.prey_belief  = temp_beliefs

        
        # Picking predator & prey positions        
        max_val = max(self.predator_belief)
        max_beliefs = [i for i, v in enumerate(self.predator_belief) if v==max_val]
        Environment.getInstance().expected_predator =  deepcopy(max_beliefs)
        predator = random.choice(max_beliefs)
        
        max_val = max(self.prey_belief)
        max_beliefs = [i for i, v in enumerate(self.prey_belief) if v==max_val]
        Environment.getInstance().expected_prey =  deepcopy(max_beliefs)
        prey = random.choice(max_beliefs)


        print('Agent Pos Curr:', self.position)
        print('Expected Prey Position:', prey)
        print('Expected Predator Position:', predator)
        if self.first_step:
            self.first_step = False
        self.nextPosition = Agent1.get_next_position(prey,predator, graphInfo, self.position)

        

                    
                

    

        
    
    
    
        