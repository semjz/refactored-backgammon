import pygame
from constants import *

class Number:
    # to use the font init() is used.
    pygame.init()
    font = pygame.font.SysFont("Arial", 15)
    
    def __init__(self, value, x, y):
        self.value = value
        self.rendered_number = Number.font.render(str(self.value), True, BLACK)
        self.width = self.rendered_number.get_width()
        self.height = self.rendered_number.get_height()
        self.x_cord, self.y_cord = self.add_paddings(x, y)

    def calc_paddings(self):
        width_padding = (SQUARE_SIZE - self.width) / 2
        height_padding = (SQUARE_SIZE - self.height) / 2 

        return width_padding, height_padding

    def add_paddings(self, x, y):
        width_padding, height_padding = self.calc_paddings()
        new_x = x + width_padding
        new_y = y + height_padding

        return new_x, new_y

    # returns True if mouse is click on number area
    def collides_with_mouse(self, x_mouse, y_mouse):
        if self.width < 10:
            return (self.x_cord - 6 < x_mouse < self.x_cord + self.width + 6) \
                    and (self.y_cord < y_mouse < self.y_cord + self.height)
        else:
            return (self.x_cord - 2 < x_mouse < self.x_cord + self.width + 2) \
                     and (self.y_cord < y_mouse < self.y_cord + self.height)

    def draw(self, surface):
        surface.blit(self.rendered_number, (self.x_cord, self.y_cord))


