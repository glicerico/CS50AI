"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    flat_board = board[0] + board[1] + board[2]
    x_count = flat_board.count(X)
    o_count = flat_board.count(O)
    return O if x_count > o_count else X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    action_set = set()
    for i, row in enumerate(board):
        for j, value in enumerate(row):
            if value is None:
                action_set.add((i, j))

    return action_set


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    new_board = [board[0], board[1], board[2]]  # Instead of importing deep copy library

    x, y = action  # Handy move coordinates
    if board[x][y] is not None:
        print("board position not empty!")
        raise ValueError
    else:
        new_board[x][y] = player(board)

    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    if symbol_winner(board, X):
        return X
    elif symbol_winner(board, O):
        return O
    else:
        return None


def symbol_winner(board, symbol):
    """
    Decides if "symbol" has won the game
    """
    dim = len(board)

    # Checking rows
    for i in range(dim):
        symbol_won = True
        for j in range(dim):
            if board[i][j] != symbol:
                symbol_won = False
                break
        if symbol_won:
            return symbol_won

    # Checking columns
    for i in range(dim):
        symbol_won = True
        for j in range(dim):
            if board[j][i] != symbol:
                symbol_won = False
                break
        if symbol_won:
            return symbol_won

    # Checking diagonal
    symbol_won = True
    for i in range(dim):
        if board[i][i] != symbol:
            symbol_won = False
            break
    if symbol_won:
        return symbol_won

    # Checking other diagonal
    symbol_won = True
    for i in range(dim):
        if board[i][dim - 1 - i] != symbol:
            symbol_won = False
            break
    if symbol_won:
        return symbol_won

    # If it didn't win in any of the above ways
    return False


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    if (winner(board) is not None) or all_filled(board):
        return True

    return False


def all_filled(board):
    """
    Returns True if all board is filled, False otherwise.
    """
    for i in range(len(board)):
        if board[i].count(None):
            return False

    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    this_winner = winner(board)
    if this_winner == X:
        return 1
    elif this_winner == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    raise NotImplementedError
