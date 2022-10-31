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

def startGame():
    graph_inst = Graph()
    
    graph = graph_inst.generate_graph()
    # graph = graph_instance.generate_graph()
    print('graph:',graph)


    prey = Prey(graph_inst)
    predator = Predator(graph_inst)
    agent : GraphEntity = get_class(Environment.getInstance().agent)(graph_inst)

    state = "RUNNING"
    agent_pos_track = list()
    prey_post_track = list()
    predator_pos_track = list()
    while state == "RUNNING":
        agent.__update__(graph, prey, predator)
        
        predator.__update__(graph, agent.agent_postion())
        prey.__update__(graph)
        agent_pos_track.append(agent.agent_postion())
        prey_post_track.append(prey.getPosition())
        predator_pos_track.append(predator.getPosition())

        if agent.agent_postion() == predator.getPosition():
            print('Agent Loses :(')
            state = "OVER"

        if agent.agent_postion() == prey.getPosition():
            print('Agent Wins :)')
            state = "OVER"

    print('Agent Path: ', agent_pos_track)
    print('Prey Path: ', prey_post_track)
    print('Predator Path: ', predator_pos_track)

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
    agent = Agent3(graph)

    running = 1
    print(graph.info)
    while True:
        if Environment.getInstance().ui:
            sleep(0.2)
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    running =False
        if running==1:
            graph.surveyed = False
            print("Actual prey position: ",prey.getPosition())
            graph.node_states_blocked= True
            agent.__update__(graph, {
                'prey' : prey.getPosition(),
                'predator' : predator.getPosition()
            })
            graph.node_states_blocked = False
            
            predator.__update__(graph, {'agent':agent.getPosition()})
            prey.__update__(graph)
            renderer.__render__(running)
        
            if agent.getPosition() == predator.getPosition():
                print('Agent Loses :(')
                running = 0

            if agent.getPosition() == prey.getPosition():
                print('Agent Wins :)')
                running = 2
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