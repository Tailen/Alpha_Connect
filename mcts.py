import math
from copy import deepcopy
from simulateGame import simulatedGame
from utils import convertInput
from random import randint
import sys
# Use epsilon to prevent division by zero
epsilon = sys.float_info.epsilon
# A list that store depths of every treeNode created
depthList = []


class treeNode(object):
    '''
    Class for a node on the Monte Carlo Tree Search
    '''
    
    # Player is 0 for red or 1 for yellow (True or False)
    def __init__(self, board, player, c=math.sqrt(2), parent=None):
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
            slots = convertInput(board.slots) # Convert slots to -1, 0, 1 representation
            self.board = simulatedGame(
                slots, board.gameEnded, board.winner, board.redTurn)
            self.depth = 1
        else:
            self.board = board
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
        return (1.0*self.w/(self.n+epsilon)) + self.c*math.sqrt(math.log(N)/(self.n+epsilon))


# The same search tree is passed around each move, to save computation
class searchTree(object):
    
    def __init__(self, board):
        # Start player is always the other player
        self.rootNode = treeNode(board, player=not board.redTurn, c=math.sqrt(2), parent=None)
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
        global depthList
        childNodes = self.rootNode.children
        print(len(depthList), 'instances of treeNode created')
        print('Maximum depth is ', max(depthList))
        # Remove any node that leads to loss in next opponent's move
        for child in childNodes.values():
            if not child.board.gameEnded:
                moves = child.board.getValidMoves()
                for move in moves:
                    board = deepcopy(child.board)
                    board.placeMove(move)
                    if board.winner == child.player:
                        child.n = sys.maxsize
            # If move leads to win, play it
            if child.board.winner == self.rootNode.player:
                child.n = 0
        # Print n value for child node, the lower the better
        print([child.n for child in childNodes.values()])
        # Select the child of root node that has the least visits (the best for current player)
        return min(childNodes.items(), key=lambda i: i[1].n)[0]