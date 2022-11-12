import os
import sys
import random
from graph import Graph
from graphEntity import GraphEntity
from util import get_shortest_path
from environment import Environment


class Agent1(GraphEntity):
    def __init__(self, graph : Graph) -> None:
        super().__init__()
        self.type = 1
        while True:
            self.position = random.randint(0,Environment.getInstance().node_count-1)
            if not graph.node_states[self.position][0] and not graph.node_states[self.position][2]:
                break
        
        graph.allocate_pos(self.position, self.type)
    

    def plan(self, graph, info) -> None:
        prey = info['prey']
        predator = info['predator']
        graphInfo = graph.info
        # neighbor_list = graph[self.position]
        print('Agent Pos Curr:', self.position)
        print('Prey Position:', prey)
        print('Predator Position:', predator)
        self.nextPosition = Agent1.get_next_position(prey, predator, graphInfo, self.position)
        
        # self.move(graph)

    @staticmethod
    def get_next_position(prey, predator, graphInfo, curr_agent):
        if Environment.getInstance().agent<8:
            agent_shortest_dist_prey = get_shortest_path(graphInfo, curr_agent, prey)
        else:
            agent_shortest_dist_prey = Agent1.getExpectedDist(graphInfo, prey, curr_agent)
        print('agent_shortest_dist_prey:', agent_shortest_dist_prey)
        # Shortest Path to predator
        if Environment.getInstance().agent>5 and Environment.getInstance().careful :
            agent_shortest_dist_predator = Agent1.getExpectedDist(graphInfo,predator,curr_agent)
        else:
            agent_shortest_dist_predator = get_shortest_path(graphInfo, curr_agent, predator)

        print('agent_shortest_dist_predator:', agent_shortest_dist_predator)

        neighbor_list = graphInfo[curr_agent]
        lookup_table = dict()
        for el in neighbor_list:
            
            # Shortest Path to prey
            if Environment.getInstance().agent<8:
                path_len_to_prey = get_shortest_path(graphInfo, el, prey)
            else:
                path_len_to_prey = Agent1.getNewPreyDist(graphInfo, prey, el)

            # Shortest Path to predator
            if Environment.getInstance().agent>5 and Environment.getInstance().careful:
                path_len_to_predator = Agent1.getNewPredatorDist(graphInfo,predator,el)
            else:
                path_len_to_predator = get_shortest_path(graphInfo, el, predator)
            
            # Updating the lookup table
            lookup_table[el] = [path_len_to_predator, path_len_to_prey]

        print('curr_agent_pos:',curr_agent)
        print('lookup_table: ', lookup_table)

        print("RUNNNNNNN!")
        order_list = [[] for _ in range(0,6)]
        close_to_prey = []
        for key in lookup_table:
            print(key ,'->',lookup_table[key] ) 
            # Neighbor that is closer to Prey and farther from the Predator.
            if (lookup_table[key][1] < agent_shortest_dist_prey and  
                lookup_table[key][0] > agent_shortest_dist_predator):
                order_list[0].append(key)

            # Neighbors that are closer to the Prey and not closer to the Predator.
            if (lookup_table[key][1] < agent_shortest_dist_prey and
                lookup_table[key][0] == agent_shortest_dist_predator):    
                order_list[1].append(key)

            # Neighbors that are not farther from the Prey and farther from the Predator.
            if (lookup_table[key][1] == agent_shortest_dist_prey and 
                lookup_table[key][0] > agent_shortest_dist_predator):
                order_list[2].append(key)

            # Neighbors that are not farther from the Prey and not closer to the Predator.
            if (lookup_table[key][1] == agent_shortest_dist_prey and
                lookup_table[key][0] == agent_shortest_dist_predator):
                order_list[3].append(key)

            # Neighbors that are farther from the Predator.
            if (lookup_table[key][0] > agent_shortest_dist_predator):
                order_list[4].append(key)

            # Neighbors that are not closer to the Predator.
            if (lookup_table[key][0] == agent_shortest_dist_predator):
                order_list[5].append(key)

            # Neighbors that not farther from the prey.
            if (lookup_table[key][1] <= agent_shortest_dist_prey):
                close_to_prey.append(key)

        print(order_list)
        ls = [item for item in order_list if len(item)!=0]
        if Environment.getInstance().careful and len(ls)==0:
            return random.choice(close_to_prey)
        if len(ls)==0:
            return curr_agent
        # print('order_list:', order_list)
        # print('first item:', ls[0])
        return random.choice(ls[0])

    @staticmethod
    def getNewPredatorDist(graphInfo,predator,agent):
        # easily Distracted predator
        if Environment.getInstance().agent>=5:
            # return expected distance
            totalExpectedDist = 0.0
            for j in range(0,len(predator)):
                neighbors = graphInfo[j]
                dists = []
                for n in neighbors:
                    dists.append(get_shortest_path(graphInfo,n,agent))
                
                mnDist = min(dists)
                nums = len([x for x in dists if x==mnDist])
                expectedDist = 0.0
                for i in range(0,len(neighbors)):
                    expectedDist += dists[i]/len(neighbors)
                totalExpectedDist += predator[j]*expectedDist
            return totalExpectedDist
        else:
            neighbors = graphInfo[predator]
            dists = []
            for n in neighbors:
                dists.append(get_shortest_path(graphInfo,n,agent))
            
            mnDist = min(dists)
            return mnDist

    @staticmethod
    def getNewPreyDist(graphInfo,prey,agent):
        # easily Distracted predator
        if Environment.getInstance().agent>=5:
            # return expected distance
            totalExpectedDist = 0.0
            for j in range(0,len(prey)):
                neighbors = graphInfo[j]
                dists = []
                for n in neighbors:
                    dists.append(get_shortest_path(graphInfo,n,agent))
                
                mnDist = min(dists)
                nums = len([x for x in dists if x==mnDist])
                expectedDist = 0.0
                for i in range(0,len(neighbors)):
                    n = neighbors[i]
                    s = 0
                    if dists[i]==mnDist:
                        s+= 0.6*(1/nums)
                    s+= 0.4/len(neighbors)
                    expectedDist += s*dists[i]
                totalExpectedDist += prey[j]*expectedDist
            return totalExpectedDist
        else:
            neighbors = graphInfo[prey]
            dists = []
            for n in neighbors:
                dists.append(get_shortest_path(graphInfo,n,agent))
            
            mnDist = min(dists)
            return mnDist

    @staticmethod
    def getExpectedDist(graphInfo, predator, curr_agent):
        expectedDist = 0.0
        for i in range(0, len(predator)):
            expectedDist += predator[i]*get_shortest_path(graphInfo,i,curr_agent)
        return expectedDist


