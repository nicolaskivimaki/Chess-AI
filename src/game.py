import pygame
from board import Board
from constants import *
import sys
import os
dirname = os.path.dirname(__file__)

"""
This module contains the Game class which is responsible for the overall 
management of the chess game. It uses the pygame library for the graphical 
representation of the game. It also uses the Board class from the board 
module for game logic and constant variables from the constants module.
"""

class Game():

    def __init__(self):

        """
        Initializes the game: creates the game clock, chess board, and the game screen.
        """
        self.clock = pygame.time.Clock()
        self.board = Board()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

    def game_loop(self):

        """
        This is the main game loop that handles game events, updates the board state
        and renders the game onto the screen.
        """

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

        """
        Loads images for each piece on the chess board.
        """
        pieces = ["bR", "bN", "bB", "bQ", "bK", "bP", "wR", "wN", "wB", "wQ", "wK", "wP"]

        for piece in pieces:
            IMAGES[piece] = pygame.transform.scale(pygame.image.load(os.path.join(dirname, "assets", f"{piece}.png")), (SQUARE_SIZE, SQUARE_SIZE))
            
    
    def draw_game(self):

        """
        Calls the draw.board and draw_pieces methods to 
        draw the board and pieces onto the screen.
        """

        self.draw_board()
        self.drawpieces()
    
    def draw_board(self):

        """
        Draws the board onto the screen.
        """

        for i in range(DIMENSIONS):
            for j in range(DIMENSIONS):
                if (i + j) % 2 == 0:
                    pygame.draw.rect(self.screen, WHITE, (i*SQUARE_SIZE, j*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                else:
                    pygame.draw.rect(self.screen, GREEN, (i*SQUARE_SIZE, j*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def drawpieces(self):

        """
        Draws the pieces onto the board based on their location in
        the board state list.
        """

        for i in range(DIMENSIONS):
            for j in range(DIMENSIONS):
                piece = self.board.board_state[j][i]
                if piece != "--":
                    self.screen.blit(IMAGES[piece], pygame.Rect(i*SQUARE_SIZE, j*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
