import pygame
from game import Game
from game_state import Game_state
from constants import *


FPS = 60
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Backgammon")


def main():
    running = True
    clock = pygame.time.Clock()
    game = Game()
    roll_count = 0

    while running:
        clock.tick(FPS)

        game.calc_lowest_home_tri_num_with_white_piece()
        game.calc_highest_home_tri_num_with_black_piece()

        if game.state == Game_state.SELECT_ORIGIN and game.dice_is_rolled \
            and not game.valid_move_exist_on_board() \
            and not game.valid_move_exist_to_piece_holder():
            
                game.move_exist_text.set_content(f"No valid move for {game.turn}")
                game.turn_text.set_content(f"{game.turn}'s turn")
                game.dice_is_rolled = False
                game.change_turn()

        if game.state == Game_state.PIECE_ON_BAR and game.dice_is_rolled \
            and not game.valid_move_exist_from_mid_to_board():
            
                game.state = Game_state.SELECT_ORIGIN
                game.move_exist_text.set_content(f"No valid move for {game.turn}")
                game.dice_is_rolled = False
                game.change_turn()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and game.state == Game_state.DECIDE_TURNS:
                x_mouse, y_mouse = pygame.mouse.get_pos()

                if game.roll_dices_btn_clicked(x_mouse, y_mouse):
                    game.roll_single_dice(roll_count + 1)
                    roll_count += 1
                
                """Decide the turns after 2 roll out"""
                if roll_count == 2 and game.decide_turns():
                    game.turn_text.set_content(f"{game.turn}'s turn")
                    game.state = Game_state.SELECT_ORIGIN
                    game.set_move_info()
                
                if roll_count == 2 and not game.decide_turns():
                    roll_count = 0

                break  # break so that next state uses new mouse cords.        

            if event.type == pygame.MOUSEBUTTONDOWN and game.state == Game_state.SELECT_ORIGIN:
                x_mouse, y_mouse = pygame.mouse.get_pos()
                
                if game.dice_is_rolled and game.select_origin(x_mouse, y_mouse):
                    game.state = Game_state.SELECT_DEST
                
                elif not game.dice_is_rolled and game.roll_dices_btn_clicked(x_mouse, y_mouse):
                    game.roll_dices()
                    if not game.valid_move_exist_on_board() and not game.valid_move_exist_to_piece_holder():
                        game.move_exist_text.set_content(f"No valid move for {game.turn}")
                        game.turn_text.set_content(f"{game.turn}'s turn")
                        game.dice_is_rolled = False
                        game.change_turn()
                    else:
                        game.move_exist_text.set_content(f"")
                        game.turn_text.set_content(f"{game.turn}'s turn")
                break  # break so that next state uses new mouse cords.

            if event.type == pygame.MOUSEBUTTONDOWN and game.state == Game_state.SELECT_DEST:
                x_mouse, y_mouse = pygame.mouse.get_pos()

                if not game.mid_bar_piece_selected and game.undo_btn_clicked(x_mouse, y_mouse):
                    game.deselect_origin()
                    game.state = Game_state.SELECT_ORIGIN

                elif game.select_dest(x_mouse, y_mouse) and game.is_valid_move_on_board(game.selected_origin, game.selected_dest):
                    game.state = Game_state.MOVE

                elif game.select_dest(x_mouse, y_mouse) and game.is_valid_move_to_piece_holders(game.selected_origin, game.selected_dest):
                    game.state = Game_state.MOVE_TO_PLACE_HOLDER

            if event.type == pygame.MOUSEBUTTONDOWN and game.state == Game_state.MOVE:
                game.move_on_board()
                game.state = Game_state.SELECT_ORIGIN
                
                if game.get_no_of_moves_left() == 0:
                    game.change_turn()
                    game.turn_text.set_content(f"{game.turn}'s turn")
                
                if game.turns_color_piece_on_mid_bar():
                    game.state = Game_state.PIECE_ON_BAR

            if event.type == pygame.MOUSEBUTTONDOWN and game.state == Game_state.MOVE_TO_PLACE_HOLDER:
                game.move_to_piece_holder()
                game.state = Game_state.SELECT_ORIGIN
                
                if game.check_winner_determined():
                    game.state = Game_state.END

                if game.no_of_moves_left == 0:
                    game.change_turn()
                    game.turn_text.set_content(f"{game.turn}'s turn")

                if game.turns_color_piece_on_mid_bar():
                    game.state = Game_state.PIECE_ON_BAR

                
            if event.type == pygame.MOUSEBUTTONDOWN and game.state == Game_state.PIECE_ON_BAR:
                x_mouse, y_mouse = pygame.mouse.get_pos()
                
                if game.dice_is_rolled and game.valid_move_exist_from_mid_to_board() \
                    and game.select_piece_on_mid_bar(x_mouse, y_mouse):
                    game.state = Game_state.SELECT_DEST

                # if dice is not rolled, it must be rolled first and game checks if there are
                # any valid moves from mid to the board.
                elif not game.dice_is_rolled and game.roll_dices_btn_clicked(x_mouse, y_mouse):
                    game.roll_dices()
                    if not game.valid_move_exist_from_mid_to_board():
                        game.state = Game_state.SELECT_ORIGIN
                        game.move_exist_text.set_content(f"No valid move for {game.turn}")
                        game.dice_is_rolled = False
                        game.change_turn()

            if event.type == pygame.MOUSEBUTTONUP:
                game.reset_btns_color()

        game.update_board(WIN)
     
    pygame.quit()

if __name__ == "__main__":
    main()
    