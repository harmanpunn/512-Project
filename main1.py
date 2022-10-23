

from agent1 import Agent1
from graph import Graph
from predator import Predator
from prey import Prey


def startGame():

    graph_inst = Graph()
    
    graph = graph_inst.generate_graph()
    # graph = graph_instance.generate_graph()
    print('graph:',graph)


    prey = Prey(graph_inst)
    predator = Predator(graph_inst)
    agent1 = Agent1(graph_inst, prey, predator)


    agent1.__update__(graph, prey, predator)





    

    


    



if __name__ == "__main__":
    startGame()