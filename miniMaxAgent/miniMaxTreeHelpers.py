from queue import PriorityQueue
from helperFunctions.action_helpers import *
from .miniMaxConstants import *
from .miniMaxHelpers import *
from referee.game import PlayerColor
import time

def  initMiniMaxTree(board, color: PlayerColor):
    """Initializes miniMaxTree based on board state. Returns root node."""
    
    root_node = {"id": 1,
                "board": board,
                "parent_id": None,
                "score": None,
                "depth": 0,
                "most_recent_move": None,
                "children": None,
                "type": MAX,
                "color": color
    }

    root_node["score"] = 0

    return root_node

def miniMaxTree(board, color: PlayerColor):
    """Constructs miniMaxTree to find best possible move, given amount of time left. Throughout the game, the opponent will be MAX and the player will be MIN. Aim to minimize "score". Returns best node from depth '1'."""

    startTime = time.time()

    # Store all nodes that have been explored
    all_states = dict()

    # To store nodes to be expanded, in ascending order of f(n)
    pq = PriorityQueue()

    # Initialize root node
    total_index = 1
    root_node = initMiniMaxTree(board, color)
    all_states[1] = root_node
    maxColor = root_node["color"]

    # Negative because we want to expand nodes with highest scores first, since we are playing as MAX
    pq.put((root_node["score"], root_node["id"]))
    current_node = all_states[pq.get()[1]]

    # Continue generating children until goal time is reached
    # alpha beta pruning (later) - focus on expanding board states which can take over a lot of cells
    
    while (time.time() - startTime) < 0.5:
        child_nodes = generate_children(current_node, total_index, all_states, maxColor)

        for child_node in child_nodes:
            all_states[child_node["id"]] = child_node
            #print("child score", child_node["score"])
            pq.put((-child_node["score"], child_node["id"]))
                
            total_index += 1

            current_node = all_states[pq.get()[1]]

    # Return move in level 1 of the tree with MAXIMUM value
    depth1Nodes = {key: value for key, value in all_states.items() if value["depth"] == 1}
    #print(depth1Nodes)

    maxID = 2
    maxScore = 0
    for id, node in depth1Nodes.items():
        if node["score"] > maxScore:
            #print("id", id)
            maxID = id
            maxScore = node["score"]
    
    #print(maxID)
    move = all_states[maxID]["most_recent_move"]
    #print("move", move)
    # print(all_states)
    cell = move[0][0]

    bestMove = (cell, move[1])
    
    #print("BESTMOVE", bestMove)

    return bestMove

def generate_children(parent_node, total_index, all_states, maxColor):
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
    possibleSpreads = getSpreadMoves(child_cells)
    for spread_move in possibleSpreads:
        #print("spreadmove", spread_move)
        child_board = spread(spread_move[0], spread_move[1], parent_board)
        child_node = create_node(parent_node, child_board, (spread_move[0], spread_move[1]), total_index, all_states, maxColor)
        
        child_nodes.append(child_node)
        total_index += 1

    # spawn cell in all possible empty spaces IF board power is not 49
    if getBoardPower(parent_board) < 49:
        for spawn_move in getSpawnMoves(parent_board, parent_color):
            child_board = spawn(spawn_move, parent_board)
            #print("child_board", child_board)
            child_node = create_node(parent_node, child_board, (spawn_move, (0, 0)), total_index, all_states, maxColor)
                
            child_nodes.append(child_node)
            total_index += 1
        
    return child_nodes

def create_node(parent_node, new_board, new_move, total_index, all_states, maxColor):
    """Creates new "node" structure, given a new board"""

    new_node = {"id": total_index + 1,
                "board": new_board,
                "parent_id": parent_node["id"],
                "score": None,
                "depth": parent_node["depth"] + 1,
                "most_recent_move": new_move,
                "children": None,
                "type": None,
                "color": None
    }

    if parent_node["type"] == MAX:
        new_node["type"] = MINI
    else:
        new_node["type"] = MAX

    new_node["color"] = getOppositeColor(parent_node["color"])

    new_node["score"] = getCellRatio(new_board, maxColor)
    propagateScore(new_node, all_states)

    return new_node

def propagateScore(node, all_states):
    "Propagates the score of a new `node` up tree if needed."

    current_node = node

    while (current_node["parent_id"] != None):
        if (current_node["type"] == MAX and current_node["score"] < all_states[node["parent_id"]]["score"]):
            # Parent MINI would want to pick lower scored move
            all_states[node["parent_id"]]["score"] = current_node["score"]

        elif (current_node["type"] == MINI and current_node["score"] > all_states[node["parent_id"]]["score"]):
            # Parent MAX would want to pick higher scored move
            all_states[node["parent_id"]]["score"] = current_node["score"]

        # no changes made
        else:
            break

        current_node = all_states[node["parent_id"]]
    
    return