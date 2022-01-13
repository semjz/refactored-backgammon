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

        for event in pygame.event.get():            
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and game.state == Game_state.DECIDE_TURNS:
                pos = pygame.mouse.get_pos()
                x_mouse, y_mouse = pos[0], pos[1]

                if game.roll_dices_btn_clicked(x_mouse, y_mouse):
                    game.roll_single_dice(roll_count + 1)
                    roll_count += 1
                
                """Decide the turns after 2 roll out"""
                if roll_count == 2:
                    if game.decide_turns():
                        game.turn_text.set_content(f"turn: {game.turn}")
                        game.state = Game_state.SELECT_ORIGIN
                        game.set_move_info()
                    else:
                        roll_count = 0

                break # break so that next state uses new mouse cords.        

            if event.type == pygame.MOUSEBUTTONDOWN and game.state == Game_state.SELECT_ORIGIN:
                pos = pygame.mouse.get_pos()
                x_mouse, y_mouse = pos[0], pos[1]
                
                if game.dice_is_rolled:
                    game.select_origin(x_mouse, y_mouse)
                    if game.selected_origin:
                        game.state = Game_state.SELECT_DEST
                
                elif game.roll_dices_btn_clicked(x_mouse, y_mouse):
                    game.roll_dices()

                break # break so that next state uses new mouse cords. 

            if event.type == pygame.MOUSEBUTTONDOWN and game.state == Game_state.SELECT_DEST:
                pos = pygame.mouse.get_pos()
                x_mouse, y_mouse = pos[0], pos[1]

                game.select_dest(x_mouse, y_mouse)
                if game.selected_dest:
                    game.set_move_distance_and_direction()
                    if game.is_valid_move_on_board():
                        game.state = Game_state.MOVE
                    

            if event.type == pygame.MOUSEBUTTONDOWN and game.state == Game_state.MOVE:
                game.move_on_board()
                game.state = Game_state.SELECT_ORIGIN
                if game.no_of_moves_left == 0:
                    game.change_turn()
                    game.turn_text.set_content(f"turn: {game.turn}")

            if event.type == pygame.MOUSEBUTTONUP:
                game.reset_btns_color()

        game.update_board(WIN)
     
    pygame.quit()

if __name__ == "__main__":
    main()

