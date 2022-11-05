from environment import Environment
import random
# from random import random
from turtle import distance

from graph import Graph
from graphEntity import GraphEntity
from util import get_shortest_path

class Predator(GraphEntity):
    

    def __init__(self, graph) -> None:
        super().__init__()    
        self.type = 0
        self.position = random.randint(0,Environment.getInstance().node_count-1)
        graph.allocate_pos(self.position,self.type)
    
    '''
    Update the predator's position such that it moves to a neighbor node
    with shortest distance to agent 
    '''
    def plan(self, graph, info):
        
        agent_position = info['agent']
        graphInfo = graph.info
        
        neighbor_list = graphInfo[self.position]
        dsts = [get_shortest_path(graphInfo, el, agent_position) for el in neighbor_list]
        min_len = min(dsts)

        equal_dsts = [neighbor_list[i] for i in range(0,len(neighbor_list)) if dsts[i]==min_len  ]
        next_position = random.choice(equal_dsts)                

        '''
        src = self.position
        dest = agent_position
        distance = []
        predecessor = list()

        for i in range(len(graphInfo)):
            distance.insert(i,9999)
            predecessor.insert(i,-1)

        if self.shortest_path(graphInfo, src, dest, distance, predecessor):
            print('Short path is available')
            path = []
            j = dest
            path.append(j)

            while predecessor[j] != -1:
                path.append(predecessor[j])
                j = predecessor[j]


            print("Shortest path : ", path)
            print('New Position:', path[len(path) - 2])
        '''
        # Update position of the predator
        self.nextPosition = next_position


    def shortest_path(self, graph, src, dest, distance, predecessor):
        queue = []
        visited = [False for i in range(len(graph))]

        queue.append(src)
        distance[src] = 0
        visited[src] = True

        print('src:', src)
        while len(queue) != 0:
            curr = queue[0]
            queue.pop(0)

            for i in range(len(graph[curr])):
                
                if visited[graph[curr][i]] == False:
                    distance[graph[curr][i]] = distance[curr] + 1
                    predecessor[graph[curr][i]] = curr
                    visited[graph[curr][i]] = True
                    queue.append(graph[curr][i])

                    if graph[curr][i] == dest:
                        return True

        return False

