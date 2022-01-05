
import pygame
from constants import *

class Text:
    pygame.init()
    font = pygame.font.SysFont("Arial", 17)
    
    def __init__(self, text, x, y, env_width, env_height):
        self.content = text
        self.render_content()
        self.x_cord, self.y_cord = x, y
        self.original_x_cord, self.original_y_cord = x, y
        self.env_width, self.env_height  = env_width, env_height

    def render_content(self):
        self.rendered_content = Text.font.render(str(self.content), True, BLACK)
        self.width = self.rendered_content.get_width()
        self.height = self.rendered_content.get_height()

    def set_content(self, text):
        self.content = text
        self.render_content()

    def calc_paddings(self):
        width_padding = (self.env_width - self.width) / 2
        height_padding = (self.env_height - self.height) / 2 

        return width_padding, height_padding

    def add_paddings(self):
        width_padding, height_padding = self.calc_paddings()
        x_cord = self.x_cord + width_padding
        y_cord = self.y_cord + height_padding
        return x_cord, y_cord 

    def collide_with_mouse(self, x_mouse, y_mouse):
        return self.x_cord < x_mouse < self.x_cord + self.width \
               and self.y_cord < y_mouse < self.height

    def draw(self, surface):
        x_cord, y_cord = self.add_paddings()
        surface.blit(self.rendered_content, (x_cord, y_cord))