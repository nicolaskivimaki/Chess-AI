import pygame
from game import Game

def main():
    pygame.init()
    game = Game()
    game.game_loop()

if __name__ == "__main__":
    main()
