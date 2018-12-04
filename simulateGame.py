# A simplified version of game class for simulations in tree search
class simulatedGame(object):

    def __init__(self, slots, gameEnded, winner, redTurn):
        self.slots = slots
        self.gameEnded = gameEnded
        self.winner = winner # False(0) for red(x) won, True(1) for yellow(o) won, -1 for draw
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

    # Return a list of valid moves (0-6)
    def getValidMoves(self):
        cord = []
        for x in range(7):
            lowest_y = -1
            for y in range(6):
                if self.slots[x][y] == '-':
                    lowest_y += 1
            if lowest_y != -1:
                cord.append(x)
        return cord