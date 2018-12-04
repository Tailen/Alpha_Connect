import numpy as np
from copy import deepcopy
from random import randint
from simulateGame import simulatedGame
# Use epsilon to prevent division by zero
epsilon = np.finfo(float).eps
# A list that store depths of every treeNode created
depthList = []


# Class for a node on the Monte Carlo Tree Search
class treeNode(object):

    c_puct = 5 # UCT score parameter
    
    # Player is 0 for red or 1 for yellow (True or False)
    def __init__(self, board, player, c=np.sqrt(2), parent=None):
        self.isLeaf = True # Indicates if the tree node is a leaf node
        self.n = 0 # Number of simulations after this move
        self.w = 0 # Number of wins after this move
        self.c = c # Exploration parameter, defaulted sqrt of 2
        self.player = player
        self.parent = parent
        self.children = {}
        # Record the node depths
        if parent == None:
            # Create simulateGame game instance if is rootNode
            self.board = simulatedGame(
                board.slots, board.gameEnded, board.winner, board.redTurn)
            self.depth = 1
        else:
            self.board = deepcopy(board)
            self.depth = parent.depth + 1
        global depthList
        depthList.append(self.depth)
        
    def select(self):
        child = self
        while not child.isLeaf:
            child = max(child.children.items(), key=lambda i: i[1].getUCT())[1]
        return child

    # Polulate children and return a random child of current node
    def expand(self):
        moves = self.board.getValidMoves()
        for move in moves:
            # Deepcopy board into all child, player is switched
            self.children[move] = treeNode(deepcopy(self.board), not self.player, self.c, parent=self)
            # make the move in child nodes
            self.children[move].board.placeMove(move)
        # Set isLeaf to False since children is not empty
        self.isLeaf = False
        # Return a random child
        return self.children[moves[randint(0, len(moves)-1)]]

    # Play out random moves until game ends, return the winner
    def simmulate(self):
        # Make a deepcopy of current board
        board = deepcopy(self.board)
        while not board.gameEnded:
            moves = board.getValidMoves()
            board.placeMove(moves[randint(0, len(moves)-1)])
        return board.winner

    # Update n and w of this node
    def update(self, winner):
        if winner == self.player:
            self.w += 1
        self.n += 1

    # Recursively calls update method of the parents of this node
    def backprop(self, winner):
        self.update(winner)
        if self.parent != None:
            self.parent.backprop(winner)

    # Calculate score of UCT(UCB1 for Trees) formula
    def getUCT(self):
        global epsilon
        # Get number of simulations of parent node
        N = self.parent.n
        return (1.0*self.w/(self.n+epsilon)) + self.c*np.sqrt(np.log(N)/(self.n+epsilon))


# The same search tree is passed around each move, to save computation
class searchTree(object):
    
    def __init__(self, board, network):
        # Start player is always the other player
        self.rootNode = treeNode(board, player=not board.redTurn, c=np.sqrt(2), parent=None)
        self.currentNode = self.rootNode

    def iterate(self):
        # Select
        self.currentNode = self.currentNode.select()
        # Expand
        if self.currentNode.n == 0:
            self.currentNode = self.currentNode.expand()
        # Simulate
        winner = self.currentNode.simmulate()
        # Backprop
        self.currentNode.backprop(winner)
        # Reset currentNode to rootNode
        self.currentNode = self.rootNode
    
    def getMove(self):
        global epsilon, depthList
        childNodes = self.rootNode.children
        print(len(depthList), 'instances of treeNode created')
        print('Maximum depth is ', max(depthList))
        # Select the child of root node that has the highest winrate
        return min(childNodes.items(), key=lambda i: 1.0*i[1].w/(i[1].n+epsilon))[0]