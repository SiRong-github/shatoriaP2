from helperFunctions.action_helpers import *
from referee.game import PlayerColor
from .miniMaxConstants import *

def heuristic(board, maxColor: PlayerColor):
    """Finds estimate of minimum number of moves to get from board state to goal state by finding optimal solution for relaxed Infexion board where red cells can ONLY jump to blue cells, multiple times in one move according to the power it has. Returns optimal number of moves to get to goal state."""

    curr_board = board.copy()

    # Play relaxed infexion with optimal moves until goal is reached.
    num_moves = 0
    while not is_goal_board(curr_board):
        curr_board = generate_board_child(curr_board, maxColor)
        num_moves += 1
    
    return num_moves

def generate_board_child(parent_board, maxColor: PlayerColor):
    """Generate most optimal successor of relaxed game's `parent_board`'s state. Returns child board configuration."""

    reds, blues = get_red_blue_cells(parent_board)

    match maxColor:
        case PlayerColor.RED:
            max_cells = reds
            min_cells = blues
            
        case PlayerColor.BLUE:
            max_cells = blues
            min_cells = reds

    # always spread max cells with highest power
    sorted_maxes = sorted(max_cells, key=lambda cell: cell[1][1])
    to_spread = sorted_maxes[0]

    # always infect min cells with highest powers first (other than 6, since spreading to a power of 6 cell will just remove it) since they'll result in high-power red cells, so we can get to shortest possible moves faster
    sorted_mins = sorted(min_cells, key=lambda cell: cell[1][1], reverse=True)
    
    sixes_idx = 0
    for blue_cell in sorted_mins:
        if get_power(blue_cell[0], parent_board) != MAX_COORDINATE:
            break
        sixes_idx += 1

    if sixes_idx != 0:
        power_sixes = sorted_mins[:sixes_idx]
        del sorted_mins[:sixes_idx]
        sorted_mins = sorted_mins + power_sixes

    # avoid trying to infect more than existing number of blue cells (power of red cell > num of blue cells left)
    power = get_power(to_spread[0], parent_board)
    if (power) > len(blues):
        power = len(blues)

    # blue cells to spread to (can only spread to 'power' number of blue cells)
    spread_targets = list()
    for blue_cell in sorted_mins:
        spread_targets.append(blue_cell[0])
        power -= 1

        if power == 0:
            break

    child_board = spread_relaxed(to_spread, spread_targets, parent_board)

    return child_board

def is_goal_board(board, maxColor: PlayerColor):
    "Returns whether or not a board has reached goal state"

    reds, blues = get_red_blue_cells(board)

    if maxColor == PlayerColor.RED:
        return len(blues) == 0
    else:
        return len(reds) == 0

def spread_relaxed(cell, destinations, board):
    """Spreads a cell to destination cells in 'relaxed infexion'. Returns resulting board"""

    copied_board = board.copy()
    cell_rq = cell[0]
    cell_color = cell[1][0]

    for destination_rq in destinations:

        # delete destination cell from board if its power is above 6
        if (get_power(destination_rq, copied_board) + 1 > MAX_COORDINATE):
            del copied_board[destination_rq]
        
        # add to power of existing cell and infect it to red
        else:
            copied_board[destination_rq] = (cell_color, get_power(destination_rq, copied_board) + 1)

    # remove parent cell from board
    del copied_board[(cell_rq[0], cell_rq[1])]

    return copied_board