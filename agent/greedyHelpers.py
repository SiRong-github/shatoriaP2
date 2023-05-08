# Helper functions

from referee.game import HexDir
from helperFunctions.action_helpers import *
from helperFunctions.tupleOperators import *
from helperFunctions.utils import *
from helperFunctions.boardHelpers import *

def getCountConqueredIfSpread(board, x, y, direction, color):
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
            if board[newCell][0] != color:
                countConquered += 1
            else:
                countConquered += 0.01

    return countConquered

def getBestGreedySpreadMove(board, own, color):

    possibleMoves = []
    otherPossibleMoves = []

    # Search for possible spread moves
    for cell in own.keys():
        x = cell[0]
        y = cell[1]
        for dir in HexDir:
            numConquered = getCountConqueredIfSpread(board, x, y, directionTupleConverter(dir), color)
            if (type(numConquered) == int and numConquered != 0):
                possibleMoves.append((numConquered, cell, dir))
            else:
                otherPossibleMoves.append((numConquered, cell, dir))

    # Sort highest to lowest
    possibleMoves.sort(key=lambda x: x[0], reverse=True)
    otherPossibleMoves.sort(key=lambda x: x[0], reverse=True)

    return possibleMoves, otherPossibleMoves
    
def getBestGreedySpawnMove(board, own, opponent):

    impossibleMoves = []

    # Search for cells in range of opponent
    for opponentToken in opponent.keys():
        impossibleMoves.append(getOpponentRange(board, opponentToken))

    # Calculate cell closest to current cell
    for ownCell in own.keys():
        for dir in HexDir:
            newCell = check_bounds(addTuples(ownCell, directionTupleConverter(dir)))
            # Check if new cell is in range of opponent
            for opponentRange in impossibleMoves:
                if newCell == opponentRange:
                    break
            if (isValidSpawnMove(board, newCell[0], newCell[1])):
                return newCell

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