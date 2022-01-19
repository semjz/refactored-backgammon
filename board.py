import pygame
import pygame.gfxdraw
from piece import Piece
from button import Button
from dice import Dice
from text import Text 
from triangle import Triangle
from constants import *

class Board():

    def __init__(self):
        self.board_play_rect_width = 6 * SQUARE_SIZE
        self.middle_border_size = 50 + ((WIDTH - 950) / 3) 
        self.board_play_area_width = self.board_play_rect_width * 2 + self.middle_border_size
        self.vertical_border_size = 50
        self.horizontal_border_size = 150 + ((WIDTH - 950) / 3)  
        self.black_pieces = []
        self.white_pieces = []
        self.white_pieces_at_mid_bar = []
        self.black_pieces_at_mid_bar = []
        self.white_pieces_holder_list = []
        self.black_pieces_holder_list = []
        self.triangle_first_piece_centers = self.set_tris_first_piece_centers()
        self.pieces = self.create_pieces_dict()
        self.pieces_in_holders = self.create_pieces_in_holders_dict()
        self.white_pieces_holder = pygame.Rect(0, 0, 0, 0)
        self.black_pieces_holder = pygame.Rect(0, 0, 0, 0)
        self.left_play_rect_x, self.left_play_rect_y  = self.left_play_rect_cords()
        self.right_play_rect_x, self.right_play_rect_y = self.right_play_rect_cord()
        self.left_play_rect, self.right_play_rect = self.create_play_rects() 
        self.numbers = self.create_numbers()
        self.dices = self.create_dices()
        self.triangles = []
        self.texts = {}
        self.buttons = {}
        self.create_texts()
        self.create_buttons()
        self.create_top_triangles()
        self.create_bottom_triangles()
    
    def left_play_rect_cords(self):

        left_play_rect_x = self.horizontal_border_size
        left_play_rect_y = self.vertical_border_size
        
        return left_play_rect_x, left_play_rect_y

    def right_play_rect_cord(self):
    
        right_play_rect_x = self.horizontal_border_size + self.board_play_rect_width + self.middle_border_size
        right_play_rect_y = self.vertical_border_size
    
        return right_play_rect_x, right_play_rect_y
    
    def create_play_rects(self):
        board_play_rect_height = HEIGHT - 2 * self.vertical_border_size
        left_play_rect = pygame.Rect(self.left_play_rect_x, self.left_play_rect_y, self.board_play_rect_width, board_play_rect_height)
        right_play_rect = pygame.Rect(self.right_play_rect_x, self.right_play_rect_y , self.board_play_rect_width, board_play_rect_height)
        return left_play_rect, right_play_rect
    
    def set_a_quarter_tri_pieces(self, triangle_first_piece_centers, start_tri_num, start_x, start_y):
        no_of_squares_from_right = 0
        for tri_num in range(start_tri_num, start_tri_num + 6):
            # bottom tri pieces
            if start_tri_num < 13:
                triangle_first_piece_centers[tri_num] = (start_x - SQUARE_SIZE * no_of_squares_from_right , start_y)
            # top tri pieces
            else:
                triangle_first_piece_centers[tri_num] = (start_x + SQUARE_SIZE * no_of_squares_from_right , start_y)
            no_of_squares_from_right += 1
    
    def set_bottom_tris_first_piece_centers(self, triangle_first_piece_centers):
        # pieces 1 to 6.
        triangle_1_first_piece_x = self.horizontal_border_size + self.board_play_area_width - SQUARE_SIZE / 2
        first_piece_y = HEIGHT - self.vertical_border_size - SQUARE_SIZE / 2
        self.set_a_quarter_tri_pieces(triangle_first_piece_centers, 1, triangle_1_first_piece_x, first_piece_y)

        # pieces 7 to 13.
        triangle_7_first_piece_x = self.horizontal_border_size + self.board_play_rect_width - SQUARE_SIZE / 2
        first_piece_y = HEIGHT - self.vertical_border_size - SQUARE_SIZE / 2
        self.set_a_quarter_tri_pieces(triangle_first_piece_centers, 7, triangle_7_first_piece_x, first_piece_y)

    

    def set_top_tris_first_piece_centers(self, triangle_first_piece_centers):
        # pieces 13 to 18.
        triangle_13_first_piece_x = self.horizontal_border_size + SQUARE_SIZE / 2 
        first_piece_y = self.vertical_border_size +  SQUARE_SIZE / 2 
        self.set_a_quarter_tri_pieces(triangle_first_piece_centers, 13, triangle_13_first_piece_x, first_piece_y)

        # pieces 19 to 23.
        triangle_13_first_piece_x = self.horizontal_border_size + self.board_play_rect_width + self.middle_border_size \
                                    + SQUARE_SIZE / 2
        first_piece_y = self.vertical_border_size +  SQUARE_SIZE / 2 
        self.set_a_quarter_tri_pieces(triangle_first_piece_centers, 19, triangle_13_first_piece_x, first_piece_y)


    # set first circle center for each triangle
    def set_tris_first_piece_centers(self):
        
        """key is the triangle number and value is the cords of where
           first piece must be placed"""
        triangle_first_piece_centers = {}
        
        self.set_bottom_tris_first_piece_centers(triangle_first_piece_centers)
        self.set_top_tris_first_piece_centers(triangle_first_piece_centers)
             
        return triangle_first_piece_centers     

    def create_a_quarter_numbers(self, numbers, start_tri_num, start_x, start_y):
        no_of_sqaures = 0
        for tri_num in range(start_tri_num, start_tri_num + 6):
            if tri_num < 13:
                x = start_x - no_of_sqaures * SQUARE_SIZE
            else:
                x = start_x + no_of_sqaures * SQUARE_SIZE
            numbers.append(Text(tri_num, x, start_y, SQUARE_SIZE, SQUARE_SIZE, 16))
            no_of_sqaures += 1


    def create_bottom_numbers(self, numbers):
        # numbers 1 to 6.
        top_left_corner_no_1_x = self.horizontal_border_size + self.board_play_area_width - SQUARE_SIZE / 2
        top_left_corner_y = HEIGHT - self.vertical_border_size / 2
        self.create_a_quarter_numbers(numbers, 1, top_left_corner_no_1_x, top_left_corner_y)

        # numbers 7 to 12.
        top_left_corner_no_7_x = self.horizontal_border_size + self.board_play_rect_width - SQUARE_SIZE / 2
        top_left_corner_y = HEIGHT - self.vertical_border_size / 2
        self.create_a_quarter_numbers(numbers, 7, top_left_corner_no_7_x, top_left_corner_y)


    def create_top_numbers(self, numbers):
        # numbers 13 to 18.
        top_left_corner_no_13_x = self.horizontal_border_size + SQUARE_SIZE / 2
        top_left_corner_y = self.vertical_border_size / 2
        self.create_a_quarter_numbers(numbers, 13, top_left_corner_no_13_x, top_left_corner_y)

        # numbers 19 to 24.
        top_left_corner_no_19_x = self.horizontal_border_size + self.board_play_rect_width + self.middle_border_size + SQUARE_SIZE / 2
        top_left_corner_y = self.vertical_border_size / 2
        self.create_a_quarter_numbers(numbers, 19, top_left_corner_no_19_x, top_left_corner_y)
          

    def create_numbers(self):
        numbers = []

        self.create_bottom_numbers(numbers)
        self.create_top_numbers(numbers)

        return numbers

    def calc_bottom_triangle_cord(self, no_of_squares_from_left):
        # base cords
        first_point_x_cord = self.horizontal_border_size + no_of_squares_from_left * SQUARE_SIZE
        first_point_y_cord = HEIGHT - self.vertical_border_size
        middle_point_x_cord = self.horizontal_border_size + no_of_squares_from_left * SQUARE_SIZE + SQUARE_SIZE / 2 
        middle_point_y_cord = HEIGHT - self.vertical_border_size - 5 * SQUARE_SIZE
        
        # left side triangle cords
        a = (first_point_x_cord , first_point_y_cord)
        b = (middle_point_x_cord , middle_point_y_cord)
        c = (first_point_x_cord + SQUARE_SIZE, first_point_y_cord)

        # left side triangle to be drawn
        left_side_down_triangle = [a, b , c]

        # right side triangle cords
        a1 = (first_point_x_cord + 6 * SQUARE_SIZE + self.middle_border_size, first_point_y_cord)
        b1 = (middle_point_x_cord + 6 * SQUARE_SIZE + self.middle_border_size, middle_point_y_cord)
        c1 = (first_point_x_cord + 7 * SQUARE_SIZE + self.middle_border_size, first_point_y_cord)

        # right side triangle to be drawn
        right_side_down_triangle = [a1, b1, c1]

        return left_side_down_triangle, right_side_down_triangle

    def create_bottom_triangles(self):
        left_tri_num = 12
        right_tri_num = 6
        for no_of_squares_from_left in range(6):
            if no_of_squares_from_left % 2 == 0:
                color = DARK_ORANGE3 
            else:
                color = TAN
            left_side_tri_cords, right_side_tri_cords = self.calc_bottom_triangle_cord(no_of_squares_from_left)
            left_tri = Triangle(left_side_tri_cords, color, left_tri_num)
            right_tri = Triangle(right_side_tri_cords, color, right_tri_num)
            self.triangles.append(left_tri)
            self.triangles.append(right_tri)

            left_tri_num -= 1
            right_tri_num -= 1


    def calc_top_triangles_cords(self, no_of_squares_from_left):
        # base cords
        first_point_x_cord = self.horizontal_border_size + no_of_squares_from_left * SQUARE_SIZE 
        first_point_y_cord = self.vertical_border_size
        middle_point_x_cord = self.horizontal_border_size + SQUARE_SIZE / 2 + no_of_squares_from_left * SQUARE_SIZE
        middle_point_y_cord = self.vertical_border_size + 5 * SQUARE_SIZE

        # left side triangle cords
        a = (first_point_x_cord , first_point_y_cord)
        b = (middle_point_x_cord, middle_point_y_cord)
        c = (first_point_x_cord + SQUARE_SIZE, first_point_y_cord)

        # left side triangle to be drawn
        left_side_down_triangle = [a, b , c]

        # right side triangle cords
        a1 = (first_point_x_cord + 6 * SQUARE_SIZE + self.middle_border_size, first_point_y_cord)
        b1 = (middle_point_x_cord + 6 * SQUARE_SIZE + self.middle_border_size, middle_point_y_cord)
        c1 = (first_point_x_cord + 7 * SQUARE_SIZE + self.middle_border_size, first_point_y_cord)

        # right side triangle to be drawn
        right_side_down_triangle = [a1, b1, c1]

        return left_side_down_triangle, right_side_down_triangle

    def create_top_triangles(self):
        left_tri_num = 13
        right_tri_num = 19
        for no_of_squares_from_left in range(6):
            if no_of_squares_from_left % 2 == 0:
                color = TAN
            else:
                color = DARK_ORANGE3
            left_side_tri_cords, right_side_tri_cords = self.calc_top_triangles_cords(no_of_squares_from_left)
            left_tri = Triangle(left_side_tri_cords, color, left_tri_num)
            right_tri = Triangle(right_side_tri_cords, color, right_tri_num)
            self.triangles.append(left_tri)
            self.triangles.append(right_tri)

            left_tri_num += 1
            right_tri_num += 1
        
    def draw_all_triangles(self, surface):
        for tri in self.triangles:
            tri.draw(surface)


    def set_up_pieces_on_a_tri(self, tri_num, no_of_pieces, piece_color, pieces_list):
        center_x, center_y = self.triangle_first_piece_centers[tri_num]
        for piece_no in range(no_of_pieces):
            if tri_num < 13:
                piece = Piece(piece_color, 25, (center_x, center_y - piece_no * SQUARE_SIZE), tri_num)
            else:
                piece = Piece(piece_color, 25, (center_x, center_y + piece_no * SQUARE_SIZE), tri_num)
            
            if piece_color == WHITE:
                self.white_pieces.append(piece)
            else:
                self.black_pieces.append(piece)

            pieces_list[tri_num].append(piece)
            
    def create_pieces_dict(self):
        pieces = {i:[] for i in range(1, 26)}
        pieces[0] = self.white_pieces_at_mid_bar
        pieces[25] = self.black_pieces_at_mid_bar
        
        """Set up white peices """
        # tri 1
        self.set_up_pieces_on_a_tri(1, 2, WHITE, pieces)
        # tri 122
        self.set_up_pieces_on_a_tri(12, 5, WHITE, pieces)
        # tri 17
        self.set_up_pieces_on_a_tri(17, 3, WHITE, pieces)
        # tri 19
        self.set_up_pieces_on_a_tri(19, 5, WHITE, pieces)


        """set up black peices"""
        # tri 6
        self.set_up_pieces_on_a_tri(6, 5, BLACK, pieces)
        # tri 8
        self.set_up_pieces_on_a_tri(8, 3, BLACK, pieces)
        # tri 13
        self.set_up_pieces_on_a_tri(13, 5, BLACK, pieces)
        # tri 24
        self.set_up_pieces_on_a_tri(24, 2, BLACK, pieces)
        
        return pieces

    def create_pieces_in_holders_dict(self):
        pieces_in_holders = {}
        pieces_in_holders[0] = self.black_pieces_holder_list
        pieces_in_holders[25] = self.white_pieces_holder_list

        return pieces_in_holders

    def create_button(self, button_x, button_y, button_width, button_height, color, name):
        self.buttons[name] = Button(button_x, button_y, button_width, button_height, color, name, 18)
    
    def create_buttons(self):
        # button size
        buttons_width = 80
        buttons_height = 40
        
        # paddings
        x_padding = (self.horizontal_border_size - buttons_width) / 2
        distance_between_btns = 10
        
        # button cords
        buttons_x = self.horizontal_border_size + self.board_play_area_width + x_padding
        undo_button_y = HEIGHT / 2 - distance_between_btns - buttons_height
        draw_button_y = HEIGHT / 2 + distance_between_btns

        self.create_button(buttons_x, undo_button_y, buttons_width, buttons_height, WHITE, "undo")
        self.create_button(buttons_x, draw_button_y, buttons_width, buttons_height, WHITE, "roll dices")


    def create_text(self, text_content, text_x, text_y, text_env_width, text_env_height, text_name):

        text = Text(text_content, text_x, text_y, text_env_width, text_env_height, 17)
        self.texts[text_name] = text

    def create_texts(self):
        # turn
        turn_content = ""
        turn_text_x = self.horizontal_border_size / 2
        turn_text_y = HEIGHT / 4
        turn_text_env_width = self.horizontal_border_size
        turn_text_env_height = HEIGHT / 2
        self.create_text(turn_content, turn_text_x, turn_text_y, turn_text_env_width, turn_text_env_height, "turn")

        move_exist = ""
        move_exist_x = self.horizontal_border_size / 2
        move_exist_y = HEIGHT / 8
        move_exist_env_width = self.horizontal_border_size
        move_exist_env_height = HEIGHT / 4
        self.create_text(move_exist, move_exist_x, move_exist_y, move_exist_env_width, move_exist_env_height, "move exist")


    def draw_background(self, surface):
        surface.fill(GRAY)

    def draw_play_rects(self, surface):
        self.left_play_rect, self.right_play_rect = self.create_play_rects()
        pygame.draw.rect(surface, BOLD_CREAM, self.left_play_rect)
        pygame.draw.rect(surface, BOLD_CREAM, self.right_play_rect)

    def draw_piece_holders(self, surface):
        # pieces holders
        place_holder_width = 50
        place_holder_height = 180
        x_padding = (self.horizontal_border_size - place_holder_width) / 2
        top_left_corner_x = self.horizontal_border_size + self.board_play_area_width + x_padding
   
        self.white_pieces_holder = pygame.Rect(top_left_corner_x, 50, place_holder_width, place_holder_height)
        self.black_pieces_holder = pygame.Rect(top_left_corner_x, 420, place_holder_width, place_holder_height)
        
        # draw pieces holders
        pygame.draw.rect(surface, BROWN, self.white_pieces_holder)
        pygame.draw.rect(surface, BROWN, self.black_pieces_holder)
    
    def draw_texts(self, surface):
        for text in self.texts.values():
            text.draw(surface)
        
    def draw_numbers(self, surface):
        for num in self.numbers:
            num.draw(surface)

    def draw_buttons(self, surface):
        for btn in self.buttons.values():
            btn.draw(surface)

    def create_dices(self):
        dices = []
        dices_width, dices_height = 40, 40
        dices_y = HEIGHT / 2 - dices_height / 2
       
        dice_1_x = self.horizontal_border_size / 2 - (5 + dices_width)
        dice_1 = Dice(dices_width, dices_height, WHITE, dice_1_x, dices_y)
        dices.append(dice_1)
       
        dice_2_x = self.horizontal_border_size / 2 + 5 
        dice_2 = Dice(dices_width, dices_height, WHITE, dice_2_x, dices_y)
        dices.append(dice_2)

        return dices   

    def draw_pieces(self, surface):
        for pieces in self.pieces.values():
            for piece in pieces:
                piece.draw_piece(surface)
    
    def draw_white_pieces_in_holder(self, surface):
        place_holder_width = 50
        x_padding = (self.horizontal_border_size - place_holder_width) / 2
        top_left_corner_x = self.horizontal_border_size + self.board_play_area_width + x_padding
        piece_y = self.vertical_border_size
        for piece_no in range(len(self.white_pieces_holder_list)):
            pygame.draw.rect(surface, WHITE, (top_left_corner_x, piece_y + piece_no * 12, 50, 10))

    def draw_black_pieces_in_holder(self, surface):
        place_holder_width = 50
        x_padding = (self.horizontal_border_size - place_holder_width) / 2
        top_left_corner_x = self.horizontal_border_size + self.board_play_area_width + x_padding
        piece_y = HEIGHT - SQUARE_SIZE - 10
        for piece_no in range(len(self.black_pieces_holder_list)):            
            pygame.draw.rect(surface, BLACK, (top_left_corner_x, piece_y - piece_no * 12, 50, 10))

    def draw_pieces_at_mid_bar(self, surface):
        for piece in self.white_pieces_at_mid_bar:
            piece.draw_piece(surface)

        for piece in self.black_pieces_at_mid_bar:
            piece.draw_piece(surface)

    def draw_board(self, surface):
        
        self.draw_background(surface)
        self.draw_play_rects(surface)
        self.draw_all_triangles(surface)
        self.draw_numbers(surface)
        self.draw_texts(surface)
        self.draw_piece_holders(surface)
        self.draw_buttons(surface)

        self.draw_pieces(surface)
        self.draw_pieces_at_mid_bar(surface)
        self.draw_white_pieces_in_holder(surface)
        self.draw_black_pieces_in_holder(surface)
 


