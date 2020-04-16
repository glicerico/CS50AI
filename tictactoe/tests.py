import tictactoe as ttt
from copy import deepcopy

X = "X"
O = "O"
EMPTY = None

empty_board = ttt.initial_state()

assert ttt.player(empty_board) == X

all_actions = {(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)}

assert all_actions == ttt.actions(empty_board)

# First move
first_move = deepcopy(empty_board)
first_move[0][0] = X

assert ttt.result(empty_board, (0, 0)) == first_move

winner_boardX = deepcopy(first_move)
winner_boardX[0][1] = X
winner_boardX[0][2] = X

assert not ttt.terminal(empty_board)
assert ttt.terminal(winner_boardX)
assert ttt.winner(winner_boardX) == X
assert ttt.utility(winner_boardX) == 1

winner_boardO = deepcopy(empty_board)
winner_boardO[0][1] = O
winner_boardO[1][1] = O
winner_boardO[2][1] = O

assert ttt.terminal(winner_boardO)
assert ttt.winner(winner_boardO) == O
assert ttt.utility(winner_boardO) == -1

winner_board_diagonal = deepcopy(empty_board)
winner_board_diagonal[2][0] = O
winner_board_diagonal[1][1] = O
winner_board_diagonal[0][2] = O
winner_board_diagonal[0][0] = X
winner_board_diagonal[1][0] = X

assert ttt.terminal(winner_board_diagonal)
assert ttt.winner(winner_board_diagonal) == O
assert ttt.utility(winner_board_diagonal) == -1

tied_board = deepcopy(empty_board)
tied_board[0][0] = X
tied_board[1][0] = X
tied_board[2][1] = X
tied_board[0][2] = X
tied_board[1][2] = X
tied_board[0][1] = O
tied_board[1][1] = O
tied_board[2][0] = O
tied_board[2][2] = O

assert ttt.terminal(tied_board)
assert ttt.winner(tied_board) is None
assert ttt.utility(tied_board) == 0
