import random

class Board():

    """
    This class represents the state of the chess board,
    including the positions of all pieces and the current
    player's turn.
    """

    def __init__(self):

        """
        Initializes the chess board with the starting positions of all pieces,
        sets the current player to white, and creates an empty move log.
        """

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
        self.move_log = []
        self.captured_piece = ""
        self.possible_moves = []

    def engine_move(self):
        all_moves = self.get_all_moves()
        valid_moves = []
        for move in all_moves:
            if not self.check_for_check(move):
                valid_moves.append(move)

        random_move = random.choice(valid_moves)
        self.make_move(random_move[0], random_move[1])


    def make_move(self, start_square, end_square):

        """
        Takes the starting square and ending square of a move
        and updates the board state accordingly.
        """
        self.move_log.append([start_square, end_square])

        start_row = start_square[1]
        start_col = start_square[0]
        end_row = end_square[1]
        end_col = end_square[0]

        to_move = self.board_state[start_row][start_col]
        move_to = self.board_state[end_row][end_col]

        if to_move == "--":
            return

        if move_to == "--":
            self.captured_piece = "--"
        else:
            self.captured_piece = move_to

        self.board_state[end_row][end_col] = to_move
        self.board_state[start_row][start_col] = "--"

    def undo_move(self):

        last_move = self.move_log[-1]
        start_square = last_move[0]
        end_square = last_move[1]

        start_row = start_square[1]
        start_col = start_square[0]
        end_row = end_square[1]
        end_col = end_square[0]

        moved_from = self.board_state[start_row][start_col]
        moved_to = self.board_state[end_row][end_col]

        self.board_state[start_row][start_col] = moved_to
        self.board_state[end_row][end_col] = self.captured_piece

    def change_turn(self):

        """
        Changes the current player's turn.
        """

        if self.white_to_move:
            self.white_to_move = False
        else:
            self.white_to_move = True

    def check_selected(self, x, y):

        """
        Takes in the selected square and checks whether
        an empty square or a piece was clicked.
        """

        square = self.board_state[y][x]

        if square == "--":
            return True

        return False

    def check_move(self, suggested_move):

        """
        Takes in a move chosen by the user and checks if
        it is a valid move according to the current board state.
        Returns True if valid, False otherwise.
        """

        possible_moves = self.get_all_moves()
        valid_moves = []
        for move in possible_moves:
            if not self.check_for_check(move):
                valid_moves.append(move)
        if suggested_move in valid_moves:
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
                        moves = self.get_pawn_moves(i, j, moves)
                    if piece == "B":
                        moves = self.get_bishop_moves(i, j, moves)
                    if piece == "R":
                        moves = self.get_rook_moves(i, j, moves)
                    if piece == "N":
                        moves = self.get_knight_moves(i, j, moves)
                    if piece == "K":
                        moves = self.get_king_moves(i, j, moves)
                    if piece == "Q":
                        moves = self.get_queen_moves(i, j, moves)
        return moves

    def check_for_check(self, move):
        """
        Returns True if the king of the current player is in check.
        """
        print("CHECKING: ", move)
        self.make_move(move[0], move[1])
        self.change_turn()
        opponent_moves = self.get_all_moves()
        for i in self.board_state:
            print(i)

        for possible_move in opponent_moves:
            end_square = possible_move[1]
            row = end_square[1]
            col = end_square[0]
            if self.board_state[row][col] == "bK" and self.white_to_move:
                print("THREATENING MOVE: ", possible_move)
                self.undo_move()
                self.change_turn()
                return True
        self.undo_move()
        self.change_turn()
        return False

    
    def check_for_stalemate(self):
        """
        Returns True if the current player is in stalemate.
        """
        if self.check_for_check():
            return False
        moves = self.get_all_moves()
        return len(moves) == 0


    def get_pawn_moves(self, cols, rows, moves):

        """
        Takes the location of a pawn and return all possible
        moves considering it's surrounding squares and
        chess rules.
        """

        if self.white_to_move:
            if self.board_state[rows-1][cols] == "--":
                moves.append([(cols, rows), (cols, rows-1)])
                if rows >= 6 and self.board_state[rows-2][cols] == "--":
                    moves.append([(cols, rows), (cols, rows-2)])
            if cols in range(0, 8):
                if self.board_state[rows-1][cols-1][0] == "b":
                    moves.append([(cols, rows), (cols-1, rows-1)])
            if cols in range(0, 7):
                if self.board_state[rows-1][cols+1][0] == "b":
                    moves.append([(cols, rows), (cols+1, rows-1)])
        else:
            if rows + 1 < len(self.board_state):
                if self.board_state[rows+1][cols] == "--":
                    moves.append([(cols, rows), (cols, rows+1)])
                    if rows <= 1 and self.board_state[rows+2][cols] == "--" and rows+2 < len(self.board_state):
                        moves.append([(cols, rows), (cols, rows+2)])
                if cols in range(0, 7):
                    if self.board_state[rows+1][cols-1][0] == "w":
                        moves.append([(cols, rows), (cols-1, rows+1)])
                if cols in range(0, 7):
                    if self.board_state[rows+1][cols+1][0] == "w":
                        moves.append([(cols, rows), (cols+1, rows+1)])
        return moves


    def get_bishop_moves(self, cols, rows, moves):
        """
        Takes the location of a bishop and returns all possible
        moves considering the chess rules.
        """
        # Check up and left direction
        if self.white_to_move:
            enemy_color = "b"  
        else:
            enemy_color = "w"

        row, col = rows - 1, cols - 1
        while row >= 0 and col >= 0:
            if self.board_state[row][col] == "--":
                moves.append([(cols, rows), (col, row)])
                row -= 1
                col -= 1
            elif self.board_state[row][col][0] == enemy_color:
                moves.append([(cols, rows), (col, row)])
                break
            else:
                break

        # Check up and right direction
        row, col = rows - 1, cols + 1
        while row >= 0 and col < 8:
            if self.board_state[row][col] == "--":
                moves.append([(cols, rows), (col, row)])
                row -= 1
                col += 1
            elif self.board_state[row][col][0] == enemy_color:
                moves.append([(cols, rows), (col, row)])
                break
            else:
                break

        # Check down and left direction
        row, col = rows + 1, cols - 1
        while row < 8 and col >= 0:
            if self.board_state[row][col] == "--":
                moves.append([(cols, rows), (col, row)])
                row += 1
                col -= 1
            elif self.board_state[row][col][0] == enemy_color:
                moves.append([(cols, rows), (col, row)])
                break
            else:
                break

        # Check down and right direction
        row, col = rows + 1, cols + 1
        while row < 8 and col < 8:
            if self.board_state[row][col] == "--":
                moves.append([(cols, rows), (col, row)])
                row += 1
                col += 1
            elif self.board_state[row][col][0] == enemy_color:
                moves.append([(cols, rows), (col, row)])
                break
            else:
                break

        return moves

    def get_rook_moves(self, cols, rows, moves):
        """
        Takes the location of a rook and returns all possible
        moves considering the chess rules.
        """

        if self.white_to_move:
            enemy_color = "b"  
        else:
            enemy_color = "w"
        
        # Check up direction
        for row in range(rows-1, -1, -1):
            if self.board_state[row][cols] == "--":
                moves.append([(cols, rows), (cols, row)])
            elif self.board_state[row][cols][0] == enemy_color:
                moves.append([(cols, rows), (cols, row)])
                break
            else:
                break
            
        # Check down direction
        for row in range(rows+1, 8):
            if self.board_state[row][cols] == "--":
                moves.append([(cols, rows), (cols, row)])
            elif self.board_state[row][cols][0] == enemy_color:
                moves.append([(cols, rows), (cols, row)])
                break
            else:
                break

        # Check left direction
        for col in range(cols-1, -1, -1):
            if self.board_state[rows][col] == "--":
                moves.append([(cols, rows), (col, rows)])
            elif self.board_state[rows][col][0] == enemy_color:
                moves.append([(cols, rows), (col, rows)])
                break
            else:
                break

        # Check right direction
        for col in range(cols+1, 8):
            if self.board_state[rows][col] == "--":
                moves.append([(cols, rows), (col, rows)])
            elif self.board_state[rows][col][0] == enemy_color:
                moves.append([(cols, rows), (col, rows)])
                break
            else:
                break

        return moves

    def get_knight_moves(self, cols, rows, moves):

        """
        Takes the location of a knight and returns all possible
        moves considering it's surrounding squares and
        chess rules.
        """
        movements = [
            [-2, -1], [-2, 1], [-1, -2], [-1, 2],
            [1, -2], [1, 2], [2, -1], [2, 1]
        ]

        for movement in movements:
            if (0 <= rows + movement[0] < 8) and (0 <= cols + movement[1] < 8):
                end_square = (cols + movement[1], rows + movement[0])
                if self.board_state[end_square[1]][end_square[0]][0] != self.board_state[rows][cols][0]:
                    moves.append([(cols, rows), end_square])
        return moves

    def get_king_moves(self, col, row, moves):

        for i in range(-1, 2):
            for j in range(-1, 2):
                new_col = col + i
                new_row = row + j
                if new_col in range(0, 8) and new_row in range(0, 8):
                    destination = self.board_state[new_row][new_col]
                    if destination == "--" or destination[0] != self.board_state[row][col][0]:
                        moves.append([(col, row), (new_col, new_row)])
        return moves

    def get_queen_moves(self, col, row, moves):
        moves = (self.get_bishop_moves(col, row, moves))
        moves = (self.get_rook_moves(col, row, moves))
        return moves
