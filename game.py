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
        self.double_dice_rolled = False
        self.turn = ""
        self.turn_text = self.board.texts[2]
        self.roll_count = 0
        self.roll_dices_btn = self.board.buttons["roll dices"]
        self.selected_origin = None
        self.selected_dest = None
        self.valid_moves = []
        self.no_of_moves_left = 0
        self.distnace_left_to_move = 0

    def sum_of_dices_face(self):
        return self.board.dices[0].get_num() + self.board.dices[1].get_num()

    def is_valid_move(self):
        distance_to_move = abs(self.selected_dest - self.selected_origin)

        # Check the direction of move is legal
        if not self.legal_move_direction(distance_to_move):
            return False
        # move is valid and same numbers are rolled.
        if distance_to_move in self.valid_moves and self.double_dice_rolled:
            return self.legal_moves_double_dice(distance_to_move)
        # move is valid and different numbers are rolled.
        if distance_to_move in self.valid_moves and not self.double_dice_rolled:
            # when player moves sum of dices.
            if distance_to_move == self.sum_of_dice_nums():
                # if either combination of moves is legal then the whole move is legal.
                if not self.legal_double_moves_single_dice(self.board.dices[0], self.board.dices[1]):
                    return self.legal_double_moves_single_dice(self.board.dices[1], self.board.dices[0])
                else:
                    return True
            else:
                # when player makes a noram single move.
                return self.dest_pieces_legal_for_move(self.selected_dest)

        return False

    # white only moves clockwise and black anti clockwise.
    def legal_move_direction(self, distance_to_move):
        distance_to_move = self.selected_dest - self.selected_origin
        current_piece = self.board.pieces[self.selected_origin][-1]
        if current_piece.get_color() == WHITE and distance_to_move > 0:
            return True
        if current_piece.get_color() == BLACK and distance_to_move < 0:
            return True
        return False
    
    # check if multiple moves made by player is legal when same numbers are rolled.
    def legal_moves_double_dice(self, distance_to_move):
        origin = self.selected_origin
        current_piece = self.board.pieces[self.selected_origin][-1]
        no_of_moves = distance_to_move / self.board.dices[0]
        if no_of_moves > self.no_of_moves_left:
            return False
        
        if current_piece.get_color() == WHITE:
            dest = origin + self.board.dices[0]
        else:
            dest = origin - self.board.dices[0]

        # check legality of in-between moves.
        for i in range(no_of_moves):
            if not self.dest_pieces_legal_for_move(dest):
                return False
            origin += self.board.dices[0]
            dest += self.board.dices[0]

        self.no_of_moves_left -= no_of_moves

        return True

    # check if a double move made is legal when differnt numbers are rolled.
    def legal_double_moves_single_dice(self, first_dice, second_dice):
        origin = self.selected_origin
        current_piece = self.board.pieces[self.selected_origin][-1]
        
        # check if both moves are legal, if any of them are illegal
        # whole move is illegal.

        if current_piece.get_color() == WHITE:
            dest = origin + first_dice.get_num()
        else:
            dest = origin - first_dice.get_num()
        
        print(origin, dest)
        
        if not self.dest_pieces_legal_for_move(dest):
            return False
        
        origin = dest
        
        if current_piece.get_color() == WHITE:
            dest = origin + second_dice.get_num()
        else:
            dest = origin - second_dice.get_num()

        print(origin, dest)

        if not self.dest_pieces_legal_for_move(dest):
            return False
                
        return True

    # a piece can't move on a triangle with more than 1 piece
    # of different color.
    def dest_pieces_legal_for_move(self, dest):
        current_piece = self.board.pieces[self.selected_origin][-1]
        dest_pieces = self.board.pieces[dest]
        
        # if destination triangle has one or no piece, move is legal
        if len(dest_pieces) in (0,1):
            return True
        dest_piece = dest_pieces[-1]
        
        # if there are more than 1 piece at destination, move is legal if color 
        # of current piece and destination triangle pieces are same.
        if len(dest_pieces) > 1 and current_piece.get_color() == dest_piece.get_color():
            return True
        
        return False

    # check if a double dice is rolled.
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
            self.valid_moves = [dices[0].get_num(), dices[1].get_num(), self.sum_of_dices_face()]

    # if same numbers are rolled, player can make 4 moves.
    def set_no_of_moves(self):
        if self.double_dice_rolled:
            self.no_of_moves_left = 4
        else:
            self.no_of_moves_left = 2

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
        
        # if mouse cords are on a piece, set selecet origin and highlight the last piece on the triangle
        # finally break the loop.
        for piece in pieces:
            if piece.collide_with_mouse(mouse_x, mouse_y):
                selected_piece = self.board.pieces[piece.get_tri_num()][-1]
                selected_piece.highlight()
                self.selected_origin = piece.get_tri_num()
                break

    def select_dest(self, mouse_x, mouse_y):
        self.selected_dest = None
        
        # if mouse cords are on a triangle, set selecet origin and highlight the last piece on the triangle
        # finally break the loop.
        for tri in self.board.triangles:
            if tri.collide_with_mouse(mouse_x, mouse_y):
                self.selected_dest = tri.get_num()
                break
                

    def roll_dices_btn_clicked(self, mouse_x, mouse_y):
        return self.roll_dices_btn.collide_with_mouse(mouse_x, mouse_y)

    # roll dices and set move info.
    def roll_dices(self):
        for dice in self.board.dices:
            dice.roll()
        self.dice_rolled = True
        self.roll_dices_btn.set_color(TAN)
        self.set_move_info()

    # check if a double dice is rolled, set valid moves and number of moves
    # and distance left to move.
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

    # if first dice has a greater number first turn is white otherwise blacks
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



