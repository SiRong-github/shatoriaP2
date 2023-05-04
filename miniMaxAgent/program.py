# COMP30024 Artificial Intelligence, Semester 1 2023
# Project Part B: Game Playing Agent

from referee.game import \
    PlayerColor, Action, SpawnAction, SpreadAction, HexPos, HexDir

from helperFunctions.action_helpers import *
from helperFunctions.boardHelpers import *
from helperFunctions.tupleOperators import *
from helperFunctions.utils import *
from .miniMaxTreeHelpers import *

# This is the entry point for your game playing agent. Currently the agent
# simply spawns a token at the centre of the board if playing as RED, and
# spreads a token at the centre of the board if playing as BLUE. This is
# intended to serve as an example of how to use the referee API -- obviously
# this is not a valid strategy for actually playing the game!

board = dict() # (x, y) : (colour, power)
own = dict() # (x, y) : power
opponent = dict()
currTotalPower = 0

class MiniMaxAgent:
    def __init__(self, color: PlayerColor, **referee: dict):
        """
        Initialise the agent.
        """
        
        self._color = color
        match color:
            case PlayerColor.RED:
                print("Testing: I am playing as red")
            case PlayerColor.BLUE:
                print("Testing: I am playing as blue")

    def action(self, **referee: dict) -> Action:
        """
        Return the next action to take.
        """
        global currTotalPower
        print(getCellRatio(board, self._color))
        print(PlayerColor)

        # Determine if opening move
        if (len(board) < 2) and self._color == PlayerColor.RED:
            return SpawnAction(HexPos(3, 3)) # easiest to visualise
        
        else:
            move = miniMaxTree(board, self._color)
            if move[1] == (0, 0):
                return SpawnAction(HexPos(move[0]))
            else:
                return SpreadAction(move[0], move[1])

    def turn(self, color: PlayerColor, action: Action, **referee: dict):
        """
        Update the agent with the last player's action.
        """
        global currTotalPower

        match action:
            case SpawnAction(cell):
                print(f"Testing: {color} SPAWN at {cell}")
                if color == self._color:
                    currTotalPower = updateBoardSpawn(tuple(cell), color, board, own, currTotalPower)
                else:
                    currTotalPower = updateBoardSpawn(tuple(cell), color, board, opponent, currTotalPower)
                pass
            case SpreadAction(cell, direction):
                print(f"Testing: {color} SPREAD from {cell}, {direction}")
                if color == self._color:
                    currTotalPower = updateBoardSpread(tuple(cell), directionTupleConverter(direction), color, board, own, opponent, currTotalPower)
                else:
                    currTotalPower = updateBoardSpread(tuple(cell), directionTupleConverter(direction), color, board, opponent, own, currTotalPower)
                pass

# Testing
# agent first: python -m referee -t 180 agent miniMaxAgent:MiniMaxAgent
# miniMax first: python -m referee miniMaxAgent:MiniMaxAgent greedySearchAgent:GreedyAgent
# Help
# python3 -m referee -h