import board

class AIEngine:

    def __init__(self):

        self.piece_scores = {"K": 0, "Q": 10, "R": 5, "B": 3, "N": 3, "P": 1}
        self.checkmate = 1000

    def find_best_move(self, board, valid_moves):

        best_move = None

        if board.white_to_move:
            turn = 1 
        else: turn = -1

        opponent_minmax_score = self.checkmate

        for player_move in valid_moves:
            board.make_move(player_move[0], player_move[1])
            board.change_turn()
            opponent_moves = board.get_valid_moves()
            opponent_max_score = -self.checkmate
            for opponent_move in opponent_moves:
                board.make_move(opponent_move[0], opponent_move[1])
                score = -turn * self.get_board_score(board.board_state)

                if score > opponent_max_score:
                    opponent_max_score = score
                
                board.undo_move()
            if opponent_max_score < opponent_minmax_score:
                opponent_minmax_score = opponent_max_score
                best_move = player_move

            board.undo_move()
            board.change_turn()

        return best_move


    def get_board_score(self, board):
        score = 0
        for row in board:
            for square in row:
                if square[0] == "w":
                    score += self.piece_scores[square[1]]
                elif square[0] == "b":
                    score -= self.piece_scores[square[1]]
        return score

