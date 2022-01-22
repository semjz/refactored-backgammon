import pygame
from constants import *


class Text:
    pygame.init()
    font = pygame.font.SysFont("Arial", 16)
    
    def __init__(self, content, x, y, env_width, env_height, color, font_size):
        self.font = pygame.font.SysFont("Arial", font_size)
        self.content = content
        self.render_content(color)
        self.x_cord, self.y_cord = x, y
        self.original_x_cord, self.original_y_cord = x, y
        self.env_width, self.env_height = env_width, env_height

    def render_content(self, color):
        content = str(self.content)
        self.rendered_content = self.font.render(content, True, color)
        self.width = self.rendered_content.get_width()
        self.height = self.rendered_content.get_height()

    def set_content(self, text, color):
        self.content = text
        self.render_content(color)

    def calc_paddings(self):
        width_padding = self.width / 2
        height_padding = self.height / 2 
        return width_padding, height_padding

    def add_paddings(self):
        width_padding, height_padding = self.calc_paddings()
        x_cord = self.x_cord - width_padding
        y_cord = self.y_cord - height_padding
        return x_cord, y_cord 
        
    def draw(self, surface):
        x_cord, y_cord = self.add_paddings()
        surface.blit(self.rendered_content, (x_cord, y_cord))
        