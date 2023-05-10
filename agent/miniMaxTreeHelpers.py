from queue import PriorityQueue
from .action_helpers import *
from .miniMaxConstants import *
from .miniMaxHelpers import *
from referee.game import PlayerColor
import time
from math import inf

def initMiniMaxTree(board, color: PlayerColor):
    """Initializes miniMaxTree based on board state. Returns root node."""
    
    root_node = {"id": 1,
                "board": board,
                "parent_id": None,
                "score": None,
                "depth": 0,
                "has_children": True,
                "children": list(),
                "most_recent_move": None,
                "type": MAX,
                "color": color
    }

    return root_node

def miniMaxTree(board, color: PlayerColor, turns_left, time_remaining):
    """Constructs miniMaxTree to find best possible move, given amount of time left. Throughout the game, the opponent will be MAX and the player will be MIN. Aim to minimize "score". Returns best node from depth '1'."""

    startTime = time.time()

    # Store all nodes that have been explored
    all_states = dict()

    # To store nodes to be expanded in current depth
    curr_pq = PriorityQueue()

    # Initialize root node
    root_node = initMiniMaxTree(board, color)
    all_states[1] = root_node
    maxColor = root_node["color"]
    curr_pq.put(((-inf, -inf), root_node["id"]))

    current_index = 1

    # logging.critical(f"Time left: {(time_remaining/turns_left)}")
    # order of expansion - put in PQ

    # Build minimax tree - build in time_remaining/turns_left seconds.
    while (time.time() - startTime) < (time_remaining/turns_left):
        # To store next nodes to be expanded in next depth
        next_pq = PriorityQueue()
        
        while not curr_pq.empty():
            current_node = all_states[curr_pq.get()[1]]
            all_states[current_node["id"]]["has_children"] = True
            child_nodes = generate_children(current_node, current_index, all_states, maxColor)
            # need to do a curr depth thingy

            for child_node in child_nodes:
                all_states[child_node["id"]] = child_node
                all_states[current_node["id"]]["children"].append(child_node["id"])
                
                # no need to expand nodes which are already a goal state
                if not is_goal_board_in_general(child_node["board"]):
                    next_pq.put((negEval(child_node["board"], maxColor), child_node["id"]))

            current_index += len(child_nodes)
        
        curr_pq = next_pq
    
    # Empty the priority
    while not curr_pq.empty():
        curr_pq.get()
    while not next_pq.empty():
        next_pq.get()

    # propagate scores up nodes
    testTime = time.time()
    alpha_beta_propagation(all_states, 1, (-inf, -inf), (inf, inf), maxColor)
    #logging.critical(time.time() - testTime)

    # Return move in level 1 of the tree with MAXIMUM value
    depth1Nodes = {key: value for key, value in all_states.items() if value["depth"] == 1}

    maxID = 2
    maxScore = (0, 0) # cellratio, totalpower
    for id, node in depth1Nodes.items():
        if node["score"] > maxScore:
            maxID = id
            maxScore = node["score"]
    
    #print(maxID)
    move = all_states[maxID]["most_recent_move"]
    #print("move", move)

    cell = move[0][0]

    bestMove = (cell, move[1])
    
    #print("BESTMOVE", bestMove)

    return bestMove

def generate_children(parent_node, current_index, all_states, maxColor):
    """Generate all possible children of a parent node. Returns child nodes"""

    parent_board = parent_node["board"]
    parent_color = parent_node["color"]
    reds, blues = get_red_blue_cells(parent_node["board"])

    # get 
    if parent_color == PlayerColor.RED:
        child_cells = reds
    else:
        child_cells = blues

    child_nodes = list()
    
    # for each cell of current player of node, spread cell in all the possible directions
    possibleSpreads = getSpreadMoves(child_cells, parent_board)
    for spread_move in possibleSpreads:
        current_index += 1
        #print("spreadmove", spread_move)
        child_board = spread(spread_move[0], spread_move[1], parent_board)
        child_node = create_node(parent_node, child_board, (spread_move[0], spread_move[1]), current_index)
        child_nodes.append(child_node)

    # spawn cell in all possible empty spaces IF board power is not 49
    if getBoardPower(parent_board) < 49:
        for spawn_move in getSpawnMoves(parent_board, parent_color):
            current_index += 1
            child_board = spawn(spawn_move, parent_board)
            #print("child_board", child_board)
            child_node = create_node(parent_node, child_board, (spawn_move, (0, 0)), current_index)
                
            child_nodes.append(child_node)
        
    return child_nodes

def create_node(parent_node, new_board, new_move, current_index):
    """Creates new "node" structure, given a new board"""

    new_node = {"id": current_index,
                "board": new_board,
                "parent_id": parent_node["id"],
                "score": None,
                "depth": parent_node["depth"] + 1,
                "has_children": False,
                "children": list(),
                "most_recent_move": new_move,
                "type": None,
                "color": getOppositeColor(parent_node["color"])
    }

    if parent_node["type"] == MAX:
        new_node["type"] = MINI
    else:
        new_node["type"] = MAX

    return new_node

def alpha_beta_propagation(all_states, node_id, alpha, beta, maxColor):
    if not all_states[node_id]["has_children"]: # return node score if node has no children
       all_states[node_id]["score"] = eval(all_states[node_id]["board"], maxColor)
       return all_states[node_id]["score"]
    
    if all_states[node_id]["type"] == MAX:
        score = (-inf, -inf)
        for child_id in all_states[node_id]["children"]:
            score = max(score, alpha_beta_propagation(all_states, child_id, alpha, beta, maxColor))
            alpha = max(alpha, score)
            
            if alpha >= beta:
                break
    
    else:
        score = (inf, inf)
        for child_id in all_states[node_id]["children"]:
            score = min(score, alpha_beta_propagation(all_states, child_id, alpha, beta, maxColor))
            beta = min(beta, score)

            if beta <= alpha:
                break
        
    all_states[node_id]["score"] = score
    return score