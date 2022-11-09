from agents.agent1 import Agent1
from environment import Environment
import random
from graph import Graph
from graphEntity import GraphEntity
from util import get_shortest_path
from collections import deque

class Agent5(GraphEntity):
    def __init__(self, graph : Graph) -> None:
        super().__init__()
        self.type = 1
        while True:
            self.position = random.randint(0,Environment.getInstance().node_count-1)
            if not graph.node_states[self.position][0] and not graph.node_states[self.position][2]:
                break
        
        # self.node_count = Environment.getInstance().node_count
        # allocating position in the graph
        graph.allocate_pos(self.position,self.type)

        self.belief = [1.0/self.node_count]*self.node_count

        self.first_step = True
        self.chunk_size = 5

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
        
        if not Environment.getInstance().careful:
            max_val = max(self.belief)
            max_beliefs = [i for i, v in enumerate(self.belief) if v==max_val]
            Environment.getInstance().expected_predator = max_beliefs
            predator = random.choice(max_beliefs)
        else:
            t = self.get_max_chunk(graph, self.chunk_size)
            dists = [get_shortest_path(graphInfo, self.position, x) for x in range(t,t+self.chunk_size)]
            min_val = min(dists)
            print("+++++++++++++  Min Dists: ",str(min_val)," +++++++++++++++++++++++++=")
            
            Environment.getInstance().expected_predator = [i for i in range(t,t+self.chunk_size)]
            if t<= self.position and self.position <t+self.chunk_size:
                predator = t
            elif dists[0]<dists[self.chunk_size-1]:
                predator = t
            else:
                predator = t+self.chunk_size-1
        
        # Transitioning priors
        for node in range(0, self.node_count):
            sum = 0.0
            for pr in range(0, self.node_count):
                if node in graph.info[pr] or node==pr:
                    sum += self.belief[pr]*(0.4/(len(graph.info[pr])+1) + 0.6*(1.0/len(close_nodes[pr]) if node in close_nodes[pr] else 0.0))
            
            self.belief[node] = sum

        prey = info['prey']
        # neighbor_list = graph[self.position]
        # print("New Beliefs : ", self.belief)
        print('Agent Pos Curr:', self.position)
        print('Prey Position:', prey)
        print('Expected Predator Position:', predator)
        self.nextPosition = Agent1.get_next_position(prey,predator, graphInfo, self.position)

    def get_node(self):
        max_val = max(self.belief)
        max_beliefs = [i for i, v in enumerate(self.belief) if v==max_val]
        Environment.getInstance().expected_predator = max_beliefs
        return  random.choice(max_beliefs)

    def get_max_chunk(self,graph:Graph,chunk_size):
        i = 0
        mxProb = 0.0
        mxChunks = []
        while i<self.node_count:
            tmp = self.belief[i:i+chunk_size-1]
            chunkProb = sum(tmp)
            if mxProb < chunkProb:
                mxProb = chunkProb
            i+=chunk_size
        i=0
        while i<self.node_count:
            tmp = self.belief[i:i+chunk_size-1]
            chunkProb = sum(tmp)
            if mxProb == chunkProb:
                mxChunks.append(i)
            i+=chunk_size
        return random.choice(mxChunks)            
                
            
    
    def get_max_belief_in_neigh(self, graph:Graph, range:int):
        fringe = deque()

        fringe.append(self.position)
        closed_set = {}
        steps = 0

        mx = float("-inf")

        while len(fringe)!=0 and steps<=range:
            steps+=1
            top = fringe.pop()

            closed_set[top] = True

            for x in graph.info[top]:
                if x not in closed_set or not closed_set[x]:
                    fringe.append(x)
                    mx = max(mx, self.belief[x])

        return mx

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
        
        if not Environment.getInstance().careful:        
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

                    
                

    

        
    
    
    
        