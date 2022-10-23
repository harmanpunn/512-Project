import sys
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

from environment import Environment
from graph import Graph
from renderer import Renderer
import pygame
from agent1 import Agent1
from predator import Predator
from prey import Prey


def str2bool(v):
  
    if v.lower() == "true":
        return True
    elif v.lower()=="false":
        return False
    else:
        raise RuntimeError("Invalid value")

allowed_args = {
    "ui":str2bool,
    "node_count":int,
}

def startGame():

    graph_inst = Graph()
    
    graph = graph_inst.generate_graph()
    # graph = graph_instance.generate_graph()
    print('graph:',graph)


    prey = Prey(graph_inst)
    predator = Predator(graph_inst)
    agent1 = Agent1(graph_inst, prey, predator)


    agent1.__update__(graph, prey, predator)


def processArgs():
    print("Number of args: ",str(len(sys.argv)))
    print("Args: ",str(sys.argv))
    if len(sys.argv)>1:
        
        argv = sys.argv[1:]
        args = {}
        for x in argv:
            if x[0:2]!="--":
                raise RuntimeError("Args start with '--'")
            x = x.split('--')[1]
            
            if len(x.split("="))!=2:
                raise RuntimeError("Arg needs single '='")
            x = x.split("=")
            if not x[0] in allowed_args.keys():
                raise RuntimeError("Invalid Argument")

            try:
                args[x[0]]= allowed_args[x[0]](x[1])
            except:
                raise ValueError("Invalid value '"+x[1]+"' for "+x[0])
        
        return args    
    return {}

args = processArgs()

env = Environment(True,50)

for x in args.keys():
    setattr(env,x,args[x]) 

graph = Graph()

# renderer =  Renderer(graph)

if __name__=="__main__":
    print("Initialized")
    startGame()

    running = False

    while running:
        if Environment.getInstance().ui:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    running =True
        
        renderer.__render__()
    
    if Environment.getInstance().ui:
        pygame.quit()