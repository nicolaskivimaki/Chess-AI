class Minimax:
    def __init__(self, depth, evaluate_fn, generate_moves_fn, is_terminal_fn):

        self.depth = depth
        self.evaluate = evaluate_fn
        self.generate_moves = generate_moves_fn
        self.is_terminal = is_terminal_fn
        
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
