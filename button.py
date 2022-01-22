import pygame
from text import Text
from constants import *


class Button:

    pygame.init()
    
    def __init__(self, x, y, width, height, color, name, font_size):
        self.top_left_x = x
        self.top_left_y = y
        self.width = width
        self.height = height
        self.text_x = self.top_left_x + width / 2
        self.text_y = self.top_left_y + height / 2
        self.text = Text(name, self.text_x, self.text_y, self.width, self.height, BLACK ,font_size)
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