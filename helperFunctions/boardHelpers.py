from .action_helpers import *
from .tupleOperators import *
from .utils import *
from referee.game import HexDir

# Helper for updating board state 

def updateBoardSpawn(cell, color, board, spawner, currTotalPower):
    """
    Updates board state based on spawn
    """
    k = 1
    board[cell] = (color, k)
    spawner[cell] = k
    currTotalPower += 1

    return currTotalPower

def updateBoardSpread(cell, direction, color, board, attacker, victim, currTotalPower):
    """
    Updates board state based on spread
    """

    # Get power
    k = board[cell][1]

    # Spread while in range
    for i in range(1, k+1):
        newCell = check_bounds(addTuples(cell, multiplyPower(direction, i)))
        # Spread if cell not empty, spawn otherwise
        if newCell in board.keys():
            prevColor = board[newCell][0]
            prevK = board[newCell][1]
            # Check if power of token == 6
            if prevK == MAX_POWER:
                # Check whose token
                if prevColor == color:
                    del attacker[newCell]
                else:
                    del victim[newCell]
                del board[newCell]
                currTotalPower -= 6
            else:
                attacker[newCell] = prevK+1
                board[newCell] = (color, prevK+1)
                # Update opponent's tokens if conquered
                if (prevColor != color):
                    del victim[newCell]
                currTotalPower += 1
        else:
            currTotalPower = updateBoardSpawn(newCell, color, board, attacker, currTotalPower)

    # Update
    del attacker[cell]
    del board[cell]
    currTotalPower -= k

    return currTotalPower


def isValidSpawnMove(board, x, y):
    """
    Check if valid spawn move
    """
    cell = (x,y)
    if cell not in board:
        return True
    return False

# def isValidSpreadMove(board, x, y, direction):
#     """
#     Check if valid spread move
#     """
#     cell = (x,y)
#     k = board[cell][1]

#     # Check if can empower own and/or conquer opponent
#     for i in range(1, k+1):
#         newCell = check_bounds(addTuples(cell, multiplyPower(direction, i)))
#         if newCell in board.keys():
#             return True
#     return False

def getRandoDir(randoDir):
    """
    Get direction based on random number
    """
    if randoDir == 0:
        return (0, 1)
    elif randoDir == 1:
        return (-1, 1)
    elif randoDir == 2:
        return (-1, 0)
    elif randoDir == 3:
        return (0, -1)
    elif randoDir == 4:
        return (1, -1)
    else:
        return (1, 0)
    
def directionTupleConverter(direction):
    """
    Convert direction to tuple
    """
    if direction == HexDir.DownRight: 
        return (0, 1)
    elif direction == HexDir.Down:      
        return (-1, 1)
    elif direction == HexDir.DownLeft:  
        return (-1, 0)
    elif direction == HexDir.UpLeft:    
        return (0, -1)
    elif direction == HexDir.Up:         
        return (1, -1)
    else:
        return (1, 0)