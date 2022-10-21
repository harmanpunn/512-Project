

from environment import Environment
from graph import Graph
from renderer import Renderer


env = Environment(True,50)

graph = Graph()

renderer =  Renderer(graph)

if __name__=="__main__":
    print("Initialized")