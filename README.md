# University Subject
This is a COMP30024 Artificial Intelligence Project created by a two-person team.

# File Purpose
The program implements one of the players in a strategic, perfect-information two-player game of contagion and domination called Infexion.

# File-Level Documentation
Infexion consists of a 7x7 hexagonally-tiled, infinitely repeating board, described by an axial coordinate system in the program. A valid coordinate is an integer pair (r,q), 0 ≤ r ≤ 6, 0 ≤ q ≤ 6. The objective of the players (named Red and Blue) are to conquer all the 'tokens' on the board.

The game ends under three conditions:
    1. One player has successfully controlled all tokens on the board and is thus declared the winner. This can only be done through the SPREAD action. 
    2. If no one has won in 343 turns, the player with the greatest total POWER is the winner, given they lead this by at least a power of 2. Otherwise, the game ends in a draw.
    3. If there are no more tokens on the board, the game ends in a draw. This may occur due to the stack removal rule (i.e., a single token attacking a POWER 6 opponent token stack, with no other tokens remaining on the board).

In a turn, a player may choose to either:
    1. Spawn a new token in an empty cell, valid only when the power (number of tokens in a token stack) of all cells on the board is less than 49, or
    2. Spread one of their token stacks with the power k, which is defined by the cell's coordinate (r,q) and a hex direction (rd, qd), which is one of the hex neighbour offsets: (0,1), (-1,1), (-1,0), (0,-1), (1,-1), or (1,0). This action leads to the following changes to the board state:
        * All tokens in the chosen token stack are removed from the cell, leaving it empty.
        * The immediately-adjacent line of k cells in the chosen direction, (rd, qd), have one token placed on top of each, thus incrementing their POWER by one.
        * The moving player takes control of any opponent-controlled stacks where a token has been placed on top.

 In the case that a stack is incremented above POWER 6 (the maximum possible power), the stack is completely removed from the game, leaving the cell empty. This also consumes the SPREAD token that would have been placed on top.

# Provided Code by the Subject
    1. agent module (Template)
        a. __init__.py
            * This imports the Agent class in program.py.
        b. program.py
            * This contains the Agent class which consists of three methods:
                i. def __init__(self, color: PlayerColor, **referee: dict): This initialises the player by determining if it plays as Red or Blue.
                ii. def action(self, **referee: dict) -> Action: This selects and returns a new action at the beginning of the player's turn.
                iii. def turn(self, color: PlayerColor, action: Action, **referee: dict): This lets the referee program validate and apply the player's action to the game state.

    2. referee (Driver Program)
        * This plays two given agents against each other and enforce the game rules provided in the File-Level Documentation

# Our Agents
We created agents utilising different game-playing algorithms in our project. These are ranked according to the most effective.
    1. Alpha-Beta
    2. MiniMax
    3. MiniMax BFS
    4. Unpruned MiniMax BFS
    5. Greedy Search
    6. Random

## Commands
# Testing
To test two agents against each other (wherein both are located in two different folders) and 
    within the time limit of 180s and space limit of 250MB:
    python3 -m referee -t 180 -s 250 folderName1:agentName1 folderName2:agentName2

    Example:
        Given Agent1 class in module Mod1 and Agent2 class in module Mod2,
        python3 -m referee -t 180 -s 250 Mod1:Agent1 Mod2:Agent2

# Help
python3 -m referee -h
