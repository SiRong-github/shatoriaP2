# COMP30024 Artificial Intelligence, Semester 1 2023
# Project Part B: Game Playing Agent

from referee.game import \
    PlayerColor, Action, SpawnAction, SpreadAction, HexPos, HexDir

from helperFunctions.action_helpers import *
from helperFunctions.boardHelpers import *
from helperFunctions.tupleOperators import *
from helperFunctions.utils import *
import random

# This is the entry point for your game playing agent. Currently the agent
# simply spawns a token at the centre of the board if playing as RED, and
# spreads a token at the centre of the board if playing as BLUE. This is
# intended to serve as an example of how to use the referee API -- obviously
# this is not a valid strategy for actually playing the game!

board = dict()
own = dict()
opponent = dict()
currTotalPower = 0

class GreedyAgent:
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

        # Create a board to store all current tokens
        updatedBoard = dict() #colour: hexPos, hexDir
        ownTokens = dict() #hexPos: power
        opponentTokens = dict() #hexPos: power
        
        timeRemaining = referee["time_remaining"]
        spaceRemaining = referee["space_remaining"]
        spaceLimit = referee["space_limit"]
        randomCells = []

        # Determine if opening move
        if (sum(map(len, board.values())) < 2):
            x = random.randint(0,6)
            y = random.randint(0,6)
            match self._color:
                case PlayerColor.RED:
                    return SpawnAction(HexPos(x, y)) # easiest to visualise if at centre
                case PlayerColor.BLUE:
                    while(not isValidSpawnMove(board, x, y)):
                        while(randomCells and (x,y) in randomCells):
                            x = random.randint(0,6)
                            y = random.randint(0,6)
                    cell = (x,y)
                    randomCells.append(cell)
                    return SpawnAction(HexPos(x,y))
        else:
            randoAction = random.randint(0,1)
            
            # Randomly select action type
            if randoAction == 0 and currTotalPower <= MAX_TOTAL_POWER:
                x = random.randint(0,6)
                y = random.randint(0,6)
                while(not isValidSpawnMove(board, x, y)):
                    while(randomCells and (x,y) in randomCells):
                        x = random.randint(0,6)
                        y = random.randint(0,6)
                    cell = (x,y)
                    randomCells.append(cell)
                return SpawnAction(HexPos(x,y))
            else: 
                ownCopy = dict(own)
                randoIndex = random.randint(0,len(ownCopy))
                # Check if can spread
                while(ownCopy):
                    count = 0
                    for k in ownCopy.keys():
                        if count == randoIndex:
                            x = k[0]
                            y = k[1]
                            for dir in HexDir:
                                direction = directionTupleConverter(dir)
                                if (isValidSpreadMove(board, x, y, direction)):
                                    return SpreadAction(HexPos(x,y), dir)    
                            break
                        count += 1
                    ownCopy.pop(k)
                    randoIndex = random.randint(0,len(ownCopy))

                # Spawn if can't spread: no neighbouring tokens
                x = random.randint(0,6)
                y = random.randint(0,6)
                while(not isValidSpawnMove(board, x, y)):
                    while(randomCells and (x,y) in randomCells):
                        x = random.randint(0,6)
                        y = random.randint(0,6)
                    cell = (x,y)
                    randomCells.append(cell)
                return SpawnAction(HexPos(x,y))

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
# agent first: python3 -m referee agent greedySearchAgent:GreedyAgent
# GreedyAgent first: python3 -m referee greedySearchAgent:GreedyAgent agent
# referee["time_remaining"]
# referee["space_remaining"]
# referee["space_limit"]
# Help
# python3 -m referee -h