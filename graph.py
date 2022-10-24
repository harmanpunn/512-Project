
from collections import defaultdict
import random
from random import choice
from time import sleep

from environment import Environment

class Graph:

    def __init__(self) -> None:
        self.node_count = Environment.getInstance().node_count

        self.info = self.generate_graph()
        self.node_states = {}
        for i in range(0,50):
            self.node_states[i] = [False, False, False]

    def generate_graph(self):
        graph = defaultdict(list)
        trial = 0
        node_list = list()
        # Graph connected in a large cirle
        for i in range(0,self.node_count):
            node_list.append(i)
            graph[i].append((i+1)%self.node_count)
            graph[i].append((i-1 + self.node_count)%self.node_count)

        while len(node_list) > 0 and trial < 100:
            node = random.choice(node_list)
            node_degree = len(graph[node])

            if node and node_degree < 3:
                lst = []
                for offset in range(-5,6):
                    if offset!=0:
                        lst.append((node-offset)%self.node_count)
                
                if not (len(list(filter(lambda l : len(graph[l])<3 and not l in graph[node],lst))) == 0):
                    chosen_node = random.choice(lst)
                    while len(graph[chosen_node])>=3 or chosen_node in graph[node]:
                        chosen_node = random.choice(lst)
                    

                    graph[node].append(chosen_node)
                    graph[chosen_node].append(node)
                    node_list.remove(chosen_node)

                node_list.remove(node)
            trial+=1    

        return graph    

    def allocate_pos(self, x: int, k : int):
        self.node_states[x][k] = True