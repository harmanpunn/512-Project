import sys

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
    # return
    print(*args, file=sys.stderr, **kwargs)
