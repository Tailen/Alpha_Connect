from random import randint
from players import humanPlayer


# For simpler reading x is red, o is yellow
class game(object):

    # Print msgs and errors if cout is True, players is a list of two player objects
    def __init__(self, players, cout=True, moveEvent=None):
        # (0,0) is top left corner
        self.slots = [['-' for i in range(6)] for i in range(7)]
        self.gameEnded = False
        self.winner = None # False(0) for red(x) won, True(1) for yellow(o) won, -1 for draw
        # Decide who plays first, 0 then first player(red) plays first
        self.redTurn = bool(randint(0, 1))
        self.cout = cout
        self.players = players
        self.moveEvent = moveEvent
        if self.redTurn and cout: print('Yellow(o) plays first\n')
        elif cout: print('Red(x) plays first\n')
        # True if the board is modified after GUI update
        self.modified = False
        self.lastMove = (None, None)

    def startGame(self):
        if self.cout: print(self)
        while not self.gameEnded:
            move = self.players[self.redTurn].getMove(self)
            self.placeMove(move)
            if self.cout: print('\n' + str(self))

    # Input a string value, return True if move is valid, and return False if invalid
    def isValidMove(self, xStr):
        try:
            x = int(xStr)
        except ValueError:
            if self.cout: print('Input not ingeter, please enter a integer between 0 and 6 inclusive')
            return False
        if x < 0 or x > 6:
            if self.cout: print('Invalid move, input must be between 0 and 6 inclusive')
            return False
        if self.slots[x][0] != '-':
            if self.cout: print('Invalid move, stack already full')
            return False
        return True

    # Return True if successfully played the move, input is assumed to be valid
    def placeMove(self, x):
        # Find y of the move at x
        y = 0
        while y < 6 and (self.slots[x][y] == '-'):
            y += 1
        y -= 1
        # Modify the board
        self.__changeBoard(x, y)
        self.redTurn = not self.redTurn # Change sides
        # Check the game status
        if self.checkPlayerWon('x'):
            self.gameEnded = True
            self.winner = 0
            if self.cout: print('Well Played! Red(x) player won!')
        elif self.checkPlayerWon('o'):
            self.gameEnded = True
            self.winner = 1
            if self.cout: print('Well Played! Yellow(o) player won!')
        elif self.checkDraw():
            self.gameEnded = True
            if self.cout: print('Well played! Draw!')
            
    def checkPlayerWon(self, color):
        # Check Horizontal
        for y in range(6):
            for x in range(0, 4):
                if self.slots[x][y]==color and self.slots[x+1][y]==color \
                and self.slots[x+2][y]==color and self.slots[x+3][y]==color:
                    return True
        # Check Vertical
        for x in range(7):
            for y in range(0, 3):
                if self.slots[x][y]==color and self.slots[x][y+1]==color \
                and self.slots[x][y+2]==color and self.slots[x][y+3]==color: 
                    return True
        # Check Diagonal
        for x in range(0,4):
            for y in range(3,6):
                if self.slots[x][y]==color and self.slots[x+1][y-1]==color \
                and self.slots[x+2][y-2]==color and self.slots[x+3][y-3]==color:
                    return True
                if self.slots[x][y-3]==color and self.slots[x+1][y-2]==color \
                and self.slots[x+2][y-1]==color and self.slots[x+3][y]==color:
                    return True

    # Place the move by editing slots list
    def __changeBoard(self, x, y):
        if self.redTurn:
            c = 'x'
        else:
            c = 'o'
        self.slots[x][y] = c
        self.modified = True
        self.lastMove = (x, y)

    def checkDraw(self):
        for x in range(7):
            # False if any slot on the top row is empty
            if self.slots[x][0] == '-':
                return False
        return True

    # withY=True returns moveList with (x, y) cords, withY=False returns a list of x
    def getValidMoves(self, withY=False):
        # moveList is a list of tuple's of (x, y)
        moveList = []
        for x in range(7):
            lowest_y = -1
            for y in range(6):
                if self.slots[x][y] == '-':
                    lowest_y += 1
            if lowest_y != -1:
                moveList.append((x, y))
        if withY:
            return moveList
        else:
            return [cord[0] for cord in moveList]

    # String representation of the board
    def __str__(self):
        s = ''
        for y in range(6):
            for x in range(7):
                s = s + self.slots[x][y] + ' '
            s = s[:-1] + '\n'
        return s


if __name__ == '__main__':
    player1 = humanPlayer()
    player2 = humanPlayer()
    myGame = game(players=(player1, player2))
    myGame.startGame()