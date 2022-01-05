import pygame
from board import Board
from text import Text
from game_state import Game_state
from constants import *

class Game:
    def __init__(self):
        self.board = Board()
        self.state = Game_state.DECIDE_TURNS
        self.dice_rolled = False
        self.turn = ""
        self.turn_text = self.board.texts[2]
        self.roll_count = 0
        self.roll_dices_btn = self.board.buttons["roll dices"]

    def roll_dices_btn_clicked(self, mouse_x, mouse_y):
        return self.roll_dices_btn.collide_with_mouse(mouse_x, mouse_y)

    def roll_dices(self):
        for dice in self.board.dices:
            dice.roll()
        self.dice_rolled = True
        self.roll_dices_btn.set_color(TAN)

    def draw_dices(self, surface):
        for dice in self.board.dices:
            dice.draw(surface)

    def decide_turns(self, sum_of_first_roll, sum_of_second_roll):
        if sum_of_first_roll > sum_of_second_roll:
            self.turn = "white"
        else:
            self.turn = "black"

    def sum_of_dice_nums(self):
        return self.board.dices[0].dice_num + self.board.dices[1].dice_num

    def update_board(self, surface):
        self.board.draw_board(surface)
        if self.dice_rolled:
            self.draw_dices(surface)
        pygame.display.update()

    def reset_btns_color(self):
        for btn in self.board.buttons.values():
            btn.set_color(WHITE)
