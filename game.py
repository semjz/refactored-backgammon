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
        self.selected_origin = None
        
    def select_origin(self, mouse_x, mouse_y):
        if self.turn == "black":
            pieces = self.board.black_pieces
        else:
            pieces = self.board.white_pieces
        
        for piece in pieces:
            if piece.collide_with_mouse(mouse_x, mouse_y):
                selected_tri_num = piece.tri_num
                selected_piece = self.board.pieces[selected_tri_num][-1]
                selected_piece.highlight()
                self.selected_origin = selected_tri_num
                break

    def roll_dices_btn_clicked(self, mouse_x, mouse_y):
        return self.roll_dices_btn.collide_with_mouse(mouse_x, mouse_y)

    def roll_dices(self):
        for dice in self.board.dices:
            dice.roll()
        self.dice_rolled = True
        self.roll_dices_btn.set_color(TAN)

    def roll_single_dice(self, dice_no):
        self.board.dices[dice_no - 1].roll()
        self.dice_rolled = True
        self.roll_dices_btn.set_color(TAN)

    def draw_dices(self, surface):
        for dice in self.board.dices:
            if dice.get_num():
                dice.draw(surface)

    def decide_turns(self):
        first_dice_num = self.board.dices[0].get_num()
        second_dice_num = self.board.dices[1].get_num()

        if first_dice_num == second_dice_num:
            return False
        else:
            if first_dice_num > second_dice_num:
                self.turn = "white"
            else:
                self.turn = "black"
            return True
        

    def sum_of_dice_nums(self):
        return self.board.dices[0].get_num() + self.board.dices[1].get_num()

    def update_board(self, surface):
        self.board.draw_board(surface)
        if self.roll_count != 0:
            self.draw_dices(surface)
        pygame.display.update()

    def reset_btns_color(self):
        for btn in self.board.buttons.values():
            btn.set_color(WHITE)



