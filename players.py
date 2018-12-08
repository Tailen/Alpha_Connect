'''Classes of players: Human, HumanGUI, MCTS, and AlphaConnect. Input game and output the move(0-6)'''

import mcts
import mcts_AlphaGo
from model import policyValueNet


class humanPlayer(object):

    def __init__(self):
        self.name = 'Console'
    
    def getMove(self, game):
        moveStr = input('Please enter the column of your move: ')
        while not game.isValidMove(moveStr):
            moveStr = int(input('Please enter the column of your move: '))
        return int(moveStr)


class humanGUIPlayer(object):

    def __init__(self, moveEvent):
        self.name = 'Human'
        self.moveEvent = moveEvent
        self.move = None

    def getMove(self, game):
        self.moveEvent.wait()
        self.moveEvent.clear()
        return self.move

    def GUIInput(self, move):
        # Wait 1 second to prevent unintentional moves
        self.move = move


class MCTSPlayer(object):

    def __init__(self):
        self.name = 'AI'

    def getMove(self, game):
        tree = mcts.searchTree(game)
        for _ in range(6000):
            tree.iterate()
        return tree.getMove()


class AlphaConnectPlayer(object):

    def __init__(self, weights_path=None):
        self.name = 'AI'
        if weights_path != None:
            self.network = policyValueNet(weights_path)
        else:
            self.network = policyValueNet()

    def getMove(self, game):
        tree = mcts_AlphaGo.searchTree(game, self.network)
        for _ in range(512):
            tree.iterate()
        return tree.getMove()