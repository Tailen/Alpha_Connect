from random import randint


# For simpler reading x is red, o is green
class board(object):

    def __init__(self, cOut=True):
        # (0,0) is top left corner
        self.slots = [['-' for i in range(6)] for i in range(7)]
        self.gameEnded = False
        self.winner = True # True(1) for red(x) won, False(0) for green(o) won, -1 for draw
        # Decides who plays first
        self.redTurn = bool(randint(0, 1))
        self.cOut = cOut
        if self.redTurn:
            if self.cOut: print('Red(x) plays first\n')
        else:
            if self.cOut: print('Green(o) plays first\n')

    def __str__(self):
        s = ''
        for y in range(6):
            for x in range(7):
                s = s + self.slots[x][y] + ' '
            s += '\n'
        return s

    # Return True if move is valid, and return False if invalid
    def validMove(self, x):
        msg = ''
        y = 0
        if x < 0 or x > 6:
            msg = 'Invalid move, not between 0 and 6 inclusive'
            if self.cOut: print(msg)
            return (False, msg)
        while y < 6 and (self.slots[x][y] == '-'):
            y += 1
        y -= 1
        if y == -1:
            msg = 'Invalid move, stack already full'
            if self.cOut: print(msg)
            return (False, y, msg)
        return (True, y, msg)

# Return current played color and position, (-1,-1) for invalid move, and a string msg
    def placeMove(self, x):
        msg = ''
        y = 0
        if not self.gameEnded:
            checkResult = self.validMove(x)
            if not checkResult[0]:
                msg = checkResult[2]
                return self.redTurn, -1, -1, msg
            else:
                y = checkResult[1]
                self.__changeBoard(x, y)
                self.redTurn = not self.redTurn # Change sides
        if self.checkPlayerWon('x'):
            self.gameEnded = True
            msg = 'Red(x) Player Won!'
            if self.cOut: print(msg)
        elif self.checkPlayerWon('o'):
            self.gameEnded = True
            self.winner = False
            msg = 'Green(o) Player Won!'
            if self.cOut: print(msg)
        elif self.__checkDraw():
            self.gameEnded = True
            self.winner = -1
            msg = 'Draw! Well played'
            if self.cOut: print(msg)
        # If successfully played the move, then the current colors changes
        return (not self.redTurn), x, y, msg
            
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

    # Render the board move by editing the slot list
    def __changeBoard(self, x, y):
        if self.redTurn:
            c = 'x'
        else:
            c = 'o'
        self.slots[x][y] = c

    def __checkDraw(self):
        for x in range(7):
            for y in range(6):
                if self.slots[x][y] == '-':
                    return False
        return True

    # withY returns moveList with (x, y) cords, withY=False returns a list of x
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


if __name__ == '__main__':
    gameBoard = board()
    print(gameBoard)
    while not gameBoard.gameEnded:
        if gameBoard.redTurn:
            print('Red(x) player\'s turn!')
        else:
            print('Green(o) player\'s turn!')
        try:
            move = int(input('Please enter the column of your move: '))
            gameBoard.placeMove(move)
        except ValueError: 
            print('Input not ingeter, please enter integer between 1 and 7')
        print()
        print(gameBoard)