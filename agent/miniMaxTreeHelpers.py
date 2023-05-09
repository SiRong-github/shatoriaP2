from queue import Queue
from .action_helpers import *
from .miniMaxConstants import *
from .miniMaxHelpers import *
from referee.game import PlayerColor
import time
import logging

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

    root_node["score"] = (-1, -1)

    return root_node

def miniMaxTree(board, color: PlayerColor, turns_left, time_remaining):
    """Constructs miniMaxTree to find best possible move, given amount of time left. Throughout the game, the opponent will be MAX and the player will be MIN. Aim to minimize "score". Returns best node from depth '1'."""

    startTime = time.time()

    # Store all nodes that have been explored
    all_states = dict()

    # To store nodes to be expanded, in ascending order of f(n)
    q = Queue()

    # Initialize root node
    root_node = initMiniMaxTree(board, color)
    all_states[1] = root_node
    maxColor = root_node["color"]
    # print("MaxColor", maxColor)

    # Negative because we want to expand nodes with highest scores first, since we are playing as MAX
    
    #TODO: COMPARE CALCULATION SCORE EVERYTIME + PRUNING NODES VS CALCULATING CHILD NODES AT THE END ONLY WITHOUT PRUNING NODES

    q.put(root_node)
    current_node = all_states[q.get()["id"]]

    # Continue generating children until goal time is reached
    # alpha beta pruning (later) - focus on expanding board states which can take over a lot of cells

    current_index = 1
    logging.critical(f"Time left: {(time_remaining/turns_left)}")
    while (time.time() - startTime) < (time_remaining/(2 * turns_left)):
        all_states[current_node["id"]]["has_children"] = True
        child_nodes = generate_children(current_node, current_index, all_states, maxColor)
        
        for child_node in child_nodes:
            all_states[child_node["id"]] = child_node
            all_states[current_node["id"]]["children"].append(child_node["id"])
            
            # no need to expand nodes with a cell ratio of 0 or 49
            if (current_node["score"][0] != 49 and current_node["score"][0] != 0):
                q.put(child_node)
        
        # print(color, [node["score"] for node in child_nodes])

        current_node = all_states[q.get()["id"]]
        curr_id = current_node["id"]
        current_index += len(child_nodes)

        logging.error(f"{curr_id}")

    # propagate scores up nodes
    testTime = time.time()
    alpha_beta_propagation(all_states, root_node, (float('-inf'), float('-inf')), (float('inf'), float('inf')))
    logging.critical(time.time() - testTime)

    # Return move in level 1 of the tree with MAXIMUM value
    depth1Nodes = {key: value for key, value in all_states.items() if value["depth"] == 1}
    # print(depth1Nodes)
    logging.info(depth1Nodes)

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
    logging.warning(all_states[maxID]["score"])
    
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

def create_node(parent_node, new_board, new_move, current_index, maxColor):
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
    
    new_node["score"] = (getCellRatio(new_node["board"], maxColor), getTotalPower(new_node["board"], maxColor))

    return new_node

def propagateScore(node, all_states):
    "Propagates the score of a new `node` up tree if needed."

    current_node = node

    logging.debug(f"current node:{current_node}")
    while (current_node["parent_id"] != None):
        cur = all_states[node["parent_id"]]
        logging.debug(f"PARENT: {cur}")
        if (current_node["type"] == MAX and current_node["score"] < all_states[node["parent_id"]]["score"]):
            # Parent MINI would want to pick lower scored move
            all_states[node["parent_id"]]["score"] = current_node["score"]
            logging.debug("PARENT MINI UPDATED")
            cur = all_states[node["parent_id"]]
            logging.debug(f"After change: {cur}")

        elif (current_node["type"] == MINI and current_node["score"] > all_states[node["parent_id"]]["score"]):
            # Parent MAX would want to pick higher scored move
            all_states[node["parent_id"]]["score"] = current_node["score"]
            logging.debug("PARENT MAX UPDATED")
            cur = all_states[node["parent_id"]]
            logging.debug(f"After change: {cur}")

        # no changes made
        else:
            logging.debug("no more change")
            break
        
        current_node = all_states[node["parent_id"]]
    
    return

def alpha_beta_propagation(all_states, node, alpha, beta):

    if not node["has_children"]: # return node score if node has no children
       all_states[node["id"]]["score"] = node["score"]
       return node["score"]
    
    if node["type"] == MAX:
        score = (float('-inf'), float('-inf'))
        for child_id in node["children"]:
            child = all_states[child_id]
            score = max(score, alpha_beta_propagation(all_states, child, alpha, beta))
            alpha = max(alpha, score)
            
            if alpha >= beta:
                break
        all_states[node["id"]]["score"] = score
        return score
    
    else:
        score = (float('inf'), float('inf'))
        for child_id in node["children"]:
            child = all_states[child_id]
            score = min(score, alpha_beta_propagation(all_states, child, alpha, beta))
            beta = min(beta, score)
            if beta <= alpha:
                break
        
        all_states[node["id"]]["score"] = score
        return score