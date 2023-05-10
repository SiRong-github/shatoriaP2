# COMP30024 Artificial Intelligence, Semester 1 2023
# Project Part B: Game Playing Agent

from referee.game import \
    PlayerColor, Action, SpawnAction, SpreadAction, HexPos

from .action_helpers import *
from .boardHelpers import *
from .tupleOperators import *
from .utils import *
from .miniMaxTreeHelpers import *

#logging.basicConfig(level=logging.WARNING, filename="logfile.txt", filemode="a+",
    #format="%(asctime)-15s %(levelname)-8s %(message)s")

# This is the entry point for your game playing agent. Currently the agent
# simply spawns a token at the centre of the board if playing as RED, and
# spreads a token at the centre of the board if playing as BLUE. This is
# intended to serve as an example of how to use the referee API -- obviously
# this is not a valid strategy for actually playing the game!

board = dict() # (x, y) : (colour, power)Z
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
        global turn
        global turns_left

        if (len(board) == 0):
            turn = 1
            turns_left = 171
        elif (len(board) == 1):
            turn = 0
            turns_left = 171

        # Determine if opening move
        if (len(board) < 2) and self._color == PlayerColor.RED:
            #logging.critical(f"{self._color}, TURN: {turn}")
            return SpawnAction(HexPos(3, 3)) # easiest to visualise
        
        else:
            turn += 2
            #logging.critical(f"{self._color}, TURN: {turn}")
            move = miniMaxTree(board, self._color, turns_left, referee["time_remaining"])
            cell = HexPos(move[0][0], move[0][1])
            turns_left -= 1

            if move[1] == (0, 0):
                return SpawnAction(cell)
            else:
                dir = tupleDirectionConverter(move[1])
                return SpreadAction(cell, dir)

    def turn(self, color: PlayerColor, action: Action, **referee: dict):
        """
        Update the agent with the last player's action.
        """
        global currTotalPower

        match action:
            case SpawnAction(cell):
                #print(f"Testing: {color} SPAWN at {cell}")
                if color == self._color:
                    currTotalPower = updateBoardSpawn(tuple(cell), color, board, currTotalPower)
                else:
                    currTotalPower = updateBoardSpawn(tuple(cell), color, board, currTotalPower)
                pass
            case SpreadAction(cell, direction):
                #print(f"Testing: {color} SPREAD from {cell}, {direction}")
                if color == self._color:
                    currTotalPower = updateBoardSpread(tuple(cell), directionTupleConverter(direction), color, board, currTotalPower)
                else:
                    currTotalPower = updateBoardSpread(tuple(cell), directionTupleConverter(direction), color, board, currTotalPower)
                pass

# Testing

# python3 -m referee -l -t 180 agent miniMaxBFSAgent:MiniMaxBFSAgent

# python -m referee -t 180 -s 250 miniMaxAlphaBeta:MiniMaxAlphaBeta miniMaxBFSAgent:MiniMaxBFSAgent
# python -m referee -t 180 miniMaxBFSAgent:MiniMaxBFSAgent miniMaxAlphaBeta:MiniMaxAlphaBeta
# python -m referee -t 180 miniMaxAlphaBeta:MiniMaxAlphaBeta greedySearchAgent:GreedyAgent

# python -m referee -t 180 miniMaxBFSAgent:MiniMaxBFSAgent greedySearchAgent:GreedyAgent
# python -m referee -t 180 miniMaxAlphaBeta:MiniMaxAlphaBeta greedySearchAgent:GreedyAgent
# python -m referee -t 180 greedySearchAgent:GreedyAgent miniMaxAlphaBeta:MiniMaxAlphaBeta 
# python -m referee -t 180 greedySearchAgent:GreedyAgent miniMaxBFSAgent:MiniMaxBFSAgent 

# Help
# python3 -m referee -h

