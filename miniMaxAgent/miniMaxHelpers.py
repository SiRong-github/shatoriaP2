# Helper functions

from referee.game import HexDir, PlayerColor
from helperFunctions.action_helpers import *
from helperFunctions.tupleOperators import *
from helperFunctions.utils import *
from helperFunctions.boardHelpers import *
import time

def getCellRatio(board, color: PlayerColor):
    """Return ratio of power of player cells to opponent cells, given a board dictionary"""

    # Each cell is in format ((position), (color, power))
    reds, blues = get_red_blue_cells(board)
    reds_total = 0
    for cell in reds:
        reds_total += get_power(cell[0], board)

    blues_total = 0
    for cell in blues:
        blues_total += get_power(cell[0], board)

    match color:
        case PlayerColor.RED:
            if (blues_total == 0):
                return 0
            else:
                return reds_total/blues_total
            
        case PlayerColor.BLUE:
            if (reds_total == 0):
                return 0
            else:
                return blues_total/reds_total

def getCountConqueredIfSpread(board, x, y, direction):
    """
    Check if valid spread move
    """
    cell = (x,y)
    k = board[cell][1]
    countConquered = 0

    # Check if can empower own and/or conquer opponent
    for i in range(1, k+1):
        newCell = check_bounds(addTuples(cell, multiplyPower(direction, i)))
        if newCell in board.keys():
            countConquered += 1
    return countConquered

def getOpponentRange(board, opponentToken):
    opponentRange = []
    k = board[opponentToken][1]
    # Check if ownToken is in range of opponent spread
    for dir in HexDir:
        direction = directionTupleConverter(dir)
        for i in range(1, k+1):
            newCell = check_bounds(addTuples(opponentToken, multiplyPower(direction, i)))
            opponentRange.append(newCell)
    return opponentRange

def isBesideOpponent(ownToken, opponentToken):

    for dir in HexDir:
        if addTuples(opponentToken, directionTupleConverter(dir)) == ownToken:
            return True
    return False