import board

class AIEngine:
    def __init__(self, depth, evaluate_fn, generate_moves_fn, is_terminal_fn):

        self.depth = depth
        self.evaluate = evaluate_fn
        self.generate_moves = generate_moves_fn
        self.is_terminal = is_terminal_fn
        self.piece_scores = {"K": 0, "Q": 10, "R": 5, "B": 3, "K": 3, "p": 1}
        self.checkmate = 1000
        
    def search(self, state, maximizing_player):

        if self.depth == 0 or self.is_terminal(state):
            return self.evaluate(state)
        
        if maximizing_player:
            best_value = float('-inf')
            for move in self.generate_moves(state):
                next_state = state.make_move(move)
                value = self.search(next_state, False)
                best_value = max(best_value, value)
            return best_value
        else:
            best_value = float('inf')
            for move in self.generate_moves(state):
                next_state = state.make_move(move)
                value = self.search(next_state, True)
                best_value = min(best_value, value)
            return best_value

    def find_best_move(self, board, valid_moves):

        best_move = None

        if board.white_to_move:
            turn = 1 
        else: turn = -1

        max_score = self.checkmate
        for player_move in valid_moves:
            board.make_move(player_move[0], player_move[1])
            score = turn * self.get_board_score(board.board_state)
            if score < max_score:
                pass


    def get_board_score(self, board):
        score = 0
        for row in board:
            for square in row:
                if square[0] == "w":
                    score + self.piece_scores[square[1]]
                elif square[0] == "b":
                    score - self.piece_scores[square[1]]

        return score

