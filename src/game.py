import pygame
from board import Board
from constants import *
import sys
import os
dirname = os.path.dirname(__file__)

class Game():

    def __init__(self):
        self.clock = pygame.time.Clock()
        self.board = Board()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

    def game_loop(self):

        self.load_images()
        self.screen.fill(pygame.Color("white"))
        print(self.board.board_state)
        selected_squares = ()
        clicks = []

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    location = pygame.mouse.get_pos()
                    x = location[0] // SQUARE_SIZE
                    y = location[1] // SQUARE_SIZE
                    if selected_squares == (x, y):
                        selected_squares = ()
                        clicks = []
                    if len(clicks) == 0 and self.board.check_selected(x, y):
                        selected_squares = ()
                        clicks = []
                    else:
                        selected_squares = (x, y)
                        clicks.append(selected_squares)
                    if len(clicks) == 2:
                        if self.board.check_move(clicks):
                            self.board.make_move(clicks[0], clicks[1])
                            self.board.change_turn()
                            print(self.board.board_state)
                            clicks = []
                        else:
                            selected_squares = ()
                            clicks = []

            self.draw_game()
            self.clock.tick(FPS)
            pygame.display.flip()
    
    def load_images(self):
        pieces = ["bR", "bN", "bB", "bQ", "bK", "bP", "wR", "wN", "wB", "wQ", "wK", "wP"]

        for piece in pieces:
            IMAGES[piece] = pygame.transform.scale(pygame.image.load(os.path.join(dirname, "assets", f"{piece}.png")), (SQUARE_SIZE, SQUARE_SIZE))
            
    
    def draw_game(self):

        self.draw_board()
        self.drawpieces()
    
    def draw_board(self):

        for i in range(DIMENSIONS):
            for j in range(DIMENSIONS):
                if (i + j) % 2 == 0:
                    pygame.draw.rect(self.screen, WHITE, (i*SQUARE_SIZE, j*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                else:
                    pygame.draw.rect(self.screen, GREEN, (i*SQUARE_SIZE, j*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def drawpieces(self):
        for i in range(DIMENSIONS):
            for j in range(DIMENSIONS):
                piece = self.board.board_state[j][i]
                if piece != "--":
                    self.screen.blit(IMAGES[piece], pygame.Rect(i*SQUARE_SIZE, j*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

