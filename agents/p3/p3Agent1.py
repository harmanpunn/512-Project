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
        # print(policy)
        # print(policy,graph)
        values = {}
        done = {}
        added = {}
        neigborsProbs = {}

        for key in policy.keys():
            if key[2] == key[0]:
                values[key] = P3Agent1.someBigNumber
                done[key] = True
            else:
                if key[1] == key[0]:
                    values[key] = 0
                    done[key] = True
                else:
                    values[key] = 0
                    done[key] = False
                    added[key] = False

            probs = {}
            prey_options = graph.info[key[1]] + [key[1]]
            predator_options = graph.info[key[2]]

            dists = []
            for opt in predator_options:
                dists.append(get_shortest_path(graph.info, opt, policy[key]))

            predator_nearest_neighs = [predator_options[i] for i in range(
                0, len(predator_options)) if dists[i] == min(dists)]

            for pr in prey_options:
                for pred in predator_options:
                    probs[(policy[key], pr, pred)] = (1/len(prey_options))*(0.6*(1/len(predator_nearest_neighs)
                                                                                 if pred in predator_nearest_neighs else 0.0)+0.4/len(predator_options))

            neigborsProbs[key] = probs

        def fillValues(key):
            fringe = []
            fringe.append((key, None))

            count = {}

            while len(fringe) != 0:
                # sleep(0.5)

                top = fringe.pop()
                if not top[0] in count.keys():
                    count[top[0]] = 0

                print(top[0],": ",count[top[0]]," || ",values[top[0]])
                if not done[top[0]]:
                    count[top[0]] +=1
                    if count[top[0]]>=P3Agent1.someBigNumber:
                        print("Too many ",top[0])
                        values[top[0]] = P3Agent1.someBigNumber
                        done[top[0]] = True

                if done[top[0]]:
                    while top[1] != None:
                        values[top[1][0]] += values[top[0]]
                        top = top[1]

                if not done[top[0]] and not added[top[0]]:
                    values[top[0]] += 1
                    added[top[0]] = True

                p = False
                for k in neigborsProbs[top[0]]:
                    if not done[k]:
                        fringe.append((k, top))
                        p = True
                    # else:
                if not p:
                    done[top[0]] = True

        def getValueX(key):
            print(key)
            if done[key] or (values[key] >= P3Agent1.someBigNumber):
                if (values[key] >= P3Agent1.someBigNumber):
                    print("Too big")
                elif values[key] == 0:
                    print("End")
                return values[key]
            else:
                values[key] = 1
                for k in neigborsProbs[key]:
                    values[k] += neigborsProbs[key][k]*getValueX(k)

                done[key] = True
                return values[key]

        def sortStates(state):
            return get_shortest_path(graph.info, state[0], state[1])
        states = list(policy.keys())
        print(len(states))

        states.sort(key=sortStates)
        for key in states:
            if not done[key]:
                # print(key)
                fillValues(key)
                break
            print(key," : done : ",values[key])
        return values
