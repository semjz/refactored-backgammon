
import pygame
from constants import *

class Text:
    pygame.init()
    font = pygame.font.SysFont("Arial", 15)
    
    def __init__(self, text):
        self.content = text
        self.rendered_content = Text.font.render(str(self.content), True, BLACK)
        self.width = self.rendered_content.get_width()
        self.height = self.rendered_content.get_height()
        self.x_cord, self.y_cord = 0, 0

    def calc_paddings(self, env_width, env_height):
        width_padding = (env_width - self.width) / 2
        height_padding = (env_height - self.height) / 2 

        return width_padding, height_padding

    def add_paddings(self, x, y, env_width, env_height):
        width_padding, height_padding = self.calc_paddings(env_width, env_height)
        self.x_cord = x + width_padding
        self.y_cord = y + height_padding


    def collide_with_mouse(self, x_mouse, y_mouse):
        return self.x_cord < x_mouse < self.x_cord + self.width \
               and self.y_cord < y_mouse < self.height

    def draw(self, surface):
        surface.blit(self.rendered_content, (self.x_cord, self.y_cord))