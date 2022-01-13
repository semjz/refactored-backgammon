import pygame
from board import Board
from text import Text
from game_state import Game_state
from board_area import Board_area
from constants import *

class Game:

    def __init__(self):
        self.board = Board()
        self.state = Game_state.DECIDE_TURNS
        self.dice_is_rolled = False
        self.double_dice_is_rolled = False
        self.turn = ""
        self.turn_text = self.board.texts[2]
        self.roll_dices_btn = self.board.buttons["roll dices"]
        self.selected_origin = None
        self.selected_dest = None
        self.move_distance = 0
        self.move_direction = None
        self.valid_moves = []
        self.no_of_moves_left = 0
        self.distnace_left_to_move = 0

    def change_turn(self):
        if self.turn == "white":
            self.turn = "black"
        else:
            self.turn = "white"

    def move_on_board(self):
        piece_to_be_moved = self.board.pieces[self.selected_origin].pop()
        dest_pieces_list = self.board.pieces[self.selected_dest]
        dest_x, dest_first_piece_y = self.board.triangle_first_piece_centers[self.selected_dest]
    
        if self.move_is_hit(piece_to_be_moved):
            dest_piece = dest_pieces_list.pop()
            self.place_piece_on_mid_bar(dest_piece)

        
        if not self.double_dice_is_rolled:
            self.valid_moves.remove(self.move_distance)
            
        self.no_of_moves_left -= 1
        if self.no_of_moves_left == 0:
            self.dice_is_rolled = False
            self.double_dice_is_rolled = False
        
        dest_y = self.calc_piece_dest_y(dest_pieces_list, dest_first_piece_y)
        piece_to_be_moved.set_tri_num(self.selected_dest)
        piece_to_be_moved.set_center(dest_x, dest_y)
        piece_to_be_moved.dehighlight()
        dest_pieces_list.append(piece_to_be_moved)


    def move_is_hit(self, piece_to_be_moved):
        if len(self.board.pieces[self.selected_dest]) == 1:
            dest_piece = self.board.pieces[self.selected_dest][-1]
            return piece_to_be_moved.get_color() != dest_piece.get_color()


    def calc_piece_dest_y(self, dest_pieces_list, dest_first_piece_y):
        if self.selected_dest < 13:
            dest_first_piece_y -= len(dest_pieces_list) * 50
        else:
            dest_first_piece_y += len(dest_pieces_list) * 50
        return dest_first_piece_y

    def place_piece_on_mid_bar(self, piece):
        dest_x = WIDTH / 2
        if piece.get_color() == WHITE:
            base_dest_y = HEIGHT - self.board.vertical_border_size -25
            dest_y = base_dest_y - len(self.board.white_pieces_on_mid_bar) * 50
            piece.set_center(dest_x, dest_y)
            self.board.white_pieces_on_mid_bar.append(piece)
        else:
            base_dest_y = self.board.vertical_border_size + 25
            dest_y = base_dest_y + len(self.board.black_pieces_on_mid_bar) * 50
            piece.set_center(dest_x, dest_y)
            self.board.black_pieces_on_mid_bar.append(piece)
        

    def is_any_piece_on_mid_bar(self):
        pieces_on_mid_bar = self.board.white_pieces_on_mid_bar + self.board.black_pieces_on_mid_bar
        return pieces_on_mid_bar

    def is_valid_move_on_board(self):
        if self.legal_move_direction() and self.move_is_valid_based_on_dices():
            return self.check_legal_move_based_on_dest_pieces(self.selected_dest)
        return False

    def move_is_valid_based_on_dices(self):
        return self.move_distance in self.valid_moves

    # white only moves clockwise and black anti clockwise.
    def legal_move_direction(self):
        current_piece = self.board.pieces[self.selected_origin][-1]
        if current_piece.get_color() == WHITE and self.move_direction == CLOCK_WISE:
            return True
        if current_piece.get_color() == BLACK and self.move_direction == ANTI_CLOCK_WISE:
            return True
        return False

    def check_legal_move_based_on_dest_pieces(self, dest):
        current_piece = self.board.pieces[self.selected_origin][-1]
        dest_pieces = self.board.pieces[dest]
            
        # if destination triangle has one or no piece, move is legal.
        if len(dest_pieces) in (0,1):
            return True
        
        # if there are more than 1 piece at destination, move is legal if 
        # current and destination pieces have same color.
        else:
            dest_piece = dest_pieces[-1]
            if current_piece.get_color() == dest_piece.get_color():
                return True
            return False

    # check if a double dice is rolled.
    def set_double_dice_is_rolled(self):
        if self.board.dices[0].get_num() == self.board.dices[1].get_num():
            self.double_dice_is_rolled = True
        else:
            self.double_dice_is_rolled = False

    def set_valid_moves(self):
        dices = self.board.dices
       
        if self.double_dice_is_rolled:
            self.valid_moves = [dices[0].get_num()]
        else:
            self.valid_moves = [dices[0].get_num(), dices[1].get_num()]

    # if same numbers are rolled, player can make 4 moves.
    def set_no_of_moves(self):
        if self.double_dice_is_rolled:
            self.no_of_moves_left = 4
        else:
            self.no_of_moves_left = 2

    def set_distnace_left_to_move(self):
        dices = self.board.dices
        if self.double_dice_is_rolled:
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
        self.dice_is_rolled = True
        self.roll_dices_btn.set_color(TAN)
        self.set_move_info()

    # check if a double dice is rolled, set valid moves and number of moves
    # and distance left to move.
    def set_move_info(self):
        self.set_double_dice_is_rolled()
        self.set_valid_moves()
        self.set_no_of_moves()
        self.set_distnace_left_to_move()

    def roll_single_dice(self, dice_no):
        self.board.dices[dice_no - 1].roll()
        self.dice_is_rolled = True
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
    
    def get_no_of_moves_left(self):
        return self.no_of_moves_left

    def set_move_distance_and_direction(self):
        displacment = self.selected_dest - self.selected_origin
        if displacment > 0:
            self.move_direction = CLOCK_WISE
        else:
            self.move_direction = ANTI_CLOCK_WISE
        self.move_distance = abs(self.selected_dest - self.selected_origin)

    def update_board(self, surface):
        self.board.draw_board(surface)
        if self.dice_is_rolled:
            self.draw_dices(surface)
        pygame.display.update()

    def reset_btns_color(self):
        for btn in self.board.buttons.values():
            btn.set_color(WHITE)



