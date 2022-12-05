import sys
import os
from time import sleep
import pandas as pd

from graphEntity import GraphEntity
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

from environment import Environment
from graph import Graph
from renderer import Renderer
from tqdm import tqdm
import pygame

from agents.p2.agent1 import Agent1

from agents.p2.agent7 import Agent7

import numpy as np

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

def strToAgent(x):
    if x=="x":
        return 10
    else:
        p = int(x)
        if p>=1 and p<=9:
            return p
        else:
            raise ValueError()

allowed_args = {
    "ui":str2bool,
    "node_count":int,
    "mode":int,
    "agent":strToAgent,
    "noisy":str2bool,
    "quiet":str2bool,
    "noisy_agent":str2bool,
    "graphs":int,
    "games":int,
    "p3":str2bool
}

def processArgs():
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


def runGame(graph : Graph):

    # graph = Graph()
    renderer =  Renderer(graph)
    # print("Initialized")
    # startGame()
    step_count = 0
    game_state = -2
    prey = Prey(graph)
    predator = Predator(graph)

    agent : GraphEntity = Agent1(graph) 
    agent.predator_belief = [1.0 if i==predator.getPosition() else 0.0 for i in range(0,Environment.getInstance().node_count)]        

    running = 1
    while True:
        if Environment.getInstance().ui:
            sleep(0.5)
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
            # elif Environment.getInstance().agent<5:
            #     info = {
            #         'predator' : predator.getPosition()
            #     }
            # elif Environment.getInstance().agent<7:
            #     info = {
            #         'prey' : prey.getPosition()
            #     }

            graph.node_states_blocked= True
            knows = agent.__update__(graph, info)
                
            graph.node_states_blocked = False
            
            predator.__update__(graph, {'agent':agent.getPosition()})
            prey.__update__(graph)
            renderer.__render__(running)
           
            if agent.getPosition() == prey.getPosition():
                print('Agent Wins :)')
                running = 2
                # Agent catches its prey
                game_state = 1

            if agent.getPosition() == predator.getPosition():
                print('Agent Loses :(')
                running = 0
                # Agent caught by predator
                game_state = 0

            if step_count > 10000:
                running = 0
                # Timeout
                game_state = -1 
            step_count+=1
        else:
            if Environment.getInstance().ui:
                renderer.__render__(running)
                sleep(2)
            break
    graph.reset_states()    
    if Environment.getInstance().ui:
        pygame.quit()
    return [step_count, game_state]  

def collectData() -> None:
    stats_dict = dict()
    step_count_list = {0:0.0,1:0.0,-1:0.0}
    game_state_list = list()
    type_list = list()
    totalConfidences = [[],[]]
    for i in  tqdm(range(0,Environment.getInstance().graphs)):
        graph = Graph()
        type = i
        confidencePerGraph = [0.0,0.0] 
        for _ in tqdm(range(0,Environment.getInstance().games),leave=False):
            [step_count, game_state, confidence] = runGame(graph) 
            step_count_list[game_state]+=step_count
            game_state_list.append(game_state)
            type_list.append(type)
            confidencePerGraph = [confidencePerGraph[i]+ confidence[i] for i in range(0, len(confidence))]
            
        confidencePerGraph = [x/Environment.getInstance().games for x in confidencePerGraph]
        for i in range(0,len(confidencePerGraph)):
            totalConfidences[i].append(confidencePerGraph[i])
    
    for k in step_count_list:
        step_count_list[k] /= Environment.getInstance().games * Environment.getInstance().graphs
    
    for t in totalConfidences:
        t = np.array(t)
        
    win_count = game_state_list.count(1)
    lose_count = game_state_list.count(0)
    timeout_count = game_state_list.count(-1)
    sys.stdout = sys.__stdout__

    z = Environment.getInstance().games * Environment.getInstance().graphs
    print("========== GAME STATS ==========")
    print("Predator confidence : Mean: ",np.mean(totalConfidences[0])," || Standard Deviation: ",np.std(totalConfidences[0]))
    print("Prey confidence : Mean: ",np.mean(totalConfidences[1])," || Standard Deviation: ",np.std(totalConfidences[1]))
    print("Win Step Counts: ", step_count_list[1])
    print("Win %: ", (win_count/z) * 100)
    print("Lose Step Count: ",step_count_list[0])
    print("Lose %: ", (lose_count/z) * 100)
    print("Timeout Step Count: ",step_count_list[-1])
    print("Timeout %: ", (timeout_count/z) * 100)
    print("================================")
    pass


if __name__ == "__main__":
    args = processArgs()
    env = Environment(True,50)
    for x in args.keys():
        setattr(env,x,args[x]) 
    
    if Environment.getInstance().quiet==True:
        sys.stdout = open(os.devnull, 'w')
    if 'mode' in args.keys() and args['mode']==1:
        print("Mode different")
        Environment.getInstance().ui = False
        collectData()
    else:
        graph = Graph()
        runGame(graph)


