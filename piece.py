import pygame
import math
from constants import *


class Piece:   
    def __init__(self, color, radius, center, number):
        self.highlighted = False
        self.highlighted_color = YELLOW
        self.color = color
        self.radius = radius
        self.center = center
        self.center_x, self.center_y = self.center
        self.tri_num = number
    
    def draw_piece(self, surface):
        if self.highlighted:
            pygame.draw.circle(surface, self.highlighted_color, self.center, self.radius) 
        else:
            pygame.draw.circle(surface, self.color, self.center, self.radius)

    def collide_with_mouse(self, x, y):
        distnace_to_piece_center = math.sqrt(math.pow(x - self.center_x, 2) + math.pow(y - self.center_y, 2))
        if distnace_to_piece_center < self.radius:
            return True
        else:
            return False    

    def highlight(self):
        self.highlighted = True

    def dehighlight(self):
        self.highlighted = False

    




    

