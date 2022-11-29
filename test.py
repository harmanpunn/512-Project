from graph import Graph
from agents.p3.p3Agent1 import P3Agent1
from environment import Environment

environment = Environment(False,5)
graph = Graph()

agent = P3Agent1(graph)

# print(agent.policy)