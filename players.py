'''Classes of players: Human, HumanGUI, MCTS, and AlphaConnect. Input game and output the move(0-6)'''

from mcts import searchTree

class humanPlayer:

    def __init__(self):
        self.name = 'Console'
    
    def getMove(self, game):
        moveStr = input('Please enter the column of your move: ')
        while not game.isValidMove(moveStr):
            moveStr = int(input('Please enter the column of your move: '))
        return int(moveStr)


class humanGUIPlayer:

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


class MCTSPlayer:

    def __init__(self):
        self.name = 'AI'

    def getMove(self, game):
        self.gameBoard = game
        tree = searchTree(self.gameBoard)
        for _ in range(3000):
            tree.iterate()
            # Reset currentNode to rootNode
            tree.currentNode = tree.rootNode
        return tree.getMove()


class AlphaConnectPlayer:

    def __init__(self):
        self.name = 'AI'

    def getMove(self, game):
        return