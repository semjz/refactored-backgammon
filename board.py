import pygame
import pygame.gfxdraw
from piece import Piece
from number import Number
from button import Button
from text import Text 
from constants import *


class Board:

    def __init__(self):
        self.board_play_rect_width = 300
        self.middle_border_size = 50 + ((WIDTH - 950) / 3) 
        self.board_play_area_width = self.board_play_rect_width * 2 + self.middle_border_size
        self.vertical_border_size = 50
        self.horizontal_border_size = 150 + ((WIDTH - 950) / 3)  
        self.black_pieces = []
        self.white_pieces = []
        self.triangle_first_piece_centers = self.set_tris_first_piece_centers()
        self.pieces = self.create_pieces_list()
        self.white_pieces_in_mid = []
        self.black_pieces_in_mid = []
        self.white_pieces_holder_list = []
        self.black_pieces_holder_list = []
        self.white_pieces_holder = pygame.Rect(0, 0, 0, 0)
        self.black_pieces_holder = pygame.Rect(0, 0, 0, 0)
        self.left_border = self.create_left_border()
        self.right_border = self.create_right_border()
        self.middle_border = self.create_middle_border()
        self.top_border = self.create_top_border()
        self.bottom_border = self.create_bottom_border()
        self.numbers = self.create_numbers()
        self.texts = self.create_texts()
        self.buttons = self.create_buttons()
        self.dices = []
        
    def create_left_border(self):
        return pygame.Rect(0, 0, self.horizontal_border_size, HEIGHT)

    def create_right_border(self):
        return pygame.Rect(self.horizontal_border_size + self.board_play_area_width, 0, self.horizontal_border_size, HEIGHT)

    def create_middle_border(self):
        return pygame.Rect(self.horizontal_border_size + self.board_play_rect_width, 0, self.middle_border_size, HEIGHT)

    def create_top_border(self):
        return pygame.Rect(0, 0, WIDTH, self.vertical_border_size)

    def create_bottom_border(self):
        return pygame.Rect(0, HEIGHT - self.vertical_border_size, WIDTH, self.vertical_border_size)

    def triangle_is_not_empty(self, tri_num):
        return self.pieces[tri_num]

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
            numbers.append(Number(tri_num, x, start_y))
            no_of_sqaures += 1


    def create_bottom_numbers(self, numbers):
        # numbers 1 to 6.
        top_left_corner_no_1_x = self.horizontal_border_size + self.board_play_area_width - SQUARE_SIZE
        top_left_corner_y = HEIGHT - self.vertical_border_size
        self.create_a_quarter_numbers(numbers, 1, top_left_corner_no_1_x, top_left_corner_y)

        # numbers 7 to 12.
        top_left_corner_no_7_x = self.horizontal_border_size + self.board_play_rect_width - SQUARE_SIZE
        top_left_corner_y = HEIGHT - self.vertical_border_size
        self.create_a_quarter_numbers(numbers, 7, top_left_corner_no_7_x, top_left_corner_y)


    def create_top_numbers(self, numbers):
        # numbers 13 to 18.
        top_left_corner_no_13_x = self.horizontal_border_size
        top_left_corner_y = 0
        self.create_a_quarter_numbers(numbers, 13, top_left_corner_no_13_x, top_left_corner_y)

        # numbers 19 to 24.
        top_left_corner_no_19_x = self.horizontal_border_size + self.board_play_rect_width + self.middle_border_size
        top_left_corner_y = 0
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
        b = (first_point_x_cord + SQUARE_SIZE, first_point_y_cord)
        c = (middle_point_x_cord , middle_point_y_cord)
        # left side triangle to be drawn
        left_side_down_triangle = [a, b , c]

        # right side triangle cords
        a1 = (first_point_x_cord + 6 * SQUARE_SIZE + self.middle_border_size, first_point_y_cord)
        b1 = (first_point_x_cord + 7 * SQUARE_SIZE + self.middle_border_size, first_point_y_cord)
        c1 = (middle_point_x_cord + 6 * SQUARE_SIZE + self.middle_border_size, middle_point_y_cord)
        # right side triangle to be drawn
        right_side_down_triangle = [a1, b1, c1]

        return left_side_down_triangle, right_side_down_triangle

    def draw_bottom_triangles(self, surface):
        for no_of_squares_from_left in range(6):
            if no_of_squares_from_left % 2 == 0:
                color = DARK_ORANGE3 
            else:
                color = TAN
            left_side_down_triangle, right_side_down_triangle = self.calc_bottom_triangle_cord(no_of_squares_from_left)
            
            self.draw_triangle(surface, left_side_down_triangle, right_side_down_triangle, color)


    def calc_top_triangles_cords(self, no_of_squares_from_left):
        # base cords
        first_point_x_cord = self.horizontal_border_size + no_of_squares_from_left * SQUARE_SIZE 
        first_point_y_cord = self.vertical_border_size
        middle_point_x_cord = self.horizontal_border_size + SQUARE_SIZE / 2 + no_of_squares_from_left * SQUARE_SIZE
        middle_point_y_cord = self.vertical_border_size + 5 * SQUARE_SIZE

        # left side triangle cords
        a = (first_point_x_cord , first_point_y_cord)
        b = (first_point_x_cord + SQUARE_SIZE, first_point_y_cord)
        c = (middle_point_x_cord, middle_point_y_cord)
        # left side triangle to be drawn
        left_side_down_triangle = [a, b , c]

        # right side triangle cords
        a1 = (first_point_x_cord + 6 * SQUARE_SIZE + self.middle_border_size, first_point_y_cord)
        b1 = (first_point_x_cord + 7 * SQUARE_SIZE + self.middle_border_size, first_point_y_cord)
        c1 = (middle_point_x_cord + 6 * SQUARE_SIZE + self.middle_border_size, middle_point_y_cord)
        # right side triangle to be drawn
        right_side_down_triangle = [a1, b1, c1]

        return left_side_down_triangle, right_side_down_triangle

    def draw_top_triangles(self, surface):
        for no_of_squares_from_left in range(6):
            if no_of_squares_from_left % 2 == 0:
                color = TAN
            else:
                color = DARK_ORANGE3

            left_side_down_triangle, right_side_down_triangle = self.calc_top_triangles_cords(no_of_squares_from_left)

            self.draw_triangle(surface, left_side_down_triangle, right_side_down_triangle, color)
        
    def draw_triangle(self, surface, left_side_down_triangle, right_side_down_triangle, color):
        """Drawing anti aliased polygans first will enhances the triangle quality"""
        # draw anti aliased polygans
        pygame.gfxdraw.aapolygon(surface, left_side_down_triangle, color)

        pygame.gfxdraw.aapolygon(surface, right_side_down_triangle, color)

        # draw filled polygans
        pygame.gfxdraw.filled_polygon(surface, left_side_down_triangle, color)
        
        pygame.gfxdraw.filled_polygon(surface, right_side_down_triangle, color)

    def draw_all_triangles(self, surface):
        self.draw_top_triangles(surface)
        self.draw_bottom_triangles(surface)

    def set_up_pieces_on_tri(self, tri_num, no_of_pieces, piece_color, pieces_list):
        x, y = self.triangle_first_piece_centers[tri_num]
        for piece_no in range(no_of_pieces):
            if tri_num < 13:
                piece = Piece(piece_color, 25, (x, y - piece_no * SQUARE_SIZE), tri_num)
            else:
                piece = Piece(piece_color, 25, (x, y + piece_no * SQUARE_SIZE), tri_num)
            
            if piece_color == WHITE:
                self.white_pieces.append(piece)
            else:
                self.black_pieces.append(piece)

            pieces_list[tri_num].append(piece)
            
    def create_pieces_list(self):
        pieces = {i:[] for i in range(1, 25)}
        
        """Set up white peices """
        # tri 1
        self.set_up_pieces_on_tri(1, 2, WHITE, pieces)
        # tri 122
        self.set_up_pieces_on_tri(12, 5, WHITE, pieces)
        # tri 17
        self.set_up_pieces_on_tri(17, 3, WHITE, pieces)
        # tri 19
        self.set_up_pieces_on_tri(19, 5, WHITE, pieces)


        """set up black peices"""
        # tri 6
        self.set_up_pieces_on_tri(6, 5, BLACK, pieces)
        # tri 8
        self.set_up_pieces_on_tri(8, 3, BLACK, pieces)
        # tri 13
        self.set_up_pieces_on_tri(13, 5, BLACK, pieces)
        # tri 24
        self.set_up_pieces_on_tri(24, 2, BLACK, pieces)
        
        return pieces

    def create_buttons(self):
        self.buttons = {}
        button_width = 80
        button_height = 40
        x_padding = (self.horizontal_border_size - button_width) / 2
        y_distance_between_btns = 10
        button_x = self.horizontal_border_size + self.board_play_area_width + x_padding
        undo_button_y = HEIGHT / 2 - y_distance_between_btns - button_height
        draw_button_y = HEIGHT / 2 + y_distance_between_btns 
        self.buttons["undo"] = Button(button_x, undo_button_y, button_width, button_height, WHITE, "undo")
        self.buttons["draw dices"] = Button(button_x, draw_button_y, button_width, button_height, WHITE, "draw dices")

        return self.buttons

    def create_texts(self):
        self.texts = []

        # White bar text
        white_bar_text = Text("white bar")
        white_bar_text_x = self.horizontal_border_size + self.board_play_rect_width
        white_bar_text_y = HEIGHT - self.vertical_border_size
        white_bar_text.add_paddings(white_bar_text_x, white_bar_text_y, self.middle_border_size, self.vertical_border_size)
        self.texts.append(white_bar_text)

        # Black bar text
        Black_bar_text = Text("black bar")
        Black_bar_text_x = self.horizontal_border_size + self.board_play_rect_width
        Black_bar_text_y = 0
        Black_bar_text.add_paddings(Black_bar_text_x, Black_bar_text_y, self.middle_border_size, self.vertical_border_size)
        self.texts.append(Black_bar_text)

        return self.texts

    def draw_background(self, surface):
        surface.fill(BACKGROUND_COLOR)

    def draw_borders(self, surface):

        pygame.draw.rect(surface, GRAY, self.left_border)

        pygame.draw.rect(surface, GRAY, self.right_border)

        pygame.draw.rect(surface, GRAY, self.middle_border)

        pygame.draw.rect(surface, GRAY, self.top_border)

        pygame.draw.rect(surface, GRAY, self.bottom_border)

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
        for text in self.texts:
            text.draw(surface)
        
    def draw_numbers(self, surface):
        for num in self.numbers:
            num.draw(surface)

    def draw_buttons(self, surface):
        for btn in self.buttons.values():
            btn.draw(surface, btn.name)

    def draw_pieces_in_mid(self, surface):
        for piece in self.white_pieces_in_mid:
            piece.draw_piece(surface)
        
        for piece in self.black_pieces_in_mid:
            piece.draw_piece(surface)

    def draw_pieces(self, surface):
        for i in range(1, 25):
            for piece in self.pieces[i]:
                piece.draw_piece(surface)
    
    def draw_white_pieces_in_holder(self, surface):
        piece_x = WIDTH - 2 * SQUARE_SIZE
        piece_y = self.vertical_border_size
        for piece_no in range(len(self.white_pieces_holder_list)):
            pygame.draw.rect(surface, WHITE, (piece_x, piece_y + piece_no * 12, 50, 10))

    def draw_black_pieces_in_holder(self, surface):
        piece_x = WIDTH - 2 * SQUARE_SIZE
        piece_y = self.vertical_border_size  - SQUARE_SIZE
        for piece_no in range(len(self.black_pieces_holder_list)):            
            pygame.draw.rect(surface, BLACK, (piece_x, piece_y - piece_no * 12, 50, 10))

    def draw_board(self, surface):
        
        self.draw_background(surface)
        self.draw_borders(surface)
        self.draw_all_triangles(surface)
        self.draw_numbers(surface)
        self.draw_texts(surface)
        self.draw_piece_holders(surface)
        self.draw_buttons(surface)

        self.draw_pieces(surface)
        self.draw_pieces_in_mid(surface)

        self.draw_white_pieces_in_holder(surface)
        self.draw_black_pieces_in_holder(surface)

    def set_dices(self, dices):
        for dice in dices:
            self.dices.append(dice)
            


