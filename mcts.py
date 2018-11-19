from game import *
import numpy as np
from copy import deepcopy


# Class of Monte Carlo Tree Search
class MCTSPlayer(object):

    def __init__(self, c):
        # rootNode = treeNode(c=np.sqrt(2))
        return


# Class for a node on the Monte Carlo Tree Search
class treeNode(object):
    
    #  c is the exploration parameter, defaulted sqrt of 2
    def __init__(self, c, board, parent=None):
        self.isLeaf = True # Indicates if the tree node is a leaf node
        self.n = 0 # Number of simulations after this move
        self.w = 0 # Number of wins after this move
        if parent != None:
            self.N = parent.n # Number of simulations of parent node
        else:
            self.N = None
        self.board = deepcopy(board)
        self.parent = parent
        self.children = {}
        
    def select(self):
        child = self
        while not child.isLeaf:
            child = max(child.children.values(), lambda n: n.getUCT)
        return child

    # Polulate children and return a random child of current node
    def expand(self):
        for move in self.board.getValidMoves(withY=False):
            self.children[move] = treeNode(self.c, self.board, parent=self)
            # make the move in child nodes

    def simmulate(self):
        return

    # Update n and w of this node
    def update(self):
        return

    # Recursively calls update method of the parents of this node
    def backprop(self):
        return

    def getUCT(self):
        return (self.w/self.n) + self.c*np.sqrt(np.log(self.N)/self.n)


# The same search tree is passed around each move, to save computation
class searchTree(object):
    
    def __init__(self):
        self.rootNode = treeNode(c=np.sqrt(2), board, parent=None)
        self.currentNode = self.rootNode

    def iterate(self):
        # Select
        self.currentNode = self.currentNode.select()
        # Expand
        if self.currentNode.n != 0:
            self.currentNode = self.currentNode.expand()