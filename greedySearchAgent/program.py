# COMP30024 Artificial Intelligence, Semester 1 2023
# Project Part B: Game Playing Agent

from referee.game import \
    PlayerColor, Action, SpawnAction, SpreadAction, HexPos, HexDir

from .action_helpers import *
from .boardHelpers import *
from .tupleOperators import *
from .utils import *
from .greedyHelpers import *

# This is the entry point for your game playing agent. Currently the agent
# simply spawns a token at the centre of the board if playing as RED, and
# spreads a token at the centre of the board if playing as BLUE. This is
# intended to serve as an example of how to use the referee API -- obviously
# this is not a valid strategy for actually playing the game!

board = dict() # (x, y) : (colour, power)
own = dict() # (x, y) : power
opponent = dict()
currTotalPower = 0

class Agent:
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

        # Determine if opening move
        if (len(board) < 2):
            match self._color:
                case PlayerColor.RED:
                    return SpawnAction(HexPos(3, 3)) # easiest to visualise
                case PlayerColor.BLUE:
                    # could be anywhere so long as one step away from board
                    # best if on hexdir in case opponent chooses to spread towards own
                    return SpawnAction(HexPos(5, 1)) #easiest to visualise
        else:
            # Spread if can conquer tokens
            possibleMoves, otherPossibleMoves = getBestGreedySpreadMove(board, own, self._color)
            if not possibleMoves and currTotalPower <= MAX_TOTAL_POWER:
                cell = getBestGreedySpawnMove(board, own, opponent)
                x = cell[0]
                y = cell[1]
                return SpawnAction(HexPos(x,y))
            else:

                # Get best possible moves
                if possibleMoves:
                    best = possibleMoves.pop(0)
                else:
                    best = otherPossibleMoves.pop(0)
                
                x = best[1][0]
                y = best[1][1]
                direction = best[2]
                return SpreadAction(HexPos(x, y), direction)

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
# agent first: python3 -m referee -t 180 agent greedySearchAgent:GreedyAgent
# GreedyAgent first: python3 -m referee -t 180 greedySearchAgent:GreedyAgent agent
# Help
# python3 -m referee -h