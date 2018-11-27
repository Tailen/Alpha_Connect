from random import randint


# For simpler reading x is red, o is green
class game(object):

    # Print msgs and errors if cout is True, players is a list of two players
    def __init__(self, players, cout=True):
        # (0,0) is top left corner
        self.slots = [['-' for i in range(6)] for i in range(7)]
        self.gameEnded = False
        self.winner = None # True(1) for red(x) won, False(0) for green(o) won, -1 for draw
        # Decide who plays first, 0 then first player(red) plays first
        self.redTurn = bool(randint(0, 1))
        self.cout = cout
        if self.redTurn and cout: print('Red(x) plays first\n')
        elif cout: print('Green(o) plays first\n')
        # True if the board is changed after GUI update
        self.changed = False

    def __str__(self):
        s = ''
        for y in range(6):
            for x in range(7):
                s = s + self.slots[x][y] + ' '
            s = s[:-1] + '\n'
        return s

    
