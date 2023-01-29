import unittest
import pytest
import pygame
from constants import *
from game import Game

class TestGame(unittest.TestCase):

    def setUp(self):
        self.game = Game()
        self.game.load_images()

    def test_init(self):
        self.assertIsNotNone(self.game.board)
        self.assertIsNotNone(self.game.screen)
        self.assertIsNotNone(self.game.clock)
        
    def test_load_images(self):
        self.game.load_images()
        self.assertIsNotNone(IMAGES["bR"])
        self.assertIsNotNone(IMAGES["wP"])
        
    def test_draw_game(self):
        self.game.draw_game()
        # Use pygame.Surface.get_at() to check the color of a pixel in the screen surface
        self.assertEqual(self.game.screen.get_at((0, 0)), WHITE)
        self.assertEqual(self.game.screen.get_at((SQUARE_SIZE, 0)), GREEN)
        
    def test_draw_board(self):
        self.game.draw_board()
        self.assertEqual(self.game.screen.get_at((0, 0)), WHITE)
        self.assertEqual(self.game.screen.get_at((SQUARE_SIZE, 0)), GREEN)

    def test_drawpieces(self):
        self.game.drawpieces()
        self.assertIsNotNone(self.game.screen.get_at((0, 0)))

if __name__ == '__main__':
    unittest.main()
