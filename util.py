import sys
from environment import Environment

def get_shortest_path(graph, src, dest):
    # print('src:',src)
    # print('dest:',dest)
    if src == dest:
        return 0;
    distance = []
    predecessor = list()

    for i in range(len(graph)):
        distance.insert(i,99999)
        predecessor.insert(i,-1)

    if shortest_path(graph, src, dest, distance, predecessor):
        # print('Short path is available')
        path = []
        j = dest
        path.append(j)

        while predecessor[j] != -1:
            path.append(predecessor[j])
            j = predecessor[j]

        
        # print("Shortest path : ", path)
        # print('New Position:', path[len(path) - 2])
        return len(path)
    else:
        raise ValueError("Invalid Graph")


def shortest_path(graph, src, dest, distance, predecessor):
    queue = []
    visited = [False for i in range(len(graph))]

    queue.append(src)
    distance[src] = 0
    visited[src] = True

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

def eprint(*args, **kwargs):
    return
    print(*args, file=sys.stderr, **kwargs)


def getNewBeliefs(belief,survey_node, survey_res):
    if not survey_res:
        sums = 0.0
        for node in range(0,Environment.getInstance().node_count):
            if node != survey_node:
                sums += belief[node]
            else:
                belief[node]=0
        belief =  [x/sums for x in belief]
    else:
        # if not (Environment.getInstance().noisy_agent and Environment.getInstance().noisy):
        for node in range(0,Environment.getInstance().node_count):
            belief[node] = 0.0 if node!=survey_node else 1.0
        # else:
        #     sums = 0.0
        #     for node in range(0,Environment.getInstance().node_count):
        #         if node != survey_node:
        #             sums += belief[node]
        #         else:
        #             belief[node]=0
        #     belief = [0.9*(0.0 if i!=survey_node else 1.0) + 0.1*belief[i]/sums for i in range(0,Environment.getInstance().node_count)]
    return belief

def transitionProbabilities(belief, graphInfo, closeNodes = None, pred=False):
    temp_beliefs = [0.0 for x in range(0,Environment.getInstance().node_count)]
    if not pred:
        for parent in range(0,Environment.getInstance().node_count):
            for neigh in (graphInfo[parent]+[parent]):
                temp_beliefs[neigh] += belief[parent]/(len(graphInfo[parent])+1)  
        return temp_beliefs
    else:
        new_belief = [0.0 for _ in range(0, Environment.getInstance().node_count)]
        for pr in range(0,Environment.getInstance().node_count):
            for x in graphInfo[pr]:
                new_belief[x] += belief[pr]*(0.6*(1/len(closeNodes[pr]) if x in closeNodes[pr] else 0.0) + 0.4/(len(graphInfo[pr])))
        return new_belief
