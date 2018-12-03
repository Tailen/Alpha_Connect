from random import randint


# For simpler reading x is red, o is yellow
class simulatedGame(object):

    # Players is a list of two player objects
    def __init__(self, slots, gameEnded, winner, redTurn):
        # (0,0) is top left corner
        self.slots = [['-' for i in range(6)] for i in range(7)]
        self.gameEnded = gameEnded
        self.winner = winner # False(0) for red(x) won, True(1) for yellow(o) won, -1 for draw
        # Decide who plays first, 0 then first player(red) plays first
        self.redTurn = redTurn

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
        if self.__checkPlayerWon('x'):
            self.gameEnded = True
            self.winner = 0
        elif self.__checkPlayerWon('o'):
            self.gameEnded = True
            self.winner = 1
        elif self.__checkDraw():
            self.gameEnded = True
            
    def __checkPlayerWon(self, color):
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

    def __checkDraw(self):
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