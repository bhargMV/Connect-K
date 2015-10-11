from util import memoize, run_search_function, INFINITY, NEG_INFINITY
from operator import itemgetter
import copy
nodes_expanded = 0

def basic_evaluate(board):
    """
    The original focused-evaluate function from the lab.
    The original is kept because the lab expects the code in the lab to be modified. 
    """
    if board.is_game_over():
        # If the game has been won, we know that it must have been
        # won or ended by the previous move.
        # The previous move was made by our opponent.
        # Therefore, we can't have won, so return -1000.
        # (note that this causes a tie to be treated like a loss)
        score = -1000
    else:
        score = board.longest_chain(board.get_current_player_id()) * 10
        # Prefer having your pieces in the center of the board.
        for row in range(6):
            for col in range(7):
                if board.get_cell(row, col) == board.get_current_player_id():
                    score -= abs(3-col)
                elif board.get_cell(row, col) == board.get_other_player_id():
                    score += abs(3-col)

    return score


def get_all_next_moves(board):
    """ Return a generator of all moves that the current player could take from this position """
    from connectfour import InvalidMoveException

    for i in xrange(board.board_width):
        try:
            yield (i, board.do_move(i))
        except InvalidMoveException:
            pass

def is_terminal(depth, board):
    """
    Generic terminal state check, true when maximum depth is reached or
    the game has ended.
    """
    return depth <= 0 or board.is_game_over()

def get_diff_in_boards(old_board, new_board):
    """
    :param old_board: The old board state
    :param new_board: The new board wherein one move is more compared to the old board
    :return: The mismatched column
    """
    for i in range(6):
        for j in range(7):
            if old_board.get_cell(i,j) != new_board.get_cell(i,j):
                return j

def get_best_minimax_board(board, depth, is_max, eval_fn = basic_evaluate,
            get_next_moves_fn = get_all_next_moves,
            is_terminal_fn = is_terminal,
            verbose = True):
    """
    :param board: the ConnectFourBoard instance to evaluate
    :param depth: the depth of the search tree (measured in maximum distance from a leaf to the root)
    :param is_max: maximizing player
    :param eval_fn:
    :param get_next_moves_fn:
    :param is_terminal_fn:
    :param verbose:
    :return: (Evaluated value of the board, The board)
    """
    global nodes_expanded
    if is_terminal_fn(depth, board):
        # Return the evaluate function of the board and the board
        return (eval_fn(board),board)

    scores = []
    children = get_next_moves_fn(board)

    if is_max:
        for child in children:
            nodes_expanded = nodes_expanded + 1
            scores.append(get_best_minimax_board(child[1], depth-1, False))
        return max(scores,key=itemgetter(0))
    else:
        for child in children:
            nodes_expanded = nodes_expanded + 1
            scores.append(get_best_minimax_board(child[1], depth-1, True))
        return min(scores,key=itemgetter(0))


def minimax(board, depth, eval_fn = basic_evaluate,
            get_next_moves_fn = get_all_next_moves,
            is_terminal_fn = is_terminal,
            verbose = True):
    """
    Do a minimax search to the specified depth on the specified board.

    board -- the ConnectFourBoard instance to evaluate
    depth -- the depth of the search tree (measured in maximum distance from a leaf to the root)
    eval_fn -- (optional) the evaluation function to use to give a value to a leaf of the tree see "focused_evaluate" in the lab for an example

    Returns an integer, the column number of the column that the search determines you should add a token to
    """
    (score, new_board) = get_best_minimax_board(board, depth, True, eval_fn)
    return get_diff_in_boards(board, new_board)
    # raise NotImplementedError

def rand_select(board):
    """
    Pick a column by random
    """
    import random
    moves = [move for move, new_board in get_all_next_moves(board)]
    return moves[random.randint(0, len(moves) - 1)]


def new_evaluate(board):
    """
    :param board: The game board
    :return: Difference of wins of X and wins of O in given board state.
    """
    winsO = 0 # Wins for Opponent
    winsX = 0 # Wins for Me

    for j in range(0,7):

        # Gets the top most element of the column.
        i = get_top(board, j)

        # Empty column
        if i == 6:

            # Count wins for elements in the column left to current column.
            if(j-1 >= 0):
                t = get_top(board, j-1)
                b = 5

                while(b >= t):
                    if(board.get_cell(b, j-1) == 2):
                        winsO = winsO + wins_left(board, copy.deepcopy(b), copy.deepcopy(j-1), 2) + \
                                wins_left_diagonal(board, copy.deepcopy(b), copy.deepcopy(j-1), 2) + \
                                wins_straight(board, copy.deepcopy(b), copy.deepcopy(j-1), 2) + \
                                wins_right_diagonal(board, copy.deepcopy(b), copy.deepcopy(j-1), 2) + \
                                wins_right(board, copy.deepcopy(b), copy.deepcopy(j-1), 2)
                    else:
                        winsX = winsX + wins_left(board, copy.deepcopy(b), copy.deepcopy(j-1), 1) + \
                                wins_left_diagonal(board, copy.deepcopy(b), copy.deepcopy(j-1), 1) + \
                                wins_straight(board, copy.deepcopy(b), copy.deepcopy(j-1), 1) + \
                                wins_right_diagonal(board, copy.deepcopy(b), copy.deepcopy(j-1), 1) + \
                                wins_right(board, copy.deepcopy(b), copy.deepcopy(j-1), 1)
                    b -= 1

            # Count wins for elements in the column right to current column.
            if(j+1 <= 6):
                t = get_top(board, j+1)
                b = 5

                while(b >= t):
                    if(board.get_cell(b, j+1) == 2):
                        winsO = winsO + wins_left(board, copy.deepcopy(b), copy.deepcopy(j+1), 2) + \
                                wins_left_diagonal(board, copy.deepcopy(b), copy.deepcopy(j+1), 2) + \
                                wins_straight(board, copy.deepcopy(b), copy.deepcopy(j+1), 2) + \
                                wins_right_diagonal(board, copy.deepcopy(b), copy.deepcopy(j+1),2) + \
                                wins_right(board, copy.deepcopy(b), copy.deepcopy(j+1), 2)
                    else:
                        winsX = winsX + wins_left(board, copy.deepcopy(b), copy.deepcopy(j+1), 1) + \
                                wins_left_diagonal(board, copy.deepcopy(b), copy.deepcopy(j+1), 1) + \
                                wins_straight(board, copy.deepcopy(b), copy.deepcopy(j+1), 1) + \
                                wins_right_diagonal(board, copy.deepcopy(b), copy.deepcopy(j+1), 1) + \
                                wins_right(board, copy.deepcopy(b), copy.deepcopy(j+1), 1)
                    b = b - 1

        # If top most element in the column is 'O'
        elif board.get_cell(i, j) == 2:
            winsO = winsO + wins_left(board, copy.deepcopy(i), copy.deepcopy(j), 2) + \
                    wins_left_diagonal(board, copy.deepcopy(i), copy.deepcopy(j), 2) + \
                    wins_straight(board, copy.deepcopy(i), copy.deepcopy(j), 2) + \
                    wins_right_diagonal(board, copy.deepcopy(i), copy.deepcopy(j), 2) + \
                    wins_right(board, copy.deepcopy(i), copy.deepcopy(j), 2)

        # Else if top most element in the column is 'X'
        else:
            winsX = winsX + wins_left(board, copy.deepcopy(i), copy.deepcopy(j), 1) + \
                    wins_left_diagonal(board, copy.deepcopy(i), copy.deepcopy(j), 1) + \
                    wins_straight(board, copy.deepcopy(i), copy.deepcopy(j), 1) + \
                    wins_right_diagonal(board, copy.deepcopy(i), copy.deepcopy(j), 1) + \
                    wins_right(board, copy.deepcopy(i), copy.deepcopy(j), 1)

    return (winsX - winsO)

def get_top(board, j):
    """
    :param board: Game board
    :param j:
    :return: Index of top most element in the column, 6 if there are no elements in column
    """
    t = 6
    while(t > 0):
        if board.get_cell(t-1, j) == 0:
            break
        t -= 1
    return t

def wins_left(board, i, j, c):
    """
    Calculates if there is a win towards left from the current index
    :param board: Game board
    :param i: row
    :param j: col
    :param c: integer to denote current player
    :return: 1000 if current player has won, 1 if there is a possible win, 0 otherwise
    """
    count = 1
    empty = 1
    k = board.get_k_value()

    if(((j+1) <= 6) and (board.get_cell(i, j+1) == c) and (get_top(board, j+1) == i)):
        return 0

    while(j >= 1 and (board.get_cell(i, j-1) == c)):
        count = count + 1
        j -= 1

    if(count >= k):
        return 1000

    while(j >= 0 and ((board.get_cell(i, j) == 0) or (board.get_cell(i, j) == c))):
        empty = empty + 1
        j -= 1

    if empty >= k:
        return 1

    return 0

def wins_left_diagonal(board, i, j, c):
    """
    Calculates if there is a win towards left dagonal from the current index
    :param board: Game board
    :param i: row
    :param j: col
    :param c: integer to denote current player
    :return: 1000 if current player has won, 1 if there is a possible win, 0 otherwise
    """
    count = 1
    empty = 1

    temp1 = i
    temp2 = j
    k = board.get_k_value()

    if((i>=1) and (j>=1) and (board.get_cell(i-1, j-1) == c)  and get_top(board, j-1) == i-1):
        return 0

    i += 1
    j += 1

    while((j <= 6) and (i <= 5) and (board.get_cell(i, j) == c)):
        count = count + 1
        i += 1
        j += 1


    if(count >= k):
        return 1000

    i = temp1
    j = temp2
    i -= 1
    j -= 1

    while((j >= 0) and (i >= 0) and ((board.get_cell(i, j) == 0) or (board.get_cell(i, j) == c))):
        empty = empty + 1
        i = i - 1
        j = j - 1

    if(empty >= k):
        return 1

    i = temp1
    j = temp2
    i = i + 1
    j = j + 1

    while((j <= 6) and (i <= 5) and ((board.get_cell(i, j) == 0) or board.get_cell(i, j) == c)):
        empty = empty + 1
        i = i + 1
        j = j + 1

    if(empty >= k):
        return 1

    return 0

def wins_straight(board, i, j, c):
    """
    Calculates if there is a win upwards from the current index
    :param board: Game board
    :param i: row
    :param j: col
    :param c: integer to denote current player
    :return: 1000 if current player has won, 1 if there is a possible win, 0 otherwise
    """
    count = 1
    empty = 1
    temp = i
    k = board.get_k_value()

    while(i <= 4 and board.get_cell(i+1, j) == c):
        count = count + 1
        i = i + 1

    if(count >= k):
        return 1000

    i = temp
    i = i - 1

    while(i >= 0 and board.get_cell(i, j) == 0):
        empty = empty + 1
        i = i - 1

    if((count + empty) >= k):
        return 1

    return 0

def wins_right_diagonal(board, i, j, c):
    """
    Calculates if there is a win towards right diagonal from the current index
    :param board: Game board
    :param i: row
    :param j: col
    :param c: integer to denote current player
    :return: 1000 if current player has won, 1 if there is a possible win, 0 otherwise
    """
    count = 1
    empty = 1

    temp1 = i
    temp2 = j
    k = board.get_k_value()

    if((i >= 1) and (j <= 5) and (board.get_cell(i-1, j+1) == c) and (get_top(board, j+1) == i-1)):
        return 0

    i = i + 1
    j = j - 1

    while((j >= 0) and (i <= 5) and board.get_cell(i, j) == c):
        count = count + 1
        i += 1
        j -= 1


    if(count >= k):
        return 1000

    i = temp1
    j = temp2
    i -= 1
    j += 1

    while((j <= 6) and (i >= 0) and ((board.get_cell(i, j) == 0) or (board.get_cell(i, j) == c))):
        empty += 1
        i = i - 1
        j = j + 1

    if(empty >= k):
        return 1

    i = temp1
    j = temp2
    i += 1
    j -= 1

    while((j >= 0) and (i <= 5) and ((board.get_cell(i, j) == 0) or board.get_cell(i, j) == c)):
        empty += 1
        i = i + 1
        j = j - 1

    if(empty >= k):
        return 1

    return 0

def wins_right(board, i, j, c):
    """
    Calculates if there is a win towards right from the current index
    :param board: Game board
    :param i: row
    :param j: col
    :param c: integer to denote current player
    :return: 1000 if current player has won, 1 if there is a possible win, 0 otherwise
    """
    count = 1
    empty = 1
    temp = j
    k = board.get_k_value()

    if(((j+1) <= 6) and board.get_cell(i, j+1) == c and get_top(board, j+1) == i):
        return 0

    while(j >= 1 and (board.get_cell(i, j-1) == c)):
        count = count + 1
        j -= 1

    if(count >= k):
        return 1000

    j = temp
    j += 1

    while j <= 6 and ((board.get_cell(i, j) == 0) or (board.get_cell(i, j) == c)):
        empty += 1
        j += 1

    if empty >= k:
        return 1

    return 0


random_player = lambda board: rand_select(board)
basic_player = lambda board: minimax(board, depth=4, eval_fn=basic_evaluate)
new_player = lambda board: minimax(board, depth=4, eval_fn=new_evaluate)
progressive_deepening_player = lambda board: run_search_function(board, search_fn=minimax, eval_fn=basic_evaluate)
