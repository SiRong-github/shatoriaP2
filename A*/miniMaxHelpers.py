# Helper functions

from referee.game import HexDir, PlayerColor
from .helperFunctions.action_helpers import *
from .helperFunctions.tupleOperators import *
from .helperFunctions.utils import *
from .helperFunctions.boardHelpers import *

def getBoardPower(board):
    totalPower = 0
    for vals in board.values():
        totalPower += vals[1]
    return totalPower

def getOppositeColor(color: PlayerColor):
    if color == PlayerColor.RED:
        return PlayerColor.BLUE
    else:
        return PlayerColor.RED

def getCellRatio(board, maxColor: PlayerColor):
    """Return ratio of power of player cells to opponent cells, relative to MAX"""

    # Each cell is in format ((position), (color, power))
    reds, blues = get_red_blue_cells(board)
    reds_total = 0
    for cell in reds.keys():
        reds_total += get_power(cell, board)

    blues_total = 0
    for cell in blues.keys():
        blues_total += get_power(cell, board)

    match maxColor:
        case PlayerColor.RED:
            if (blues_total == 0):
                return 49
            else:
                return reds_total/blues_total
            
        case PlayerColor.BLUE:
            if (reds_total == 0):
                return 49
            else:
                return blues_total/reds_total
            
def getTotalPower(board, maxColor: PlayerColor):
    """Return ratio of power of player cells to opponent cells, relative to MAX"""

    # Each cell is in format ((position), (color, power))
    reds, blues = get_red_blue_cells(board)

    match maxColor:
        case PlayerColor.RED:
            cells = reds
            
        case PlayerColor.BLUE:
            cells = blues
    
    sum = 0
    for cell in cells:
        sum += get_power(cell, board)
        
    return sum

def eval(board, maxColor: PlayerColor):
    """Return eval score of a board"""

    return (getCellRatio(board, maxColor), getTotalPower(board, maxColor))

def negEval(board, maxColor: PlayerColor):
    """Return negative eval score of a board for priority queue"""

    return (-getCellRatio(board, maxColor), -getTotalPower(board, maxColor))

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

def getSpreadMoves(own, board):
    """Return all possible spread moves on board."""

    possibleMoves = []

    # Search for possible spread moves
    for cell in own.keys():
        x = cell[0]
        y = cell[1]

        for dir in HexDir:
            tupleDir = directionTupleConverter(dir)

             # Don't bother trying if cell has power 1 and will take over nothing
            if get_power(cell, board) == 1 and getCountConqueredIfSpread(board, x, y, tupleDir) == 0:
                continue
            
            else:
                possibleMoves.append(((cell, own[cell]), tupleDir))

    return possibleMoves

def getSpawnMoves(board, color):
    """Return all possible spawn moves on board."""

    doableMoves = []

    # Get spawn moves which are not in opponent range
    for i in range(0, 7):
        for j in range(0, 7):
            if (i, j) not in board:
                doableMoves.append(((i, j), (color, 1)))
    
    return doableMoves