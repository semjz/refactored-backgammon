import pygame
from text import Text
from constants import *

class Button:

    pygame.init()
    font = pygame.font.SysFont("Arial", 18)
    
    def __init__(self, x, y, width, height, color, name):
        self.top_left_x = x
        self.top_left_y = y
        self.width = width
        self.height = height
        self.text = Text(name, self.top_left_x, self.top_left_y, self.width, self.height)
        self.color = color

    def draw(self, surface):
        # draw button
        pygame.draw.rect(surface, self.color, (self.top_left_x, self.top_left_y
                                               , self.width, self.height))
        # draw button's text
        self.text.draw(surface)


    def collide_with_mouse(self, x, y):
        return (self.top_left_x < x < self.top_left_x + self.width) \
               and (self.top_left_y < y < self.top_left_y + self.height) 

    def set_color(self, color):
        self.color = color