'''Class of players: Human, MCTS, and AlphaConnect. Input board and output the move(0-6)'''


class humanPlayer:

    def __init__(self):
        return
    
    def getMove(self, board):
        move = int(input('Please enter your move: '))
        while not board.validMove():
            move = int(input('Please enter a valid move (integer 0-6 inclusive): '))
        return move
    
    