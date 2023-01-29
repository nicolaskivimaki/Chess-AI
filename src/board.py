
class Board():

    def __init__(self):
    
        self.board_state = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]

        self.white_to_move = True
        self.moveLog = []
    
    def make_move(self, start_square, end_square):
        print(start_square, end_square)
        start_row = start_square[1]
        start_col = start_square[0]
        end_row = end_square[1]
        end_col = end_square[0]

        to_move = self.board_state[start_row][start_col]

        if to_move == "--":
            return

        self.board_state[end_row][end_col] = to_move
        self.board_state[start_row][start_col] = "--"
    
    def change_turn(self):
        if self.white_to_move:
            self.white_to_move = False
        else:
            self.white_to_move = True
    
    def check_selected(self, x, y):
        square = self.board_state[y][x]

        if square == "--":
            return True
        else:
            return False

    def check_move(self, move):
        print("Requested move:", move)
        possible_moves = self.get_all_moves()
        if move in possible_moves:
            return True
        return False

    def get_all_moves(self):
        moves = []
        for i in range(8):
            for j in range(8):
                color = self.board_state[j][i][0]
                if (color == "w" and self.white_to_move) or (color =="b" and not self.white_to_move):
                    piece = self.board_state[j][i][1]
                    if piece == "P":
                        print("White pawn")
                        moves.append(self.get_pawn_moves(i, j, moves))
        return moves

    def get_pawn_moves(self, cols, rows, moves):

        print("OOR", cols-1, rows-1)
        print(self.board_state[cols][rows])

        if self.white_to_move:
            if self.board_state[rows-1][cols] == "--":
                moves.append([(cols, rows), (cols, rows-1)])
                if self.board_state[rows-2][cols] == "--" and rows == 6:
                    moves.append([(cols, rows), (cols, rows-2)])
            if cols in range (0, 8):
                if self.board_state[rows-1][cols-1][0] == "b":
                    moves.append([(cols, rows), (cols-1, rows-1)])
            if cols in range (0, 7):
                if self.board_state[rows-1][cols+1][0] == "b":
                    moves.append([(cols, rows), (cols+1, rows-1)])

        else:
            if rows in range(0, 7):
                if self.board_state[rows+1][cols] == "--":
                    moves.append([(cols, rows), (cols, rows+1)])
                    if self.board_state[rows+2][cols] == "--" and rows == 1:
                        moves.append([(cols, rows), (cols, rows+2)])
                if cols in range (1, 7):
                    if self.board_state[rows+1][cols-1][0] == "w":
                        moves.append([(cols, rows), (cols-1, rows+1)])
                if cols in range (0, 7):
                    if self.board_state[rows+1][cols+1][0] == "w":
                        moves.append([(cols, rows), (cols+1, rows+1)])

        print("possible moves:", moves)
        return moves

