import pygame
from board import Board
from constants import *


FPS = 60
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Backgammon")


def main():
    running = True
    clock = pygame.time.Clock()
    board = Board()

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        board.draw_board(WIN)
        pygame.display.update()
     
    pygame.quit()

if __name__ == "__main__":
    main()

