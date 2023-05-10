from .action_helpers import *
from .tupleOperators import *
from .utils import *
from referee.game import HexDir

# Helper for updating board state 

def updateBoardSpawn(cell, color, board):
    """
    Updates board state based on spawn
    """
    k = 1
    board[cell] = (color, k)
    return

def updateBoardSpread(cell, direction, color, board):
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
                del board[newCell]
            else:
                board[newCell] = (color, prevK+1)
        else:
            updateBoardSpawn(newCell, color, board)

    # Update
    del board[cell]

    return

def isValidSpawnMove(board, x, y):
    """
    Check if valid spawn move
    """
    cell = (x,y)
    if cell not in board:
        return True
    return False
    
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

def tupleDirectionConverter(tuple):
    """
    Convert direction to tuple
    """
    if tuple == (0, 1): 
        return HexDir.DownRight
    elif tuple == (-1,1):      
        return HexDir.Down
    elif tuple == (-1, 0):  
        return HexDir.DownLeft
    elif tuple == (0, -1):    
        return HexDir.UpLeft
    elif tuple == (1, -1):         
        return HexDir.Up
    else:
        return HexDir.UpRight