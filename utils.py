# Convert input from a 7x6 2D List to the network input of (7, 6, 1) numpy array
# Red pieces are 1, yellow pieces are -1, and empty positions are 0
def convertInput(board, redTurn=True):
    converted = [[0 for i in range(6)] for i in range(7)]
    for x in range(len(board)):
        for y in range(len(board[0])):
            if board[x][y] == 'x':
                # The board is formated based on the perspective of current player
                if redTurn:
                    converted[x][y] = 1
                else:
                    converted[x][y] = -1
            elif board[x][y] == 'o':
                if redTurn:
                    converted[x][y] = -1
                else:
                    converted[x][y] = 1
            else:
                converted[x][y] = 0
    return converted

class dotdict(dict):
    def __getattr__(self, name):
        return self[name]