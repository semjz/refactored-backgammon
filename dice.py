import pygame
import pygame.gfxdraw
import random
from constants import *

class Dice:
    def __init__(self, width, height, color, x, y):
        self.width = width
        self.height = height
        self.color = color
        self.num = None
        self.x_top_left = x
        self.y_top_left = y
        self.to_be_drawn = False
        self.moves_made_by = 0
    
    def set_to_be_drawn(self, bol):
        self.to_be_drawn = bol

    def get_to_be_drawn(self):
        return self.to_be_drawn

    def get_num(self):
        return self.num

    def set_num(self, num):
        self.num = num
        
    def roll(self):
        self.num = random.randint(1,6)

    def draw(self, surface, turn):
        if turn == "black":
            rec_color = BLACK
            circ_color = WHITE
        else:
            rec_color = WHITE
            circ_color = BLACK
        
        plain_dice = pygame.Surface((self.width, self.height))
        plain_dice.fill(rec_color)
        if self.num == 1:
            self.draw_circle(plain_dice, int(self.width / 2), int(self.height / 2), 4, circ_color)
        
        elif self.num == 2:
            self.draw_circle(plain_dice, int(self.width / 6), int(self.height / 6), 4, circ_color)
            self.draw_circle(plain_dice, int(self.width * 5 / 6), int(self.height * 5 / 6), 4, circ_color)
        
        elif self.num == 3:
            self.draw_circle(plain_dice, int(self.width / 6), int(self.height / 6), 4, circ_color)
            self.draw_circle(plain_dice, int(self.width / 2), int(self.height / 2), 4, circ_color)
            self.draw_circle(plain_dice, int(self.width * 5 / 6), int(self.height * 5 / 6), 4, circ_color)
        
        elif self.num == 4:
            self.draw_circle(plain_dice, int(self.width / 6), int(self.height / 6), 4, circ_color)
            self.draw_circle(plain_dice, int(self.width * 5 / 6), int(self.height / 6), 4, circ_color)
            self.draw_circle(plain_dice, int(self.width / 6), int(self.height * 5 / 6), 4, circ_color)
            self.draw_circle(plain_dice, int(self.width * 5 / 6), int(self.height * 5 / 6), 4, circ_color)
        
        elif self.num == 5:
            self.draw_circle(plain_dice, int(self.width / 6), int(self.height / 6), 4, circ_color)
            self.draw_circle(plain_dice, int(self.width * 5 / 6), int(self.height / 6), 4, circ_color)
            self.draw_circle(plain_dice, int(self.width / 2), int(self.height / 2), 4, circ_color)
            self.draw_circle(plain_dice, int(self.width / 6), int(self.height * 5 / 6), 4, circ_color)
            self.draw_circle(plain_dice, int(self.width * 5 / 6), int(self.height * 5 / 6), 4, circ_color)
        
        elif self.num == 6:
            self.draw_circle(plain_dice, int(self.width / 6), int(self.height / 6), 4, circ_color)
            self.draw_circle(plain_dice, int(self.width / 6), int(self.height / 2), 4, circ_color)
            self.draw_circle(plain_dice, int(self.width / 6), int(self.height * 5 / 6), 4, circ_color)
            self.draw_circle(plain_dice, int(self.width * 5 / 6), int(self.height / 6), 4, circ_color)
            self.draw_circle(plain_dice, int(self.width * 5 / 6), int(self.height / 2), 4, circ_color)
            self.draw_circle(plain_dice, int(self.width * 5 / 6), int(self.height * 5 / 6), 4, circ_color)
        # x and y are the top left corner cords.
        surface.blit(plain_dice, (self.x_top_left, self.y_top_left)) 

    def draw_circle(self, surface, x, y, r, color):
        pygame.gfxdraw.aacircle(surface, x, y, r, color)
        pygame.gfxdraw.filled_circle(surface, x, y, r, color)

    

