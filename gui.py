import pygame # For building the GUI
import time # For timing between moves to prevent unintended placements
from game import game # The basic machanics of the game
import os # To traverse directories and load images
from random import randint
from threading import Thread, Event, Lock
from players import humanGUIPlayer


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
boardFrontPos = (180, 50)
boardBackPos = (212, 54)
turnLabelPos = (900, 330)
# Initialize threading lock objects
moveEvent = Event() # Block gameTread when waiting GUIPlayer input
boardLock = Lock() # Block gameTread when updating board postitions


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
            if minimizeBtn.update(): # button.update returns True if button is clicked
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
    quitWindow()

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
    quitWindow()

# Show game screen
def showGameScreen(isFullscreen=False):
    # Initialize button instances
    minimizeBtn = button(fullscreenBtnPos, 96, 101, 'btn_minimize', command=setWindowed)
    maximizeBtn = button(fullscreenBtnPos, 96, 101, 'btn_maximize', command=setFullScreen)
    turnLabel = button(turnLabelPos, 184, 195, 'bg_turn')
    tracker = rowTracker() # Responsible for passing the gui input to player class
    # Randomize the order of how two players are passed to game
    player1 = humanGUIPlayer(moveEvent)
    player2 = humanGUIPlayer(moveEvent)
    player1Turn = randint(0, 1)
    if player1Turn:
        gameThread = Thread(target=startBackend, args=[player1, player2], daemon=True)
    else:
        gameThread = Thread(target=startBackend, args=[player2, player1], daemon=True)
    # Start gameThread
    gameThread.start()
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
        with boardLock:
            if gameBackend.modified:
                player1Turn = not player1Turn
                # Update the GUI pieces based on lastMove and start new piece animation
                
                gameBackend.modified = False
                print(gameBackend)
        gameDisplay.blit(imageDic['board_back'], boardBackPos)
        gameDisplay.blit(imageDic['board_front'], boardFrontPos)
        turnLabel.update()
        tracker.update(player1Turn, (player1, player2))
        if isFullscreen:
            if minimizeBtn.update(): # button.update returns True if button is clicked
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
    quitWindow()

# Set the gameDisplay to fullscren mode, enable hardware acceleration and double buffering
def setFullScreen():
    # Scale display and image sizes
    pygame.display.set_mode(
        (maxWidth, maxHeight), pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)
    # Set currentScreenScale to fullscreen scale
    global currentScreenScale
    currentScreenScale = scaleRatio

# Set the gameDisplay to windowed mode, disable hardware acceleration and double buffering
def setWindowed():
    # Scale display and image sizes
    pygame.display.set_mode((defaultWidth, defaultHeight))
    # Set currentScreenScale to windowed scale (1.0)
    global currentScreenScale
    currentScreenScale = 1.0

def quitGame(gameThread):
    # Set gameEnded to end gameThread
    gameBackend.gameEnded = True
    # Raise 'Are you sure?' window, then call startScreen
    if True:
        gameThread.join()

# Uninitialize pygame, then python
def quitWindow():
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
            # Set current x, y, width, height to animation scaled version
            c_W = int(self.width*self.currentScale*currentScreenScale)
            c_H = int(self.height*self.currentScale*currentScreenScale)
            scaledImage = pygame.transform.smoothscale(imageDic[self.imageName], (c_W, c_H))
            c_X = int((self.pos[0] + self.width*(1-self.currentScale)/2) * currentScreenScale)
            c_Y = int((self.pos[1] + self.height*(1-self.currentScale)/2) * currentScreenScale)
            gameDisplay.blit(scaledImage, (c_X, c_Y))
        else: # Refresh the static image
            # For static button, current position and dimension is default times screenScale
            (c_X, c_Y, c_W, c_H) = tuple([i*currentScreenScale for i in (
                self.pos[0], self.pos[1], self.width, self.height)])
            gameDisplay.blit(imageDic[self.imageName], (c_X, c_Y))
        # Get information about the mouse
        mousePos = pygame.mouse.get_pos()
        mousePress = pygame.mouse.get_pressed()[0]
        # Check overlap
        if c_X <= mousePos[0] <= c_X+c_W and c_Y <= mousePos[1] <= c_Y+c_H:
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


class rowTracker:

    def __init__(self):
        self.currentX = 0
           
    def update(self, player1Turn, players):
        # Get information about the mouse
        mousePos = pygame.mouse.get_pos()
        mousePress = pygame.mouse.get_pressed()[0]
        if mousePress:
            # Select the current player and input move
            players[not player1Turn].GUIInput(3)
            # Release the lock on backend
            moveEvent.set()


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
currentScreenScale = 1.0


# Run game in background with another thread
def startBackend(playerA, playerB):
    # Block the main thread until gameBackend is initialized
    with boardLock:
        print('parent process id:', os.getppid())
        print('process id:', os.getpid())
        # Set globals so gameScreen have access to game object
        global gameBackend
        gameBackend = game(players=(playerA, playerB), cout=True)
    gameBackend.startGame()

if __name__ == "__main__":
#     # move = Value('i', 0)
#     # Start GUI process
#     GUIProcess = Process(target=showStartScreen)
#     GUIProcess.start()
<<<<<<< HEAD
    gameThread = Thread(target=playGame)
    gameThread.daemon = True # Terminate when main thread terminates
    gameThread.start()
=======
>>>>>>> 201f2d9ca66df73f7f92ce67b8abb3824192e2f3
    showStartScreen()