'''Classes of players: Human, HumanGUI, MCTS, and AlphaConnect. Input game and output the move(0-6)'''
import threading


class humanPlayer:

    def __init__(self):
        self.name = 'Console'
    
    def getMove(self, game):
        moveStr = input('Please enter the column of your move: ')
        while not game.isValidMove(moveStr):
            moveStr = int(input('Please enter the column of your move: '))
        return int(moveStr)


class humanGUIPlayer:

    def __init__(self):
        self.name = 'Human'
        self.move = None

    def getMove(self, game):
        game.moveEvent.wait()
        game.moveEvent.clear()
        return self.move

    def GUIInput(self, move):
        self.move = move


class MCTSPlayer:

    def __init__(self):
        self.name = 'AI'

    def getMove(self, game):
        return


class AlphaConnectPlayer:

    def __init__(self):
        self.name = 'AI'

    def getMove(self, game):
        return