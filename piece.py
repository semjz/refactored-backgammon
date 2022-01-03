import pygame
from constants import *


class Piece:   
    def __init__(self, color, radius, center, number):
        self.highlighted = False
        self.highlighted_color = YELLOW
        self.color = color
        self.radius = radius
        self.center = center
        self.tri_num = number
    
    def draw_piece(self, surface):
        if self.highlighted:
            pygame.draw.circle(surface, self.highlighted_color, self.center, self.radius) 
        else:
            pygame.draw.circle(surface, self.color, self.center, self.radius)      
        
    def set_center(self, x, y):
        self.center = (x, y)

    def set_tri_num(self, number):
        self.tri_num = number

    def highlight(self):
        self.highlighted = True

    def dehighlight(self):
        self.highlighted = False

    




    

