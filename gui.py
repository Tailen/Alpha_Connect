import pygame # For building the GUI
import time # For timing between moves to prevent unintended placements
from game import game # The basic machanics of the game
import os # To traverse directories and load images

from threading import Thread
from players import humanPlayer


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





# Set constants and defaults
fps = 30
defaultWidth, defaultHeight = 1280, 720
imageFolderPath = './pic/'
# Preset color values
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)
# Default button positions
fullscreenBtnPos = (15, 15)
playBtnPos = (810, 330)


# Show start sceen
def showStartScreen(isFullscreen=False):
    # Initialize button instances
    minimizeBtn = button(fullscreenBtnPos, 96, 101, 'btn_minimize', command=setWindowed)
    maximizeBtn = button(fullscreenBtnPos, 96, 101, 'btn_maximize', command=setFullScreen)
    playBtn = button(playBtnPos, 233, 239, 'btn_play',
        animate=True, command=lambda: showGameScreen(isFullscreen))
    # Start screen main loop
    running = True
    isFullscreen = False
    while running:
        # Check events
        for event in pygame.event.get():
            # Exit event
            if event.type == pygame.QUIT:
                running = False
            # Keydown events
            elif event.type == pygame.KEYDOWN:
                # Close the game when 'esc' is hit
                if event.key == pygame.K_ESCAPE:
                    running = False
        # Update display
        gameDisplay.blit(imageDic['bg_menu'], (0, 0))
        playBtn.update()
        if isFullscreen:
            if minimizeBtn.update():
                isFullscreen = False
            # Scale gameDisplay to fit onto root
            root.blit(pygame.transform.smoothscale(gameDisplay, (maxWidth, maxHeight)), (0, 0))
        else:
            if maximizeBtn.update():
                isFullscreen = True
            root.blit(gameDisplay, (0, 0))
        pygame.display.flip()
        # Set framerate
        clock.tick(fps)
    # Quit program if main loop break
    quitGame()

# def startGame():
#     from players import humanPlayer
#     l.acquire()
#     player1 = humanPlayer()
#     player2 = humanPlayer()
#     myGame = game(players=(player1, player2))
#     myGame.startGame()
#     l.release

# Show opponent selection screen
def showSelectScreen(isFullscreen=False):
    # Initialize button instances

    # Select screen main loop
    running = True
    while running:
        # Check events
        for event in pygame.event.get():
            # Exit event
            if event.type == pygame.QUIT:
                running = False
            # Keydown events
            elif event.type == pygame.KEYDOWN:
                # Close the game when 'esc' is hit
                if event.key == pygame.K_ESCAPE:
                    running = False
        # Update display
        gameDisplay.blit(imageDic['bg_select'], (0, 0))
        if isFullscreen:
            # Scale gameDisplay to fit onto root
            root.blit(pygame.transform.smoothscale(gameDisplay, (maxWidth, maxHeight)), (0, 0))
        else:
            root.blit(gameDisplay, (0, 0))
        pygame.display.flip()
        # Set framerate
        clock.tick(fps)
    # Quit program if main loop break
    quitGame()

# Show game screen
def showGameScreen(isFullscreen=False):
    # Initialize button instances

    # Game screen main loop
    running = True
    while running:
        # Check events
        for event in pygame.event.get():
            # Exit event
            if event.type == pygame.QUIT:
                running = False
            # Keydown events
            elif event.type == pygame.KEYDOWN:
                # Close the game when 'esc' is hit
                if event.key == pygame.K_ESCAPE:
                    running = False
        # Update display
        gameDisplay.blit(imageDic['bg_game'], (0, 0))
        gameDisplay.blit(imageDic['board_back'], (32, 14))
        gameDisplay.blit(imageDic['board_front'], (0, 10))
        if isFullscreen:
            # Scale gameDisplay to fit onto root
            root.blit(pygame.transform.smoothscale(gameDisplay, (maxWidth, maxHeight)), (0, 0))
        else:
            root.blit(gameDisplay, (0, 0))
        pygame.display.flip()
        # Set framerate
        clock.tick(fps)
    # Quit program if main loop break
    quitGame()

# Set the gameDisplay to fullscren mode, enable hardware acceleration and double buffering
def setFullScreen():
    # Scale display and image sizes
    pygame.display.set_mode(
        (maxWidth, maxHeight), pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)
    # imageDic['bg_menu'] = pygame.transform.smoothscale(imageDic['bg_menu'], (maxWidth, maxHeight))
    # imageDic['bg_menu'] = pygame.transform.smoothscale(imageDic['bg_menu'], (maxWidth, maxHeight))

# Set the gameDisplay to windowed mode, disable hardware acceleration and double buffering
def setWindowed():
    # Scale display and image sizes
    pygame.display.set_mode((defaultWidth, defaultHeight))
    # imageDic['bg_menu'] = pygame.transform.smoothscale(imageDic['bg_menu'], (defaultWidth, defaultHeight))
    # imageDic['bg_menu'] = pygame.transform.smoothscale(imageDic['bg_menu'], (defaultWidth, defaultHeight))

# Uninitialize pygame, then python
def quitGame():
    pygame.quit()
    quit()


class button:

    def __init__(self, pos, width, height, imageName, animate=False, command=None):
        self.pos = pos
        self.width = width
        self.height = height
        self.onButton = False
        self.animate = animate
        self.imageName = imageName
        self.command = command
        self.currentScale = 1.0
        self.growingSpeed = 0.15/fps

    # Check if cursor overlaps button area, change cursor shape, and return pressed status
    def update(self):
        # Animate the button
        if self.animate:
            if self.currentScale > 1.05 or self.currentScale < 0.95:
                self.growingSpeed = -self.growingSpeed
            self.currentScale += self.growingSpeed
            scaledImage = pygame.transform.smoothscale(imageDic[self.imageName], (
                int(self.width*self.currentScale), int(self.height*self.currentScale)))
            scaledX = self.pos[0] + self.width*(1-self.currentScale)/2
            scaledY = self.pos[1] + self.height*(1-self.currentScale)/2
            gameDisplay.blit(scaledImage, (scaledX, scaledY))
        else: # Refresh the static image
            gameDisplay.blit(imageDic[self.imageName], self.pos)
        # Get information about the mouse
        mousePos = pygame.mouse.get_pos()
        mousePress = pygame.mouse.get_pressed()[0]
        x = self.pos[0]
        y = self.pos[1]
        if x <= mousePos[0] <= x+self.width and y <= mousePos[1] <= y+self.height:
            # If cursor overlaps the input area, change the cursor
            if not self.onButton:
                pygame.mouse.set_cursor(*pygame.cursors.ball)
                self.onButton = True
            # Execute command if mouse is pressed on the button
            if mousePress:
                if self.command != None: self.command()
                return True
        # Change the cursor back to arrow if moved away from button
        elif self.onButton:
            pygame.mouse.set_cursor(*pygame.cursors.arrow)
            self.onButton = False
        return False


# Initialize pygame
pygame.init()
root = pygame.display.set_mode((defaultWidth, defaultHeight))
gameDisplay = root.copy()
pygame.display.set_caption('Alpha Connect')
clock = pygame.time.Clock()

# ---------------------------------------------
screenInfo = pygame.display.Info()
# print(screenInfo)
# ---------------------------------------------

# Load images from pic directory
imageDic = {} # A dictionary of image names to the images
for filename in os.listdir(imageFolderPath):
    if filename.endswith('.png'):
        path = os.path.join(imageFolderPath, filename)
        imageName = filename[:-4]
        imageDic[imageName] = pygame.image.load(path).convert_alpha()
# Resize backgrounds to default width and height
imageDic['bg_menu'] = pygame.transform.smoothscale(imageDic['bg_menu'], (defaultWidth, defaultHeight))
imageDic['bg_game'] = pygame.transform.smoothscale(imageDic['bg_game'], (defaultWidth, defaultHeight))
# Retreive the fullscreen(max) width and height of the display 
(maxWidth, maxHeight) = pygame.display.list_modes()[0]
scaleRatio = 1.0 * maxWidth / defaultWidth
# Calculate fullscreen object positions based on the scale ratio
max_fullscreenBtnPos = (fullscreenBtnPos[0]*scaleRatio, fullscreenBtnPos[1]*scaleRatio)
max_playBtnPos = (playBtnPos[0]*scaleRatio, playBtnPos[1]*scaleRatio)


# Test threading and multiprocessing feasibilities
def playGame():
    print('parent process id:', os.getppid())
    print('process id:', os.getpid())
    player1 = humanPlayer()
    player2 = humanPlayer()
    myGame = game(players=(player1, player2))
    myGame.startGame()

if __name__ == "__main__":
#     # move = Value('i', 0)
#     # Start GUI process
#     GUIProcess = Process(target=showStartScreen)
#     GUIProcess.start()
    gameThread = Thread(target=playGame)
    gameThread.start()
    showStartScreen()