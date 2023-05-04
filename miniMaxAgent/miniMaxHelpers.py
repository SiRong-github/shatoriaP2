# Helper functions

from referee.game import HexDir, PlayerColor
from helperFunctions.action_helpers import *
from helperFunctions.tupleOperators import *
from helperFunctions.utils import *
from helperFunctions.boardHelpers import *

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
    print("Get cell ratio, blues total", blues_total)

    match maxColor:
        case PlayerColor.RED:
            if (blues_total == 0):
                print("1")
                return 0
            else:
                print("2")
                return reds_total/blues_total
            
        case PlayerColor.BLUE:
            if (reds_total == 0):
                print("3")
                return 0
            else:
                print("4")
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

def getSpreadMoves(own):
    """Return all possible spread moves on board."""

    possibleMoves = []

    # Search for possible spread moves
    for cell in own.keys():
        x = cell[0]
        y = cell[1]

        for dir in HexDir:
            possibleMoves.append(cell, directionTupleConverter(dir))

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

def getDefensiveSpawnMoves(board, opponent):
    """Return spawn moves which aren't in `opponent` range. Possible way of alpha beta pruning!"""

    impossibleMoves = []
    doableMoves = []

    # Search for cells in range of opponent
    for opponentToken in opponent.keys():
        impossibleMoves.append(getOpponentRange(board, opponentToken))

    # Get spawn moves which are not in opponent range
    for i in range(0, 7):
        for j in range(0, 7):
            if (i, j) not in impossibleMoves:
                doableMoves.append((i, j))
    
    return doableMoves

def getOpponentRange(board, opponentToken):
    """Returns cells which an opponent cell `opponentToken` can reach"""
     
    opponentRange = []
    k = board[opponentToken][1] # power of opponent cell

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