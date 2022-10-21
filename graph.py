
from collections import defaultdict
import random
from random import choice
from time import sleep

from environment import Environment

class Graph:

    def __init__(self) -> None:
        self.e_count = 0
        self.node_count = Environment.getInstance()

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
                a = (node+1)%self.node_count
                b = (node+5)%self.node_count 
                lst = [i for i in range(min(a,b),max(a,b)+1) if i in node_list]
                forward_node = random.choice(lst) if lst else None

                a = (node-1 + self.node_count) % self.node_count
                b = (node-5 + self.node_count) % self.node_count 
                backward_node = random.choice(lst) if lst else None

                if forward_node is None and backward_node is None:
                    continue
                elif forward_node is None:
                    chosen_node = backward_node
                elif backward_node is None:
                    chosen_node = forward_node
                else:
                    chosen_node = random.choice([forward_node, backward_node])

                chosen_node_degree = len(graph[chosen_node])

                if chosen_node and node != chosen_node and chosen_node_degree < 3:
                    # Connect an edge between node and chosen_node
                    self.add_edge(graph, node, chosen_node)
                    node_list.remove(node)
                    node_list.remove(chosen_node) 
            trial+=1    

        return graph    

    def add_edge(self,graph,u,v):
        if v not in graph[u]:
            graph[u].append(v)
        if u not in graph[v]:    
            graph[v].append(u)
        self.e_count+=1