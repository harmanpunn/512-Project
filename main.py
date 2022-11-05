import sys
import os
from time import sleep

from graphEntity import GraphEntity
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

from environment import Environment
from graph import Graph
from renderer import Renderer
import pygame

from agents.agent1 import Agent1
from agents.agent3 import Agent3
from agents.agent5 import Agent5

from predator import Predator
from prey import Prey

get_class = lambda x: globals()[x]

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
    "mode":int,
    "agent":int
}

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

def runGame(args):
    env = Environment(True,50)
    for x in args.keys():
        setattr(env,x,args[x]) 

    graph = Graph()
    renderer =  Renderer(graph)
    # print("Initialized")
    # startGame()

    prey = Prey(graph)
    predator = Predator(graph)
    agent : GraphEntity = get_class("Agent"+str(Environment.getInstance().agent))(graph)

    running = 1
    print(graph.info)
    first_step = True
    while True:
        if Environment.getInstance().ui:
            sleep(0.2)
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    running =False
        if running==1:
            graph.surveyed = False

            info = {}
            if Environment.getInstance().agent<3:
                info = {
                    'prey' : prey.getPosition(),
                    'predator' : predator.getPosition()
                }
            elif Environment.getInstance().agent<5:
                info = {
                    'predator' : predator.getPosition()
                }
            elif Environment.getInstance().agent<7:
                info = {
                    'prey' : prey.getPosition()
                }
                if first_step:
                    info["predator"] = predator.getPosition()
                    first_step = False

            graph.node_states_blocked= True
            print(info)
            agent.__update__(graph, info)
            graph.node_states_blocked = False

            predator.__update__(graph, {'agent':agent.getPosition()})
            prey.__update__(graph)
            renderer.__render__(running)
        
            if agent.getPosition() == prey.getPosition():
                print('Agent Wins :)')
                running = 2
            if agent.getPosition() == predator.getPosition():
                print('Agent Loses :(')
                running = 0

        else:
            if Environment.getInstance().ui:
                renderer.__render__(running)
                sleep(4)
            break

    
    if Environment.getInstance().ui:
        pygame.quit()

if __name__ == "__main__":
    args = processArgs()
    if 'mode' in args.keys() and args['mode']==1:
        print("Mode different")
    runGame(args)