from queue import Queue
from helperFunctions.action_helpers import *
from .miniMaxConstants import *
from .miniMaxHelpers import *
from referee.game import PlayerColor
import time
import logging

def  initMiniMaxTree(board, color: PlayerColor):
    """Initializes miniMaxTree based on board state. Returns root node."""
    
    root_node = {"id": 1,
                "board": board,
                "parent_id": None,
                "score": None,
                "depth": 0,
                "has_children": True,
                "most_recent_move": None,
                "type": MAX,
                "color": color
    }

    root_node["score"] = (-1, -1)

    return root_node

def generate_children(parent_node, current_index, all_states, maxColor):
    """Generate all possible children of a parent node. Returns child nodes"""

    parent_board = parent_node["board"]
    parent_color = parent_node["color"]
    reds, blues = get_red_blue_cells(parent_node["board"])

    # get 
    if parent_color == PlayerColor.RED:
        child_cells = reds
        opponent_cells = blues
    else:
        child_cells = blues
        opponent_cells = reds

    child_nodes = list()

    # spawn cell in all possible empty spaces IF board power is not 49
    if getBoardPower(parent_board) < 49:
        for spawn_move in getSpawnMoves(parent_board, parent_color):
            current_index += 1
            child_board = spawn(spawn_move, parent_board)
            #print("child_board", child_board)
            child_node = create_node(parent_node, child_board, (spawn_move, (0, 0)), current_index, all_states, maxColor)
                
            child_nodes.append(child_node)
    
    # for each cell of current player of node, spread cell in all the possible directions
    possibleSpreads = getSpreadMoves(child_cells, parent_board)
    for spread_move in possibleSpreads:
        current_index += 1
        #print("spreadmove", spread_move)
        child_board = spread(spread_move[0], spread_move[1], parent_board)
        child_node = create_node(parent_node, child_board, (spread_move[0], spread_move[1]), current_index, all_states, maxColor)
        
        child_nodes.append(child_node)

    # print(possibleSpreads)
        
    return child_nodes

def create_node(parent_node, new_board, new_move, current_index, all_states, maxColor):
    """Creates new "node" structure, given a new board"""

    new_node = {"id": current_index,
                "board": new_board,
                "parent_id": parent_node["id"],
                "score": None,
                "depth": parent_node["depth"] + 1,
                "has_children": False,
                "most_recent_move": new_move,
                "type": None,
                "color": getOppositeColor(parent_node["color"])
    }

    if parent_node["type"] == MAX:
        new_node["type"] = MINI
    else:
        new_node["type"] = MAX
    
    new_node["score"] = (getCellRatio(new_node["board"], maxColor), getTotalPower(new_node["board"], maxColor))

    return new_node

def propagateScore(node, all_states):
    "Propagates the score of a new `node` up tree if needed."

    current_node = node

    while (current_node["parent_id"] != None):
        cur = all_states[node["parent_id"]]
        if (current_node["type"] == MAX and current_node["score"] < all_states[node["parent_id"]]["score"]):
            # Parent MINI would want to pick lower scored move
            all_states[node["parent_id"]]["score"] = current_node["score"]
            cur = all_states[node["parent_id"]]

        elif (current_node["type"] == MINI and current_node["score"] > all_states[node["parent_id"]]["score"]):
            # Parent MAX would want to pick higher scored move
            all_states[node["parent_id"]]["score"] = current_node["score"]
            cur = all_states[node["parent_id"]]

        # no changes made
        else:
            break
        
        current_node = all_states[node["parent_id"]]
    
    return