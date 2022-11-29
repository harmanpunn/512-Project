from agents.p2.agent1 import Agent1
from environment import Environment
import random
from graph import Graph
from graphEntity import GraphEntity
from util import get_shortest_path, eprint, getNewBeliefs, transitionProbabilities
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
        # eprint("Predator prob sums: ",str(sum(self.predator_belief)))
        # eprint("Prey     prob sums: ",str(sum(self.prey_belief)))
        # eprint("Pred: ",self.predator_belief)
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
        self.predator_belief = getNewBeliefs(self.predator_belief,self.position,False)
        # Prey
        self.prey_belief = getNewBeliefs(self.prey_belief,self.position,False)

        survey_or_move = self.survey_or_move(graphInfo)
        if not Environment.getInstance().agentX or (Environment.getInstance().agentX and survey_or_move):
            survey_node = -1
            if (Environment.getInstance().agent==9 and max(self.predator_belief)<0.5) or (Environment.getInstance().agent!=9 and not 1.0 in self.predator_belief):
                # Use predator beliefs when not certain about predator
                print("Using predator beliefs")
                max_val = max(self.predator_belief)
                max_beliefs = [i for i, v in enumerate(self.predator_belief) if v==max_val]
                survey_node = random.choice(max_beliefs)
            else:
                # Use prey beliefs when certain about predator
                print("Using prey beliefs")
                max_val = max(self.prey_belief)
                max_beliefs = [i for i, v in enumerate(self.prey_belief) if v==max_val]
                survey_node = random.choice(max_beliefs)
            
            survey_node_state = graph.survey(survey_node)

            survey_res = survey_node_state[2]
            # Updating Priors with fact about prey at survey location
            self.prey_belief = getNewBeliefs(self.prey_belief,survey_node, survey_res)

            if not 1.0 in self.predator_belief:
                survey_res = survey_node_state[0]
                # Updating Priors with fact that predator not at survey location
                self.predator_belief = getNewBeliefs(self.predator_belief,survey_node,survey_res)

        knows = [0,0] 
        if max(self.predator_belief)==1.0:
            knows[0] = 1
        if max(self.prey_belief)==1.0:
            knows[1] = 1          
        
        # Transitioning priors 
        # Predator
        self.predator_belief = transitionProbabilities(self.predator_belief,graphInfo,close_nodes,True)
        # Prey
        # Transitioning prior probabilities
        self.prey_belief  = transitionProbabilities(self.prey_belief,graphInfo)


        # Picking predator & prey positions        
        max_val = max(self.predator_belief)
        max_beliefs = [i for i, v in enumerate(self.predator_belief) if v==max_val]
        Environment.getInstance().expected_predator =  deepcopy(max_beliefs)
        predator = random.choice(max_beliefs)
        
        max_val = max(self.prey_belief)
        max_beliefs = [i for i, v in enumerate(self.prey_belief) if v==max_val]
        Environment.getInstance().expected_prey =  deepcopy(max_beliefs)
        prey = random.choice(max_beliefs)

        if Environment.getInstance().agentX and survey_or_move:
            return knows

        print('Agent Pos Curr:', self.position)
        print('Expected Prey Position:', prey)
        print('Expected Predator Position:', predator)
        if self.first_step:
            self.first_step = False
        if not Environment.getInstance().careful:
            self.nextPosition = Agent1.get_next_position(prey,predator, graphInfo, self.position)
        else:
            self.nextPosition = Agent1.get_next_position(prey,deepcopy(self.predator_belief), graphInfo, self.position)
        
        return knows

    def survey_or_move(self,graphInfo):
        eprint("Predator max: ",max(self.predator_belief))
        eprint("Prey max: ",max(self.prey_belief))
        x = Agent1.getNewPredatorDist(graphInfo,self.predator_belief,self.position)
        eprint("Pred Distance : ",x)
        if x<10:
            eprint("Ight imma head out!")
            return False
        if max(self.predator_belief)<0.5 or max(self.prey_belief)<0.2:
            eprint("Still sus ;_;")
            return True
        else:
            eprint("Confidence is the key!")

            return False
            

        

                    
                

    

        
    
    
    
        