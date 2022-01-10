import pygame
from board import Board
from text import Text
from game_state import Game_state
from constants import *
from timeit import default_timer as timer



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
        self.selected_dest = None
        self.double_dice_rolled = False
        self.valid_moves = []
        self.no_of_moves = 0
        self.distnace_left_to_move = 0


    def is_valid_move(self):
        distance_to_move = self.selected_dest - self.selected_origin

        if distance_to_move in self.valid_moves:
            current_piece = self.board.pieces[self.selected_origin][-1]
            dest_pieces = self.board.pieces[self.selected_dest]
            if not dest_pieces:
                return True
            dest_piece = dest_pieces[-1]
            # if there are more than 2 pieces at destination, move is legal if color 
            # of current piece and destination are same.
            if len(dest_pieces) > 1 and current_piece.get_color() == dest_piece.get_color():
                return True
               
        return False

    def set_double_dice_rolled(self):
        if self.board.dices[0].get_num() == self.board.dices[1].get_num():
            self.double_dice_rolled = True
        else:
            self.double_dice_rolled = False

    def set_valid_moves(self):
        dices = self.board.dices
       
        if self.double_dice_rolled:
            self.valid_moves = [dices[0].get_num() * i for i in range(1,5)]
        else:
            self.valid_moves = [dices[0].get_num(), dices[1].get_num()]

    def set_no_of_moves(self):
        if self.double_dice_rolled:
            self.no_of_moves = 4
        else:
            self.no_of_moves = 2

    def set_distnace_left_to_move(self):
        dices = self.board.dices
        if self.double_dice_rolled:
            self.distnace_left_to_move = 4 * dices[0].get_num()
        else:
            self.distnace_left_to_move = dices[0].get_num() + dices[1].get_num()
        
    def select_origin(self, mouse_x, mouse_y):
        self.selected_origin = None

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

    def select_dest(self, mouse_x, mouse_y):
        self.selected_dest = None

        for tri in self.board.triangles:
            if tri.collide_with_mouse(mouse_x, mouse_y):
                self.selected_dest = tri.get_num()
                break
                

    def roll_dices_btn_clicked(self, mouse_x, mouse_y):
        return self.roll_dices_btn.collide_with_mouse(mouse_x, mouse_y)

    def roll_dices(self):
        for dice in self.board.dices:
            dice.roll()
        self.dice_rolled = True
        self.roll_dices_btn.set_color(TAN)
        self.set_move_info()

    def set_move_info(self):
        self.set_double_dice_rolled()
        self.set_valid_moves()
        self.set_no_of_moves()
        self.set_distnace_left_to_move()

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
        if self.dice_rolled:
            self.draw_dices(surface)
        pygame.display.update()

    def reset_btns_color(self):
        for btn in self.board.buttons.values():
            btn.set_color(WHITE)



