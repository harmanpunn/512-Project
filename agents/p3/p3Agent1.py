from graphEntity import GraphEntity
from graph import Graph
from environment import Environment
from util import get_shortest_path
import random

from time import sleep


class P3Agent1(GraphEntity):

    someBigNumber = 200

    def __init__(self, graph: Graph) -> None:
        # super.__init__()
        self.type = 1

        graphInfo = graph.info
        self.policy = {}

        for agent in range(0, Environment.getInstance().node_count):
            for prey in range(0, Environment.getInstance().node_count):
                for predator in range(0, Environment.getInstance().node_count):
                    self.policy[(agent, prey, predator)] = random.choice(
                        graphInfo[agent]+[agent])
        # print(graph.info)
        graph.info = {0: [1, 4, 2], 1: [2, 0, 4],
                      2: [3, 1, 0], 3: [4, 2], 4: [0, 3, 1]}
        self.policy = {(0, 0, 0): 2, (0, 0, 1): 0, (0, 0, 2): 4, (0, 0, 3): 0, (0, 0, 4): 4, (0, 1, 0): 1, (0, 1, 1): 4, (0, 1, 2): 1, (0, 1, 3): 2, (0, 1, 4): 4, (0, 2, 0): 1, (0, 2, 1): 4, (0, 2, 2): 4, (0, 2, 3): 1, (0, 2, 4): 4, (0, 3, 0): 0, (0, 3, 1): 0, (0, 3, 2): 2, (0, 3, 3): 2, (0, 3, 4): 1, (0, 4, 0): 2, (0, 4, 1): 4, (0, 4, 2): 1, (0, 4, 3): 4, (0, 4, 4): 2, (1, 0, 0): 2, (1, 0, 1): 2, (1, 0, 2): 1, (1, 0, 3): 0, (1, 0, 4): 1, (1, 1, 0): 1, (1, 1, 1): 4, (1, 1, 2): 4, (1, 1, 3): 1, (1, 1, 4): 1, (1, 2, 0): 1, (1, 2, 1): 1, (1, 2, 2): 2, (1, 2, 3): 0, (1, 2, 4): 1, (1, 3, 0): 0, (1, 3, 1): 2, (1, 3, 2): 1, (1, 3, 3): 0, (1, 3, 4): 0, (1, 4, 0): 2, (1, 4, 1): 0, (1, 4, 2): 0, (1, 4, 3): 2, (1, 4, 4): 1, (2, 0, 0): 1, (2, 0, 1): 2, (2, 0, 2): 3, (2, 0, 3): 2, (2, 0, 4): 2, (2, 1, 0): 2, (2, 1, 1): 1, (2, 1, 2): 2, (2, 1, 3): 2, (2, 1, 4): 3, (2, 2, 0): 0, (2, 2, 1): 1, (
            2, 2, 2): 1, (2, 2, 3): 2, (2, 2, 4): 3, (2, 3, 0): 2, (2, 3, 1): 1, (2, 3, 2): 0, (2, 3, 3): 1, (2, 3, 4): 3, (2, 4, 0): 0, (2, 4, 1): 0, (2, 4, 2): 3, (2, 4, 3): 3, (2, 4, 4): 0, (3, 0, 0): 4, (3, 0, 1): 4, (3, 0, 2): 2, (3, 0, 3): 3, (3, 0, 4): 4, (3, 1, 0): 3, (3, 1, 1): 2, (3, 1, 2): 3, (3, 1, 3): 4, (3, 1, 4): 3, (3, 2, 0): 4, (3, 2, 1): 4, (3, 2, 2): 3, (3, 2, 3): 2, (3, 2, 4): 3, (3, 3, 0): 3, (3, 3, 1): 3, (3, 3, 2): 2, (3, 3, 3): 4, (3, 3, 4): 3, (3, 4, 0): 4, (3, 4, 1): 4, (3, 4, 2): 3, (3, 4, 3): 3, (3, 4, 4): 4, (4, 0, 0): 0, (4, 0, 1): 1, (4, 0, 2): 0, (4, 0, 3): 0, (4, 0, 4): 1, (4, 1, 0): 1, (4, 1, 1): 4, (4, 1, 2): 0, (4, 1, 3): 3, (4, 1, 4): 1, (4, 2, 0): 3, (4, 2, 1): 1, (4, 2, 2): 3, (4, 2, 3): 0, (4, 2, 4): 4, (4, 3, 0): 1, (4, 3, 1): 1, (4, 3, 2): 4, (4, 3, 3): 0, (4, 3, 4): 0, (4, 4, 0): 3, (4, 4, 1): 1, (4, 4, 2): 0, (4, 4, 3): 3, (4, 4, 4): 3}
        print(P3Agent1.calculateValues(self.policy, graph))

    @staticmethod
    def calculateValues(policy, graph: Graph):
        
        # values of the states
        values = {}
        # marked when value is calculated
        done = {}
        # storing new state probs of a state
        neigborsProbs = {}

        # sort states based on prey & agent distance
        def sortStates(state):
            return get_shortest_path(graph.info, state[0], state[1])
        states = list(policy.keys())
        states.sort(key=sortStates)

        # for each state
        for state in policy.keys():
            if state[2] == state[0]:
                values[state] = P3Agent1.someBigNumber
                done[state] = True
            else:
                if state[1] == state[0]:
                    values[state] = 0
                    done[state] = True
                else:
                    values[state] = 0
                    done[state] = False

            probs = {}
            prey_options = graph.info[state[1]] + [state[1]]
            predator_options = graph.info[state[2]]

            dists = []
            for opt in predator_options:
                dists.append(get_shortest_path(graph.info, opt, policy[state]))

            predator_nearest_neighs = [predator_options[i] for i in range(
                0, len(predator_options)) if dists[i] == min(dists)]

            for pr in prey_options:
                for pred in predator_options:
                    probs[(policy[state], pr, pred)] = (1/len(prey_options))*(0.6*(1/len(predator_nearest_neighs)
                                                                                 if pred in predator_nearest_neighs else 0.0)+0.4/len(predator_options))

            neigborsProbs[state] = probs

        
        def fillValues(key):
            fringe = []
            fringe.append((key,None))

            while len(fringe)!=0:
                top = fringe.pop()
                curr = top[0]

                p = False
                for next in neigborsProbs[curr]:
                    if not done[next]:
                        p = True
                        fringe.append((next,curr))
                
                if not p:
                    done[curr] = True

        for state in states:
            if not done[state]:
                # print(key)
                try:
                    (state)
                except RecursionError:
                    print(values)
                    raise RecursionError
                break
            print(state," : done : ",values[state])
        return values
