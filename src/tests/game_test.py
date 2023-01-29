import unittest
import pytest
import pygame
from constants import *
from game import Game
from board import Board

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


class TestBoard(unittest.TestCase):

    def setUp(self):
        self.board = Board()

    def test_init(self):
        self.assertEqual(self.board.board_state, [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ])
        self.assertTrue(self.board.white_to_move)

    def test_move_black_pawns(self):
        self.board.make_move((0, 1), (0, 2))
        self.assertEqual(self.board.board_state, [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["--", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["bP", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ])

        self.board.change_turn()

        self.board.make_move((7, 1), (7, 3))
        self.assertEqual(self.board.board_state, [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["--", "bP", "bP", "bP", "bP", "bP", "bP", "--"],
            ["bP", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ])
    
    def test_move_white_pawns_(self):
        self.board.make_move((0, 6), (0, 5))
        self.assertEqual(self.board.board_state, [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ])

        self.board.change_turn()

        self.board.make_move((1, 6), (1, 4))
        self.assertEqual(self.board.board_state, [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "wP", "--", "--", "--", "--", "--", "--"],
            ["wP", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ])

    def test_pawns_take(self):
        self.board.make_move((4, 6), (4, 4))
        self.board.make_move((4, 1), (4, 3))
        self.board.make_move((3, 6), (3, 4))
        self.board.make_move((3, 1), (3, 3))
        self.board.make_move((4, 4), (3, 3))
        self.board.make_move((4, 3), (3, 4))

        self.assertEqual(self.board.board_state, [
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'], 
            ['bP', 'bP', 'bP', '--', '--', 'bP', 'bP', 'bP'], 
            ['--', '--', '--', '--', '--', '--', '--', '--'], 
            ['--', '--', '--', 'wP', '--', '--', '--', '--'], 
            ['--', '--', '--', 'bP', '--', '--', '--', '--'], 
            ['--', '--', '--', '--', '--', '--', '--', '--'], 
            ['wP', 'wP', 'wP', '--', '--', 'wP', 'wP', 'wP'], 
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']
        ])

    def test_check_moves(self):
        self.assertTrue(self.board.check_move([(0, 6), (0, 5)]))
        self.assertFalse(self.board.check_move([(0, 6), (0, 2)]))

    def test_change_turn(self):
        self.board.change_turn()
        self.assertFalse(self.board.white_to_move)
        self.board.change_turn()
        self.assertTrue(self.board.white_to_move)

    def test_check_selected(self):
        self.assertTrue(self.board.check_selected(2, 3))
        self.assertFalse(self.board.check_selected(0, 0))


if __name__ == '__main__':
    unittest.main()
