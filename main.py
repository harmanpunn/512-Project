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

from agents.agent1 import Agent1
from agents.agent3 import Agent3
from agents.agent5 import Agent5
from agents.agent7 import Agent7

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
    "agent":int,
    "noisy":str2bool,
    "quiet":str2bool
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


def runGame(graph : Graph):

    # graph = Graph()
    renderer =  Renderer(graph)
    # print("Initialized")
    # startGame()
    step_count = 0
    game_state = -2
    prey = Prey(graph)
    predator = Predator(graph)

    if Environment.getInstance().agent % 2 == 0:
        Environment.getInstance().careful = True

    if Environment.getInstance().agent < 3:
        agent : GraphEntity = Agent1(graph)
    elif Environment.getInstance().agent < 5:
        agent : GraphEntity = Agent3(graph) 
    elif Environment.getInstance().agent < 7:
        agent : GraphEntity = Agent5(graph) 
    elif Environment.getInstance().agent < 9:
        agent : GraphEntity = Agent7(graph)         

        # agent : GraphEntity = get_class("Agent"+str(Environment.getInstance().agent))(graph)

    running = 1
    print(graph.info)
    first_step = True

    if Environment.getInstance().noisy:
        print("So NOISY!")
    
    if Environment.getInstance().careful:
        print("TipToe B)")

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
            else:
                if first_step:
                    info["predator"] = predator.getPosition()
                    first_step = False

            graph.node_states_blocked= True
            agent.__update__(graph, info)
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

            if step_count > 200:
                running = 0
                # Timeout
                game_state = -1 

        else:
            if Environment.getInstance().ui:
                renderer.__render__(running)
                sleep(4)
            break
        step_count+=1
    graph.reset_states()    
    
    if Environment.getInstance().ui:
        pygame.quit()
    return [step_count, game_state]    

def collectData() -> None:
    
    graph = Graph()
    stats_dict = dict()
    step_count_list = list()
    game_state_list = list()
    type_list = list()
    for i in  tqdm(range(0,100)):
        type = i
        for _ in tqdm(range(0,100),leave=False):
            [step_count, game_state] = runGame(graph) 
            step_count_list.append(step_count)
            game_state_list.append(game_state)
            type_list.append(type)
        

    stats_dict = {'graph_type': type_list, 'step_count': step_count_list, 'game_count' : game_state_list}

    win_count = game_state_list.count(1)
    lose_count = game_state_list.count(0)
    timeout_count = game_state_list.count(-1)
    sys.stdout = sys.__stdout__

    print("========== GAME STATS ==========")
    print("Win Count: ",win_count)
    print("Win %: ", (win_count/10000) * 100)
    print("Lose Count: ",lose_count)
    print("Lose %: ", (lose_count/10000) * 100)
    print("Timeout Count: ",timeout_count)
    print("Timeout %: ", (timeout_count/10000) * 100)
    print("================================")
    '''    
    stats_dict['graph_type'] = 1
    stats_dict['step_count'] = step_count
    stats_dict['game_state'] = game_state
    '''
    # print(stats_dict) 
    # stats_df = pd.DataFrame(columns=['Graph Type', 'Step Count', 'Game State'])
    # stats_df.loc[len(stats_df.index)] = []
    # stats_df.loc[len()]
    # stats_df = pd.DataFrame(data = stats_dict)
    # stats_df.to_csv('Agent'+str(Environment.getInstance().agent)+'.csv', index=False)
    pass


if __name__ == "__main__":
    args = processArgs()
    env = Environment(True,50)
    for x in args.keys():
        setattr(env,x,args[x]) 
    
    if Environment.getInstance().quiet==True or 'mode' in args.keys() and args['mode']==1:
        sys.stdout = open(os.devnull, 'w')
    if 'mode' in args.keys() and args['mode']==1:
        print("Mode different")
        Environment.getInstance().ui = False
        collectData()
    else:
        graph = Graph()
        runGame(graph)


