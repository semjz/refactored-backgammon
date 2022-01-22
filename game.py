import pygame
from board import Board
from piece import Piece
from game_state import Game_state
from constants import *


class Game:

    def __init__(self):
        self.board = Board()
        self.state = Game_state.DECIDE_TURNS
        self.dice_is_rolled = False
        self.double_dice_is_rolled = False
        self.turn = None
        self.winner = None
        self.turn_text = self.board.texts["turn"]
        self.move_exist_text = self.board.texts["move exist"]
        self.roll_dices_btn = self.board.buttons["roll dices"]
        self.undo_btn = self.board.buttons["undo"]
        self.selected_origin = None
        self.selected_dest = None
        self.move_distance = None
        self.move_direction = None
        self.no_of_moves_left = None
        self.valid_moves = []
        self.mid_bar_piece_selected = False
        self.lowest_home_tri_num_with_white_piece = None
        self.highest_home_tri_num_with_black_piece = None
        
    def change_turn(self):
        if self.turn == "white":
            self.turn = "black"
        else:
            self.turn = "white"

    def move_on_board(self):
        origin_pieces_list = self.board.pieces[self.selected_origin]
        piece_to_be_moved = origin_pieces_list.pop()
        dest_pieces_list = self.board.pieces[self.selected_dest]
        dest_x, dest_first_piece_y = self.board.triangle_first_piece_centers[self.selected_dest]

        if self.move_is_hit(piece_to_be_moved):
            dest_piece = dest_pieces_list.pop()
            self.place_piece_at_mid_bar(dest_piece)

        dest_y = self.calc_piece_dest_y(dest_pieces_list, dest_first_piece_y)
        if len(dest_pieces_list) >= 5:
            self.add_piece_to_tri_5_or_more(dest_pieces_list, dest_x, dest_y)

        if len(origin_pieces_list) >= 5:
            self.remove_piece_from_tri_5_or_more(origin_pieces_list)

        self.valid_moves.remove(self.move_distance)
        for dice in self.board.dices:
            if dice.get_num() == self.move_distance and dice.get_to_be_drawn():
                dice.set_to_be_drawn(False)
                break
        
        self.no_of_moves_left -= 1
        if self.no_of_moves_left == 0:
            self.dice_is_rolled = False
            self.double_dice_is_rolled = False
                
        piece_to_be_moved.set_tri_num(self.selected_dest)
        piece_to_be_moved.set_center(dest_x, dest_y)
        piece_to_be_moved.dehighlight()
        self.mid_bar_piece_selected = False
        dest_pieces_list.append(piece_to_be_moved)

        self.calc_lowest_home_tri_num_with_white_piece()
        self.calc_highest_home_tri_num_with_black_piece()

    def move_to_piece_holder(self):
        origin_pieces_list = self.board.pieces[self.selected_origin]
        piece_to_be_moved = origin_pieces_list.pop()
        dest_pieces_list = self.board.pieces_in_holders[self.selected_dest]

        # fix bug to remove dice from valid moves when a piece on lower
        # tri than indicated by dice is removed.
        if self.move_distance in self.valid_moves:
            self.valid_moves.remove(self.move_distance)
        else:
            for valid_move in self.valid_moves:
                if self.move_distance < valid_move: 
                    self.valid_moves.remove(valid_move)
                    break

        equal_dice_found = False
        for dice in self.board.dices:
            if dice.get_to_be_drawn() and self.move_distance == dice.get_num():
                dice.set_to_be_drawn(False)
                equal_dice_found = True
                break

        if not equal_dice_found: 
            for dice in self.board.dices:
                if dice.get_to_be_drawn() and self.move_distance < dice.get_num():
                    dice.set_to_be_drawn(False)
                    break

                
        # bug fix for pieces nt expanding when moving to piece holder.
        if len(origin_pieces_list) >= 5:
            self.remove_piece_from_tri_5_or_more(origin_pieces_list)
        
        self.no_of_moves_left -= 1
        if self.no_of_moves_left == 0:
            self.dice_is_rolled = False
            self.double_dice_is_rolled = False

        piece_to_be_moved.dehighlight()
        dest_pieces_list.append(piece_to_be_moved)
        
        if self.turn == "white":
            self.board.white_pieces.remove(piece_to_be_moved)
        else:
            self.board.black_pieces.remove(piece_to_be_moved)

        self.calc_lowest_home_tri_num_with_white_piece()
        self.calc_highest_home_tri_num_with_black_piece()

    def move_is_hit(self, piece_to_be_moved: Piece):
        if len(self.board.pieces[self.selected_dest]) == 1:
            dest_piece = self.board.pieces[self.selected_dest][-1]
            return piece_to_be_moved.get_color() != dest_piece.get_color()

    def add_piece_to_tri_5_or_more(self, dest_pieces_list, dest_x, dest_y):
        no_of_pieces_on_tri_after_move = len(dest_pieces_list) + 1
        try:
            self.board.texts[self.selected_dest].set_content(no_of_pieces_on_tri_after_move, RED)
        except KeyError:
            self.board.create_text(no_of_pieces_on_tri_after_move
                                   , dest_x
                                   , dest_y
                                   , SQUARE_SIZE
                                   , SQUARE_SIZE
                                   , RED
                                   , 18
                                   , self.selected_dest)


    def remove_piece_from_tri_5_or_more(self, origin_pieces_list):
        if len(origin_pieces_list) == 5:
            self.board.remove_text(self.selected_origin)
        else:
            self.board.texts[self.selected_origin].set_content(len(origin_pieces_list), RED)


    def calc_piece_dest_y(self, dest_pieces_list, dest_first_piece_y):
        if len(dest_pieces_list) <= 4:
            no_of_pieces = len(dest_pieces_list)
        else:
            no_of_pieces = 4

        if self.selected_dest < 13:
            dest_first_piece_y -= no_of_pieces * SQUARE_SIZE
        else:
            dest_first_piece_y += no_of_pieces * SQUARE_SIZE

        return dest_first_piece_y

    def place_piece_at_mid_bar(self, piece: Piece):
        dest_x = WIDTH / 2
        piece.set_on_mid_bar(True)

        if piece.get_color() == "white":
            base_dest_y = HEIGHT - self.board.vertical_border_size - 25
            dest_y = base_dest_y - len(self.board.white_pieces_at_mid_bar) * 50
            piece.set_center(dest_x, dest_y)
            piece.set_tri_num(0)
            self.board.white_pieces_at_mid_bar.append(piece)
        else:
            base_dest_y = self.board.vertical_border_size + 25
            dest_y = base_dest_y + len(self.board.black_pieces_at_mid_bar) * 50
            piece.set_center(dest_x, dest_y)
            piece.set_tri_num(25)
            self.board.black_pieces_at_mid_bar.append(piece)

    def turns_color_piece_on_mid_bar(self):
        if self.turn == "white":
            return self.board.white_pieces_at_mid_bar
        else:
            return self.board.black_pieces_at_mid_bar

    def is_valid_move_on_board(self, origin_tri, dest_tri):
        self.set_move_distance_and_direction(origin_tri, dest_tri)
        # if place holders are destination
        if dest_tri <= 0 or dest_tri >= 25:
            return False
        return self.legal_move_direction(origin_tri) and self.move_is_valid_based_on_dices() \
                and self.check_legal_move_based_on_dest_pieces(origin_tri, dest_tri)

    def is_valid_move_to_piece_holders(self, origin_tri, dest_tri):
        self.set_move_distance_and_direction(origin_tri, dest_tri)
        return (self.move_is_valid_based_on_dices() 
                or self.piece_of_closest_tri_right_of_determined_tri_by_dices_selected(origin_tri)) \
                and self.is_valid_move_to_current_turn_piece_holder(dest_tri)
    
    def move_is_valid_based_on_dices(self):
        return self.move_distance in self.valid_moves

    def piece_of_closest_tri_right_of_determined_tri_by_dices_selected(self, origin_tri):
        if self.turn == "white" and self.white_pieces_at_lower_tri_than_determined_origin_tri_by_dices() \
            and origin_tri == self.lowest_home_tri_num_with_white_piece:
                return True
        if self.turn == "black" and self.black_pieces_at_higher_tri_than_determined_origin_tri_by_dices() \
            and origin_tri == self.highest_home_tri_num_with_black_piece:
                return True
        return False

    def white_pieces_at_lower_tri_than_determined_origin_tri_by_dices(self):
        for valid_move in self.valid_moves:
            if self.lowest_home_tri_num_with_white_piece > 25 - valid_move:
                return True
        return False

    def black_pieces_at_higher_tri_than_determined_origin_tri_by_dices(self):
        for valid_move in self.valid_moves:
            if self.highest_home_tri_num_with_black_piece < valid_move:
                return True
        return False

    def is_valid_move_to_current_turn_piece_holder(self, dest_tri):
        if self.turn == "white":
            return self.is_valid_move_to_white_piece_holder(dest_tri)
        else:
            return self.is_valid_move_to_black_piece_holder(dest_tri)

    def is_valid_move_to_white_piece_holder(self, dest_tri):
        return self.pieces_are_at_home_base() and dest_tri == 25 

    def is_valid_move_to_black_piece_holder(self, dest_tri):
        return self.pieces_are_at_home_base() and dest_tri == 0  
        
    def pieces_are_at_home_base(self):
        return self.turn == "white" and self.pieces_are_at_white_home_base() \
                or self.turn == "black" and self.pieces_are_at_black_home_base()

    def pieces_are_at_white_home_base(self):
        for piece in self.board.white_pieces:
            if piece.get_tri_num() < 19:
                return False
        return True

    def pieces_are_at_black_home_base(self):
        for piece in self.board.black_pieces:
            if piece.get_tri_num() > 6:
                return False
        return True

    # white only moves clockwise and black anti clockwise.
    def legal_move_direction(self, origin_tri):
        current_piece = self.board.pieces[origin_tri][-1]
        return current_piece.get_color() == "white" and self.move_direction == CLOCK_WISE \
                or current_piece.get_color() == "black" and self.move_direction == ANTI_CLOCK_WISE

    def check_legal_move_based_on_dest_pieces(self, origin, dest):
        current_piece = self.board.pieces[origin][-1]
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
        if self.board.dices[1].get_num() == self.board.dices[2].get_num():
            self.double_dice_is_rolled = True
        else:
            self.double_dice_is_rolled = False

    def set_valid_moves(self):
        if self.double_dice_is_rolled:
            self.valid_moves = [self.board.dices[1].get_num() for i in range(4)]
        else:
            self.valid_moves = [self.board.dices[1].get_num(), self.board.dices[2].get_num()]

    # if same numbers are rolled, player can make 4 moves.
    def set_no_of_moves(self):
        if self.double_dice_is_rolled:
            self.no_of_moves_left = 4
        else:
            self.no_of_moves_left = 2
    
    def get_no_of_moves_left(self):
        return self.no_of_moves_left
        
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
                self.selected_origin = piece.get_tri_num()
                selected_piece = self.board.pieces[piece.get_tri_num()][-1]
                selected_piece.highlight()
                return True
        return False
    
    def deselect_origin(self):
        selected_piece = self.board.pieces[self.selected_origin][-1]
        selected_piece.dehighlight()
        self.selected_origin = None

    def select_piece_on_mid_bar(self, mouse_x, mouse_y):
        if self.turn == "black":
            pieces = self.board.black_pieces_at_mid_bar
            selected_mid_bar = 25
        else:
            pieces = self.board.white_pieces_at_mid_bar
            selected_mid_bar = 0
        
        for piece in pieces:
            if piece.collide_with_mouse(mouse_x, mouse_y):
                self.mid_bar_piece_selected = True
                self.selected_origin = selected_mid_bar
                selected_piece = self.board.pieces[self.selected_origin][-1]
                selected_piece.highlight()
                return True
        return False

    def select_dest(self, mouse_x, mouse_y):
        self.selected_dest = None
        # if mouse cords are on a triangle, set selecet origin and highlight 
        # the last piece on the triangle finally break the loop.
        for tri in self.board.triangles:
            if tri.collide_with_mouse(mouse_x, mouse_y):
                self.selected_dest = tri.get_num()
                return True
        
        if self.white_piece_holder_selected(mouse_x, mouse_y):
            self.selected_dest = 25
            return True

        if self.black_piece_holder_selected(mouse_x, mouse_y):
            self.selected_dest = 0
            return True
        return False       

    def white_piece_holder_selected(self, mouse_x, mouse_y):
        return pygame.Rect.collidepoint(self.board.white_pieces_holder, mouse_x, mouse_y)    

    def black_piece_holder_selected(self, mouse_x, mouse_y):
        return pygame.Rect.collidepoint(self.board.black_pieces_holder, mouse_x, mouse_y)    
        
    def roll_dices_btn_clicked(self, mouse_x, mouse_y):
        return self.roll_dices_btn.collide_with_mouse(mouse_x, mouse_y)

    def undo_btn_clicked(self, mouse_x, mouse_y):
        return self.undo_btn.collide_with_mouse(mouse_x, mouse_y)

    # roll dices and set move info.
    def roll_dices(self):
        double_dice_num = None
        for i in range(1, 3):
            self.board.dices[i].roll()
            self.board.dices[i].set_to_be_drawn(True)
        
        self.set_double_dice_is_rolled()
        if self.double_dice_is_rolled:
            double_dice_num = self.board.dices[1].get_num()
            for i in range(0, 4, 3):
                self.board.dices[i].set_num(double_dice_num)
                self.board.dices[i].set_to_be_drawn(True)
        
        self.dice_is_rolled = True
        self.set_move_info()

    def roll_single_dice(self, dice_no):
        self.board.dices[dice_no + 1].roll()
        self.board.dices[dice_no + 1].set_to_be_drawn(True)
        self.dice_is_rolled = True
        self.roll_dices_btn.set_color(TAN)

    # check if a double dice is rolled, set valid moves and number of moves
    # and distance left to move.
    def set_move_info(self):
        self.set_valid_moves()
        self.set_no_of_moves()

    def draw_dices(self, surface):
        for dice in self.board.dices:
            if dice.get_to_be_drawn() and dice.get_num():
                dice.draw(surface, self.turn)

    # if first dice has a greater number first turn is white otherwise blacks
    def decide_turns(self):
        first_dice_num = self.board.dices[1].get_num()
        second_dice_num = self.board.dices[2].get_num()

        if first_dice_num == second_dice_num:
            return False
        else:
            if first_dice_num > second_dice_num:
                self.turn = "white"
            else:
                self.turn = "black"
            return True
    
    def set_move_distance_and_direction(self, origin_tri, dest_tri):
        displacment = dest_tri - origin_tri
        self.move_distance = abs(displacment)

        if displacment > 0:
            self.move_direction = CLOCK_WISE
        else:
            self.move_direction = ANTI_CLOCK_WISE        

    def reset_btns_color(self):
        for btn in self.board.buttons.values():
            btn.set_color(WHITE)

    def calc_lowest_home_tri_num_with_white_piece(self):
        self.lowest_home_tri_num_with_white_piece = 24
        for piece in self.board.white_pieces:
            if piece.get_tri_num() in (0,25):
                break
            if piece.get_tri_num() and self.board.pieces[piece.get_tri_num()] \
                and piece.get_tri_num() < self.lowest_home_tri_num_with_white_piece:
                self.lowest_home_tri_num_with_white_piece = piece.get_tri_num()

    def calc_highest_home_tri_num_with_black_piece(self):
        self.highest_home_tri_num_with_black_piece = 1
        for piece in self.board.black_pieces:
            if piece.get_tri_num() in (0,25):
                break
            if self.board.pieces[piece.get_tri_num()] \
               and piece.get_tri_num() > self.highest_home_tri_num_with_black_piece:
                self.highest_home_tri_num_with_black_piece = piece.get_tri_num()

    def winner_is_determined(self):
        return self.turn == "white" and not self.board.white_pieces \
               or self.turn == "black" and not self.board.black_pieces

    def update_board(self, surface):
        self.board.draw_board(surface)
        self.draw_dices(surface)
        pygame.display.update()

# check if there are any valid moves from mid bar peice to board.
    def valid_move_exist_from_mid_to_board_for_piece(self, piece):
        piece_tri_num = piece.get_tri_num()
        if self.double_dice_is_rolled:
            return self.is_valid_move_on_board(*self.calc_orig_and_dest_move_from_mid_to_board(piece_tri_num, self.valid_moves[0]))
        else:
            try:
                return self.is_valid_move_on_board(*self.calc_orig_and_dest_move_from_mid_to_board(piece_tri_num, self.valid_moves[0])) \
                       or self.is_valid_move_on_board(*self.calc_orig_and_dest_move_from_mid_to_board(piece_tri_num, self.valid_moves[1]))
            except IndexError:
                return self.is_valid_move_on_board(*self.calc_orig_and_dest_move_from_mid_to_board(piece_tri_num, self.valid_moves[0]))
    
    def calc_orig_and_dest_move_from_mid_to_board(self, piece_tri_num, move_distance):
        if self.turn == "white":
            return 0, piece_tri_num + move_distance
        else:
            return 25, piece_tri_num - move_distance

    def valid_move_exist_from_mid_to_board(self):
        if self.turn == "white":
            origin_tri = 0
        else:
            origin_tri = 25
        
        piece = self.board.pieces[origin_tri][-1]
        return self.valid_move_exist_from_mid_to_board_for_piece(piece)
            
    # check if there are any valid moves on board.
    def valid_move_exist_on_board(self):
        for pieces in self.board.pieces.values():
            if pieces:
                piece = pieces[-1]
            else:
                continue
            if piece.get_color() == self.turn and self.valid_move_exist_on_board_for_piece(piece):
                return True
        return False

    def valid_move_exist_on_board_for_piece(self, piece):
        piece_tri_num = piece.get_tri_num()
        if self.double_dice_is_rolled:
            return self.is_valid_move_on_board(piece_tri_num, self.calc_dest_move_on_board(piece_tri_num, self.valid_moves[0]))
        else:
            try:
                return self.is_valid_move_on_board(piece_tri_num, self.calc_dest_move_on_board(piece_tri_num, self.valid_moves[0])) \
                       or self.is_valid_move_on_board(piece_tri_num, self.calc_dest_move_on_board(piece_tri_num, self.valid_moves[1]))
            except IndexError:
                return self.is_valid_move_on_board(piece_tri_num, self.calc_dest_move_on_board(piece_tri_num, self.valid_moves[0]))

    def calc_dest_move_on_board(self, piece_tri_num, move_distance):
        if self.turn == "white":
            return piece_tri_num + move_distance
        else:
            return piece_tri_num - move_distance

    # check if there are any valid moves on board.
    def valid_move_exist_to_piece_holder(self):
        for pieces in self.board.pieces.values():
            if pieces:
                piece = pieces[-1]
            else:
                continue
            if piece.get_color() == self.turn and self.valid_move_exist_to_piece_holder_for_piece(piece):
                return True
        return False

    def valid_move_exist_to_piece_holder_for_piece(self, piece):
        piece_tri_num = piece.get_tri_num()
        return self.is_valid_move_to_piece_holders(piece_tri_num, self.calc_dest_move_to_piece_holder())

    def calc_dest_move_to_piece_holder(self):
        if self.turn == "white":
            return 25
        else:
            return 0

    def undraw_extra_dices(self):
        for i in range(0, 4, 3):
            self.board.dices[i].set_to_be_drawn(False)
            
