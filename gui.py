import pygame # For building the GUI
import time # For timing between moves to prevent unintended placements
from game import board # The basic machanics of the game
import os # To traverse directories and load images


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
        self.last_time = time.time()

    def makeMove(self, x):
        if (not self.game.gameEnded) and (time.time()-self.last_time) > 0.5:
            redTurn, _, y, msg = self.game.placeMove(x+1) # Input of placeMove is 1-7
            if y != -1:
                self.slotList[x][y].placePiece(redTurn)
            # If msg is not empty, update the msg
            if bool(msg):
                self.label.config(text=msg)
            self.last_time = time.time()


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

    # Set parameters
    fps = 30
    defaultWidth, defaultHeight = 3200, 1800
    imageFolderPath = './pic/'
    # Preset color values
    black = (0, 0, 0)
    white = (255, 255, 255)
    red = (255, 0, 0)
    blue = (0, 0, 255)
    # Initialize pygame
    pygame.init()
    gameDisplay = pygame.display.set_mode(
        (defaultWidth, defaultHeight), pygame.FULLSCREEN)
    pygame.display.set_caption('Alpha Connect')
    # ---------------------------------------------
    screenInfo = pygame.display.Info()
    print(screenInfo)
    # print(pygame.display.list_modes())
    # ---------------------------------------------

    clock = pygame.time.Clock()
    # Load images from pic directory
    imageDic = {} # A dictionary of image names to the images
    for filename in os.listdir(imageFolderPath):
        if filename.endswith('.png'):
            path = os.path.join(imageFolderPath, filename)  
            imageName = filename[:-4]
            imageDic[imageName] = pygame.image.load(path).convert_alpha()
    imageDic['bg_menu'] = pygame.transform.scale(imageDic['bg_menu'], (defaultWidth, defaultHeight))
    
    # Start screen main loop
    def showStartScreen():
        closed = False
        while not closed:
            # Check events
            for event in pygame.event.get():
                # Exit event
                if event.type == pygame.QUIT:
                    closed = True
                # Keydown events
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        closed = True
                # Resize event
                # elif event.type == pygame.VIDEORESIZE:
                #     gameDisplay = pygame.display.set_mode(
                #         event.dict['size'], pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)
                #     gameDisplay.blit(pygame.transform.scale(imageDic['bg_menu'], event.dict['size']), (0, 0))
            # # Update display
            gameDisplay.blit(imageDic['bg_menu'], (0, 0))
            pygame.display.flip()

            # Set framerate
            clock.tick(fps)
        # Quit program if main loop break
        pygame.quit()
        quit()
    
    # Game screen main loop
    def showGameScreen():
        crashed = False
        while not crashed:
            # Check events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    crashed = True
            # Update display
            gameDisplay.fill(white)
            gameDisplay.blit(imageDic['board_back'], (32, 14))
            gameDisplay.blit(imageDic['board_front'], (0, 10))
            pygame.display.flip()
            # Set framerate
            clock.tick(fps)
        # Quit program if main loop break
        pygame.quit()
        quit()

    showStartScreen()