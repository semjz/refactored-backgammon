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

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():            
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:

                if game.state == Game_state.DECIDE_TURNS:
                    """Decide the turns adter 2 roll out"""
                    pos = pygame.mouse.get_pos()
                    x_mouse, y_mouse = pos[0], pos[1]

                    if game.roll_dices_btn_clicked(x_mouse, y_mouse):
                        game.roll_single_dice(game.roll_count + 1)
                        game.roll_count += 1
                        
                        if game.roll_count == 2:
                            if game.decide_turns():
                                game.turn_text.set_content(f"turn: {game.turn}")
                                game.state = Game_state.SELECT_ORIGIN
                            else:
                                game.roll_count = 0
                        
                    break # break so that new x and y positions are used for next game state.

                if game.state == Game_state.SELECT_ORIGIN:
                    pos = pygame.mouse.get_pos()
                    x_mouse, y_mouse = pos[0], pos[1]
                    
                    if game.dice_rolled:
                        game.select_origin(x_mouse, y_mouse)
                        if game.selected_origin:
                            game.state = Game_state.SELECT_DEST
                    
                    if game.roll_dices_btn_clicked(x_mouse, y_mouse):
                        game.roll_dices()

            if event.type == pygame.MOUSEBUTTONUP:
                game.reset_btns_color()

        game.update_board(WIN)
     
    pygame.quit()

if __name__ == "__main__":
    main()

