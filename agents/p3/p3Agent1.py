from graphEntity import GraphEntity
from graph import Graph
from environment import Environment
from util import get_shortest_path
from valueIteration import getValues, getPolicyFromValues
import random

from time import sleep


class P3Agent1(GraphEntity):

    someBigNumber = 200

    def __init__(self, graph: Graph) -> None:
        # super.__init__()
        self.type = 1
        while True:
            self.position = random.randint(0,Environment.getInstance().node_count-1)
            if not graph.node_states[self.position][0] and not graph.node_states[self.position][2]:
                break
        graph.allocate_pos(self.position, self.type)

        vals , matrix = getValues(graph)
        self.policy = getPolicyFromValues(vals, matrix)

    def plan(self, graph: Graph, info):
        state = (self.position, info["prey"],info["predator"])
        self.nextPosition = self.policy[state]
        return [1,1]

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
