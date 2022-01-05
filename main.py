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
            pos = pygame.mouse.get_pos()
            x_mouse, y_mouse = pos[0], pos[1]
            
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if game.state == Game_state.DECIDE_TURNS and game.roll_dices_btn_clicked(x_mouse, y_mouse):
                    game.roll_dices()
                    if game.roll_count == 0:
                        sum_of_first_roll = game.sum_of_dice_nums()
                    else:
                        sum_of_second_roll = game.sum_of_dice_nums()
                    game.roll_count += 1
                    if game.roll_count == 2:
                        game.decide_turns(sum_of_first_roll, sum_of_second_roll)
                        game.turn_text.set_content(f"turn: {game.turn}")
                        game.state = Game_state.SELECT_ORIGIN

            if event.type == pygame.MOUSEBUTTONUP:
                game.reset_btns_color()

        game.update_board(WIN)
     
    pygame.quit()

if __name__ == "__main__":
    main()

