"""
Class that handles all the rendering part of the project

"""
from copy import deepcopy
import math
import random
from turtle import screensize
import pygame
from environment import Environment
from graph import Graph


class Renderer:
    """
    Initializes the screen 
    Parameters:
        graph -> generated graph object 
    """
    def __init__(self, graph : Graph) -> None:
        self.screenSize = (700,700)
        self.node_count = Environment.getInstance().node_count
        self.node_colors = []
        self.node_centers = []
        center  = (self.screenSize[0]/2,self.screenSize[1]/2)

        for i in range(0,self.node_count):
            self.node_colors.append(random.choices(range(256), k=3))
            self.node_centers.append((center[0]+ 200*math.cos(2*i*math.pi/self.node_count),center[1]+ 200*math.sin(2*i*math.pi/self.node_count)))
        
        self.graph_info = graph.info

        self.edge_rects = []
        self.edge_angles = []
        checked = set()
        for i in graph.info.keys():
            for k in graph.info[i]:
                if not (k,i) in checked:
                    p1 = self.node_centers[i]
                    p2 = self.node_centers[k]

                    xm = (p1[0]+p2[0])/2
                    ym = (p1[1]+p2[1])/2
                    r = Renderer.norm(p1,p2)/2
                    self.edge_rects.append((xm-r,ym-r,2*r,2*r))

                    a1 = Renderer.angle((xm,ym),p1,1)
                    a2 = Renderer.angle((xm,ym),p2,1)
                    self.edge_angles.append((a1,a2))
                    checked.add((i,k))


        if Environment.getInstance().ui:
            pygame.init()
            self.surface = pygame.display.set_mode(self.screenSize)
            pygame.display.set_caption('Circle of Life')
            self.font = pygame.font.Font('freesansbold.ttf', 12)

    
    @staticmethod
    def angle(A, B, aspectRatio):
        x = B[0] - A[0]
        y = B[1] - A[1]
        angle = math.atan2(-y, x / aspectRatio)
        return angle

    # Rendering
    def __render__(self):
        if not Environment.getInstance().ui:
            return
        self.surface.fill((217,217,217))
        
        for i in range(0,len(self.edge_rects)):
            pygame.draw.arc(self.surface,(0,0,0),self.edge_rects[i],self.edge_angles[i][0],self.edge_angles[i][1])
        for i in range(0, self.node_count):  
            radius = 10
            text = self.font.render(str(i), True, (0,0,0))
            textRect = text.get_rect()
            textRect.center = self.node_centers[i]
            pygame.draw.circle(self.surface, self.node_colors[i], self.node_centers[i], radius)
            pygame.draw.circle(self.surface, (0,0,0), self.node_centers[i] , radius,width=1)
            self.surface.blit(text,textRect)

        # center  = (self.screenSize[0]/2,self.screenSize[1]/2)
        # p1 = self.node_centers[0]
        # p2 = self.node_centers[1]

        # xm = (p1[0]+p2[0])/2
        # ym = (p1[1]+p2[1])/2
        # r = Renderer.norm(p1,p2)/2   
        # pygame.draw.rect(self.surface,(0,0,0),self.edge_rects[i],width=1)

        pygame.display.flip()
        pass

    @staticmethod
    def norm(p1,p2):
        return math.sqrt(pow(p1[0]-p2[0],2)+pow(p1[1]-p2[1],2))