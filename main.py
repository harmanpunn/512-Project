import sys
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

from environment import Environment
from graph import Graph
from renderer import Renderer
import pygame

allowed_args = {
    "ui":bool,
    "node_count":int,
}

def processArgs():
    print("Number of args: ",str(len(sys.argv)))
    print("Args: ",str(sys.argv))
    if len(sys.argv)>1:
        
        argv = sys.argv[1:]
        print(argv)
        for x in argv:
            if x[0:2]!="--":
                raise RuntimeError("Args start with '--'")
            
            if len(x.split("="))!=2:
                raise RuntimeError("Arg needs single '='")
    
    return {}

args = processArgs()

# env = Environment(True,50)

# graph = Graph()

# renderer =  Renderer(graph)

# if __name__=="__main__":
#     print("Initialized")
#     print(graph.info)

#     running = True

#     while running:
#         for event in pygame.event.get():
#             if event.type==pygame.QUIT:
#                 running =True
        
#         renderer.__render__()
    

#     pygame.quit()