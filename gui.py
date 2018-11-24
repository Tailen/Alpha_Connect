import pygame
from time import time
from game import board



class boardGUI:

    def __init__(self):
        return


class gameBoard:

    def __init__(self, wnd):
        # Create main window
        self.wnd = wnd
        self.wnd.title('Connect++')
        self.game = board()
        # Set Grid to resize with main window
        for x in range(7):
            self.wnd.columnconfigure(x, weight=1)
        for y in range(2):
            self.wnd.rowconfigure(y, weight=1)
        # Create 42 slots in main window
        self.slotList = [[] for i in range(7)]
        for x in range(7):
            self.slotList[x].append(stack(self.wnd, x, self))
        # Create Frame and label below all slots
        self.bottomFrame = Frame(self.wnd, borderwidth=1, relief='solid')
        self.bottomFrame.grid(column=0, row=1, columnspan=7, sticky='EWSN')
        self.label = Label(self.bottomFrame, text='Good Luck, Have Fun!', font=("Courier", 18))
        self.label.pack()
        # Initialize last_time
        self.last_time = time()

    def makeMove(self, x):
        if (not self.game.gameEnded) and (time()-self.last_time) > 0.5:
            redTurn, _, y, msg = self.game.placeMove(x+1) # Input of placeMove is 1-7
            if y != -1:
                self.slotList[x][y].placePiece(redTurn)
            # If msg is not empty, update the msg
            if bool(msg):
                self.label.config(text=msg)
            self.last_time = time()



class icon:

    def __init__(self, icon_name):
        return

    def __pressed(self):
        # Shrink icon by 5% centered in middle
        return


if __name__ == '__main__':
    # wnd = Tk()
    # game = gameBoard(wnd)
    # mainloop()
    pygame.init()
    gameDisplay = pygame.display.set_mode((800,600))
    pygame.display.set_caption('Alpha Connect')
    clock = pygame.time.Clock()
    crashed = False
    while not crashed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed == True
            print(event)
        pygame.display.update()
        clock.tick(30)
    pygame.quit()
    quit()