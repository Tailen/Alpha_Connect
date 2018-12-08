import numpy as np
from copy import deepcopy
from simulateGame import simulatedGame
from utils import convertInput
import numpy as np
# Use epsilon to prevent division by zero
epsilon = np.finfo(float).eps
# A list that store depths of every treeNode created
depthList = []


# Class for a node on the Monte Carlo Tree Search for AlphaGo Zero
class treeNode(object):

    c_puct = 5 # PUCT score parameter
    
    # Player is 0 for red or 1 for yellow (True or False)
    def __init__(self, board, player, policy_value=1, parent=None):
        self.isLeaf = True # Indicates if the tree node is a leaf node
        self.n = 0 # Number of simulations after this move
        self.p = policy_value # The initial policy variable return by NN
        self.v = None # The value variable return by NN
        self.Q = None # The Q score that indicates how good this node is
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
        
    # Recursively select the child node with the highest PUCT score
    def select(self):
        child = self
        while not child.isLeaf:
            child = max(child.children.items(), key=lambda i: i[1].getPUCT())[1]
        return child

    # Run policyValueNet on the selected node to evaluate v, and assign p to expanded nodes
    def evaluate(self, network):
        # Get NN output
        output = network.predict(self.board.slots)
        policy = output[0][0] # A list of policy probs
        self.v = output[1][0][0] # A single float
        # Filter invalid moves and renormalize policy
        valids, moves = np.array(self.board.getValidMoves(returnBinary=True))
        policy = policy*valids # Mask invalid moves
        policySum = np.sum(policy)
        if policySum > 0:
            policy = policy / policySum # Renormalize
        else:
            # If all valid moves are 0, make all valid moves equally probable
            print('All valid moves are 0, making all valid moves equally propable')
            policy = (policy + valids) / np.sum(valids)
        # Assign p to all child nodes
        for move in moves:
            # Deepcopy board into all child, player is switched
            self.children[move] = treeNode(deepcopy(self.board), not self.player, policy[move], parent=self)
            # Make the move in child nodes
            self.children[move].board.placeMove(move)
            # # Set the value v to 1 if the child node loses (Cannot lose on your move)
            # winner = self.children[move].board.winner
            # if winner == self.player: # Current node wins
            #     self.v = 1
            #     self.children[move].v = -1
            #     self.children[move].Q = -1
            #     self.children[move].isLeaf = False
        # Set isLeaf to False since children is not empty
        self.isLeaf = False
        # Return the value of current Node
        return self.v

    # Update n and Q values of this node
    def update(self, value):
        if self.Q == None:
            self.Q = self.v
        else:
            self.Q = (self.n*self.Q + value) / (self.n + 1)
        self.n += 1

    # Recursively calls update method of the parents of this node
    def backprop(self, value):
        self.update(value)
        if self.parent != None:
            self.parent.backprop(-value)

    # Calculate Q(s,a) + PUCT Score
    def getPUCT(self):
        # Get number of visits of parent node
        N = self.parent.n
        return self.parent.Q + self.c_puct*self.p*np.sqrt(N)/(1+self.n)


# The same search tree is passed around each move, to save computation
class searchTree(object):
    
    def __init__(self, board, network):
        # Start player is always the other player
        self.rootNode = treeNode(board, player=not board.redTurn, parent=None)
        self.currentNode = self.rootNode
        self.network = network

    def iterate(self):
        # Select
        self.currentNode = self.currentNode.select()
        # Evaluate and Expand
        value = self.currentNode.evaluate(self.network)
        # Backprop
        self.currentNode.backprop(value)
        # Reset currentNode to rootNode
        self.currentNode = self.rootNode
    
    def getMove(self):
        global epsilon, depthList
        childNodes = self.rootNode.children
        print(len(depthList), 'instances of treeNode created')
        print('Maximum depth is ', max(depthList))
        # Select the child of root node that has the highest visits
        return min(childNodes.items(), key=lambda i: i[1].n)[0]