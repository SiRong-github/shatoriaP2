# COMP30024 Artificial Intelligence, Semester 1 2023
# Project Part B: Game Playing Agent

from referee.game import \
    PlayerColor, Action, SpawnAction, SpreadAction, HexPos
from queue import PriorityQueue
from .helperFunctions.action_helpers import *
from .helperFunctions.boardHelpers import *
from .helperFunctions.tupleOperators import *
from .helperFunctions.utils import *
from .miniMaxTreeHelpers import *
from time import time

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
        global turn
        global turns_left

        if (len(board) == 0 or len(board) == 1):
            turns_left = 171
        
        # Determine if opening move
        if (len(board) < 2) and self._color == PlayerColor.RED:
            return SpawnAction(HexPos(3, 3)) # easiest to visualise
        
        else:
            #RUN MINIMAX TREE OVER HERE
            startTime = time()

            # Store all nodes that have been explored
            all_states = dict()

            # To store nodes to be expanded in current depth
            curr_pq = PriorityQueue()

            # Initialize root node
            color = self._color
            root_node = initMiniMaxTree(board, color)
            all_states[1] = root_node
            maxColor = root_node["color"]
            curr_pq.put(((-inf, -inf), root_node["id"]))

            current_index = 1
            
            # Build minimax tree - build in time_remaining/turns_left seconds.
            while (time() - startTime) < (referee["time_remaining"]/turns_left):
                
                # To store next nodes to be expanded in next depth
                next_pq = PriorityQueue()
                
                while not curr_pq.empty():
                    current_node = all_states[curr_pq.get()[1]]
                    all_states[current_node["id"]]["has_children"] = True
                    child_nodes = generate_children(current_node, current_index)

                    for child_node in child_nodes:
                        all_states[child_node["id"]] = child_node
                        all_states[current_node["id"]]["children"].append(child_node["id"])
                        
                        # no need to expand nodes which are already a goal state
                        if not is_goal_board_in_general(child_node["board"]):
                            next_pq.put((negEval(child_node["board"], maxColor), child_node["id"]))

                    current_index += len(child_nodes)
                
                curr_pq = next_pq

            # clear old queues to save space
            curr_pq = PriorityQueue()
            next_pq = PriorityQueue()

            # propagate scores up nodes
            alpha_beta_propagation(all_states, 1, (-inf, -inf), (inf, inf), maxColor)

            # Return move in level 1 of the tree with MAXIMUM value
            depth1Nodes = {key: value for key, value in all_states.items() if value["depth"] == 1}

            maxID = 2
            maxScore = (0, 0) # cellratio, totalpower
            for id, node in depth1Nodes.items():
                if node["score"] > maxScore:
                    maxID = id
                    maxScore = node["score"]
            
            move = all_states[maxID]["most_recent_move"]

            cell = move[0][0]

            bestMove = (cell, move[1])

            # END OF MINIMAX CODE

            cell = HexPos(bestMove[0][0], bestMove[0][1])
            turns_left -= 1

            if bestMove[1] == (0, 0):
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
                    currTotalPower = updateBoardSpawn(tuple(cell), color, board, own, currTotalPower)
                else:
                    currTotalPower = updateBoardSpawn(tuple(cell), color, board, opponent, currTotalPower)
                pass
            case SpreadAction(cell, direction):
                #print(f"Testing: {color} SPREAD from {cell}, {direction}")
                if color == self._color:
                    currTotalPower = updateBoardSpread(tuple(cell), directionTupleConverter(direction), color, board, own, opponent, currTotalPower)
                else:
                    currTotalPower = updateBoardSpread(tuple(cell), directionTupleConverter(direction), color, board, opponent, own, currTotalPower)
                pass

# Testing

# python -m referee -t 90 miniMaxBFSAgent:MiniMaxBFSAgent agent:Agent

# python -m referee -t 180 -s 250 miniMaxAlphaBeta:MiniMaxAlphaBeta miniMaxBFSAgent:MiniMaxBFSAgent
# python -m referee -t 30 -s 250 agent:Agent agent:Agent

# python -m referee -t 180 -s 250 miniMaxBFSAgent:MiniMaxBFSAgent miniMaxAlphaBeta:MiniMaxAlphaBeta
# python -m referee -t 180 -s 250 agent:Agent greedySearchAgent:GreedyAgent
# python -m referee -t 180 miniMaxAlphaBeta:MiniMaxAlphaBeta miniMaxAlphaBeta:MiniMaxAlphaBeta

# python -m referee -t 180 miniMaxBFSAgent:MiniMaxBFSAgent greedySearchAgent:GreedyAgent
# python -m referee -t 180 miniMaxAlphaBeta:MiniMaxAlphaBeta greedySearchAgent:GreedyAgent
# python -m referee -t 180 greedySearchAgent:GreedyAgent miniMaxAlphaBeta:MiniMaxAlphaBeta 
# python -m referee -t 180 greedySearchAgent:GreedyAgent miniMaxBFSAgent:MiniMaxBFSAgent 

# Help
# python3 -m referee -h

