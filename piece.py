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
        self.tri_num = number
    
    def draw_piece(self, surface):
        if self.highlighted:
            pygame.draw.circle(surface, self.highlighted_color, self.center, self.radius) 
        else:
            pygame.draw.circle(surface, self.color, self.center, self.radius)

    def collide_with_mouse(self, x, y):
        center_x, center_y = self.center
        distnace_to_piece_center = math.sqrt(math.pow(x - center_x, 2) + math.pow(y - center_y, 2))
        if distnace_to_piece_center < self.radius:
            return True
        else:
            return False    

    def set_center(self, x, y):
        self.center = (x, y)

    def highlight(self):
        self.highlighted = True

    def dehighlight(self):
        self.highlighted = False

    def get_color(self):
        return self.color

    def set_tri_num(self, num):
        self.tri_num = num

    def get_tri_num(self):
        return self.tri_num

    




    

