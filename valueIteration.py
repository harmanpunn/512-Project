from collections import defaultdict
from random import *
from environment import Environment
from graph import Graph
from util import get_shortest_path

# environment = Environment(False,5)
# graph = Graph()


def getValues(graph: Graph):
    values = {}
    prob_matrix = {}
    for agent in range(0, Environment.getInstance().node_count):
            for prey in range(0, Environment.getInstance().node_count):
                for predator in range(0, Environment.getInstance().node_count):
                    values[(agent, prey, predator)] = randint(0,99)
                    if agent==predator:
                        values[(agent, prey, predator)] = 9999
                    if agent == prey and agent!=predator:
                        values[(agent, prey, predator)] = 0


    states = values.keys()   
    for state in states:
        probs = {}
        actions = graph.info[state[0]] + [state[0]]
        for action in actions:
            action_probs = {}
            prey_options = graph.info[state[1]] + [state[1]]
            predator_options = graph.info[state[2]]
            neigh_dist = []
            for neigh in predator_options:
                neigh_dist.append(get_shortest_path(graph.info, neigh, action))

            predator_close = [predator_options[i] for i in range(
                0, len(predator_options)) if neigh_dist[i] == min(neigh_dist)]

            for p in prey_options:
                for r in predator_options:
                    action_probs[(action, p, r)] = (1/len(prey_options))*(0.6*(1/len(predator_close)
                                                                                 if r in predator_close else 0.0)+0.4/len(predator_options))
            probs[action] = action_probs
        prob_matrix[state] = probs 


    i = 0  
    p = None
    while p!=0:
        print('p:', p)
        p = 0.0
        for state in states:
            if state[0]==state[2]:
                continue
            if state[0] == state[1] and state[0]!=state[2]:
                continue
            min_val = float('inf')
            for action in prob_matrix[state].keys():
                val = 1
                for s_prime in prob_matrix[state][action].keys():
                    val += prob_matrix[state][action][s_prime]*values[s_prime]

                min_val = min(val, min_val)    

            p += (min_val - values[state]) ** 2
            
            values[state] = min_val
        i+=1
    return values, prob_matrix

def getPolicyFromValues(values, prob_matrix):
    policy = {}
    for state in values.keys():
        min_val = float('inf')
        for action in prob_matrix[state].keys():
            val = 1
            for s_prime in prob_matrix[state][action].keys():
                val += prob_matrix[state][action][s_prime]*values[s_prime]

            if min_val > val:
                policy[state] = action
                min_val = min(val, min_val)

    return policy
    

# values, probMatrix = getValues()         
# print(getPolicyFromValues(values,probMatrix))