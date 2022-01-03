import pygame
from constants import *

class Button:

    pygame.init()
    font = pygame.font.SysFont("Arial", 18)
    
    def __init__(self, x, y, width, height, color, name):
        self.top_left_x = x
        self.top_left_y = y
        self.width = width
        self.height = height
        self.color = color
        self.name = name
        self.rendered_text = None
        self.clicked = False

    def draw(self, surface, text):
        pygame.draw.rect(surface, self.color, (self.top_left_x, self.top_left_y
                                               , self.width, self.height))
        self.draw_text(surface, text)

    
    def draw_text(self, surface, text):
        self.rendered_text = Button.render_text(text)
        text_x, text_y = self.calc_text_cords()
        surface.blit(self.rendered_text, (text_x, text_y))

    @staticmethod
    def render_text(text):
        return Button.font.render(text, True, BLACK)
    
    def calc_text_cords(self):
        x_padding = (self.width - self.rendered_text.get_width()) / 2
        y_padding = (self.height - self.rendered_text.get_height()) / 2
        text_x = self.top_left_x + x_padding
        text_y = self.top_left_y + y_padding
        return text_x, text_y

    def collide_with_mouse(self, x, y):
        return (self.top_left_x < x < self.top_left_x + self.width) \
               and (self.top_left_y < y < self.top_left_y + self.height) 

    def set_color(self, color):
        self.color = color