import pygame # For building the GUI
import time # For timing between moves to prevent unintended placements
from game import game # The basic machanics of the game
import os # To traverse directories and load images
from random import randint
from threading import Thread, Event, Lock # Allow responsive UI
from players import humanGUIPlayer, MCTSPlayer, AlphaConnectPlayer


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
boardFrontPos = (180, 60)
boardBackPos = (212, 64)
turnLabelPos = (990, 420)
homeBtnPos = (1170, 15)
restartBtnPos = (1065, 15)
musicBtnPos = (960, 15)
vsHumanBtnPos = (270, 270)
vsAIBtnPos = (690, 270)
# Initialize threading lock objects
moveEvent = Event() # Block gameTread when waiting GUIPlayer input
boardLock = Lock() # Block gameTread when updating board postitions


# Show start sceen
def showStartScreen(isFullscreen=False, music=True):
    # Initialize button instances
    minimizeBtn = button(fullscreenBtnPos, 96, 101, 'btn_minimize', command=setWindowed)
    maximizeBtn = button(fullscreenBtnPos, 96, 101, 'btn_maximize', command=setFullScreen)
    musicBtn = button(homeBtnPos, 96, 101, 'btn_sound', command=setMute)
    muteBtn = button(homeBtnPos, 96, 101, 'btn_mute', command=setSound)
    playBtn = button(playBtnPos, 233, 239, 'btn_play',
        animate=True, command=lambda: showSelectScreen(isFullscreen, music))
    # Start screen main loop
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
        gameDisplay.blit(imageDic['bg_menu'], (0, 0))
        playBtn.update()
        if music:
            if musicBtn.update():
                music = False
        else:
            if muteBtn.update():
                music = True
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
def showSelectScreen(isFullscreen=False, music=True):
    # Initialize button instances
    homeBtn = button(homeBtnPos, 96, 101, 'btn_home', 
        command=lambda: showStartScreen(isFullscreen, music))
    musicBtn = button(restartBtnPos, 96, 101, 'btn_sound', command=setMute)
    muteBtn = button(restartBtnPos, 96, 101, 'btn_mute', command=setSound)
    vsHumanBtn = button(vsHumanBtnPos, 316, 250, 'btn_human', command=lambda: startHumanGame())
    vsAIBtn = button(vsAIBtnPos, 316, 250, 'btn_ai', command=lambda: startAIGame())
    def startHumanGame():
        player1 = humanGUIPlayer(moveEvent)
        player2 = humanGUIPlayer(moveEvent)
        showGameScreen(isFullscreen, music, player1, player2)
    def startAIGame():
        player1 = MCTSPlayer()
        player2 = humanGUIPlayer(moveEvent)
        showGameScreen(isFullscreen, music, player1, player2)
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
        homeBtn.update()
        vsHumanBtn.update()
        vsAIBtn.update()
        if music:
            if musicBtn.update():
                music = False
        else:
            if muteBtn.update():
                music = True
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
def showGameScreen(isFullscreen=False, music=True, player1=MCTSPlayer, player2=humanGUIPlayer(moveEvent)):
    # Initialize button instances
    minimizeBtn = button(fullscreenBtnPos, 96, 101, 'btn_minimize', command=setWindowed)
    maximizeBtn = button(fullscreenBtnPos, 96, 101, 'btn_maximize', command=setFullScreen)
    homeBtn = button(homeBtnPos, 96, 101, 'btn_home',
        command=lambda: startScreenNext(gameThread))
    restartBtn = button(restartBtnPos, 96, 101, 'btn_restart', 
        command=lambda: gameScreenNext(gameThread))
    # End and wait for gameThread before show other screens
    def startScreenNext(gameThread):
        gameBackend.gameEnded = True
        gameThread.join()
        showStartScreen(isFullscreen, music)
    def gameScreenNext(gameThread):
        gameBackend.gameEnded = True
        gameThread.join()
        showGameScreen(isFullscreen, music, player1, player2)
    musicBtn = button(musicBtnPos, 96, 101, 'btn_sound', command=setMute)
    muteBtn = button(musicBtnPos, 96, 101, 'btn_mute', command=setSound)
    tracker = Tracker() # Responsible for passing the gui input to player class
    gamePieces = Pieces() # Animates the piece drop down
    # Randomize the order of how two players are passed to game
    player1Turn = randint(0, 1)
    if player1Turn:
        gameThread = Thread(target=startBackend, args=[player1, player2], daemon=True)
    else:
        gameThread = Thread(target=startBackend, args=[player2, player1], daemon=True)
    turnLabel = TurnLabel(turnLabelPos, player1Turn, player1.name, player2.name)
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
                gamePieces.dropPiece(gameBackend.lastMove)



                gameBackend.modified = False
            # Update turnLabel if game ended
            if gameBackend.gameEnded:
                turnLabel.gameEnded = True
                turnLabel.winner = gameBackend.winner
        gameDisplay.blit(imageDic['board_back'], boardBackPos)
        gamePieces.update()
        gameDisplay.blit(imageDic['board_front'], boardFrontPos)
        turnLabel.update(player1Turn)
        tracker.update(player1Turn, (player1, player2))
        homeBtn.update()
        restartBtn.update()
        if music:
            if musicBtn.update():
                music = False
        else:
            if muteBtn.update():
                music = True
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

def setSound():
    pygame.mixer.music.play()

def setMute():
    pygame.mixer.music.fadeout(1000)

def show_text(text, size, pos, width, height):
    font = pygame.font.Font('FreeSans.ttf', size)
    TextSurf = font.render(text, True, black)
    TextRect = TextSurf.get_rect()
    TextRect.center = ((pos[0]+width/2),(pos[1]+height/2))
    gameDisplay.blit(TextSurf, TextRect)


class button:
    '''
    A button object implemented in pygame. 
    It can animate scaling effect, and return True if pressed.
    If command is given, execute that command when pressed.
    '''

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
        self.waitMouseUp = False

    # Check if cursor overlaps button area, change cursor shape, and return pressed status
    # Mind that rendered screen and root screen are different: 
    # gameDisplay is always default width and height, root scales to current screen size
    # Drawn images are on gameScreen, while mouse clicks are on root screen
    def update(self):
        # Animate the button
        if self.animate:
            if self.currentScale > 1.05 or self.currentScale < 0.95:
                self.growingSpeed = -self.growingSpeed
            self.currentScale += self.growingSpeed
            # Calculate animation scaled drawn width, height, and x, y
            d_W = int(self.width*self.currentScale)
            d_H = int(self.height*self.currentScale)
            scaledImage = pygame.transform.smoothscale(imageDic[self.imageName], (d_W, d_H))
            d_X = int(self.pos[0] + self.width*(1-self.currentScale)/2)
            d_Y = int(self.pos[1] + self.height*(1-self.currentScale)/2)
            gameDisplay.blit(scaledImage, (d_X, d_Y))
        else: 
            # For static images, drawn width, height, and x, y are equal to default
            d_X, d_Y, d_W, d_H = self.pos[0], self.pos[1], self.width, self.height
            # Refresh the static image
            gameDisplay.blit(imageDic[self.imageName], (d_X, d_Y))
        # Get information about the mouse
        mousePos = pygame.mouse.get_pos()
        mousePress = pygame.mouse.get_pressed()[0]
        # Calculate cursor width, height, and x, y based on respective drawn ones 
        (c_X, c_Y, c_W, c_H) = tuple([i*currentScreenScale for i in (d_X, d_Y, d_W, d_H)])
        # Check overlap
        if c_X <= mousePos[0] <= c_X+c_W and c_Y <= mousePos[1] <= c_Y+c_H:
            # If cursor overlaps the input area, change the cursor
            if not self.onButton:
                pygame.mouse.set_cursor(*pygame.cursors.ball)
                self.onButton = True
            # Execute command if mouse is pressed and up on the button
            if mousePress and not self.waitMouseUp:
                self.waitMouseUp = True
            if not mousePress and self.waitMouseUp:
                pygame.mouse.set_cursor(*pygame.cursors.arrow) # Turn cursor back to arrow if click
                self.waitMouseUp = False
                if self.command != None: self.command()
                return True
        # Change the cursor back to arrow if moved away from button
        elif self.onButton:
            pygame.mouse.set_cursor(*pygame.cursors.arrow)
            self.onButton = False
        return False


class TurnLabel:
    '''
    A turn-label object implemented in pygame.
    '''

    def __init__(self, pos, player1Turn, player1Name, player2Name):
        self.pos = pos
        self.piecePos = (pos[0]+52, pos[1]+66)
        self.textPos = (pos[0]+27, pos[1]+17)
        self.player1Turn = player1Turn
        self.player1Name = player1Name
        self.player2Name = player2Name
        self.gameEnded = False
        self.winner = None

    # Check current turn, and change turn label if applicable
    def update(self, player1Turn):
        self.player1Turn = player1Turn
        gameDisplay.blit(imageDic['bg_turn'], self.pos)
        if not self.gameEnded:
            if gameBackend.redTurn:
                gameDisplay.blit(imageDic['red_piece'], self.piecePos)
            else:
                gameDisplay.blit(imageDic['yellow_piece'], self.piecePos)
            # Show text 'Human Turn' or 'AI Turn' if is a AI vs Human game 
            if self.player1Name != self.player2Name:
                if self.player1Turn:
                    show_text((self.player1Name+' Turn'), 21, self.textPos, 130, 24)
                else:
                    show_text((self.player2Name+' Turn'), 21, self.textPos, 130, 24)
            # Else show 'Player 1' or 'Player 2' directly
            else: 
                if self.player1Turn:
                    show_text('Player1 Turn', 21, self.textPos, 130, 24)
                else:
                    show_text('Player2 Turn', 21, self.textPos, 130, 24)
        # Game Ended
        else:
            if self.player1Name == self.player2Name:
                if self.winner == -1:
                    show_text('Draw! GGWP', 21, self.textPos, 130, 24)
                elif self.winner == 0:
                    show_text('Red Won!', 21, self.textPos, 130, 24)
                else:
                    show_text('Yellow Won!', 21, self.textPos, 130, 24)
            else:
                if self.winner == -1:
                    show_text('Draw! GGWP', 21, self.textPos, 130, 24)
                elif self.player1Turn:
                    show_text(self.player2Name + ' Won!', 21, self.textPos, 130, 24)
                else:
                    show_text(self.player1Name + ' Won!', 21, self.textPos, 130, 24) 


class Tracker:
    '''
    A Tracker object implemented in pygame.
    Follows the mouse in the seven columns.
    Animated with parametric blend function to achieve ease-in/ease-out.
    '''

    # Class constants
    trackerY = 6
    # Border X for tracker
    trackerXList = [boardFrontPos[0]+66+i*92 for i in range(8)]
    # How many frames used for one animation
    totalFrame = int(fps/2)

    def __init__(self):
        # Put the tracker on 4th column(center) when first initialized
        self.trackerColumn = 3
        # 46 is half the distance between slots
        self.currentX = Tracker.trackerXList[self.trackerColumn] + 46
        self.targetX = self.currentX
        self.animating = False
        self.frameCount = 0
        self.waitMouseUp = False
        self.last_time = time.time()
        
    def update(self, player1Turn, players):
        # Get information about the mouse
        cursorX = int(pygame.mouse.get_pos()[0] / currentScreenScale)
        mousePress = pygame.mouse.get_pressed()[0]
        # Animate and move the tracker
        for i in range(7):
            if Tracker.trackerXList[i] < cursorX < Tracker.trackerXList[i+1]:
                if i != self.trackerColumn:
                    self.trackerColumn = i
                    self.targetX = Tracker.trackerXList[self.trackerColumn] + 46
                    self.__getMoveList()
                    self.animating = True
                    self.frameCount = 0
        # Display tracker at the current column if target column did not change
        if self.animating:
            self.__animate()
        else:
            # -50 is to compensate distance from top-left corner of image to point of the tracker
            gameDisplay.blit(imageDic['arrow'], (self.currentX-50, Tracker.trackerY))
        # Detect mouse down and wait for mouse up
        if mousePress and not self.waitMouseUp:
            # Any move within 1 sec will be discarded to prevent unwanted moves
            if (time.time() - self.last_time) > 1:
                self.last_time = time.time()
                self.waitMouseUp = True
        # Send input to player instances
        if not mousePress and self.waitMouseUp:
            self.waitMouseUp = False
            if players[not player1Turn].name == 'Human':
                # Select the current player and input move
                players[not player1Turn].GUIInput(self.trackerColumn)
                # Release the block on backend
                moveEvent.set()

    # Animate the move from one column to another based on calculated moveList
    def __animate(self):
        self.currentX = self.moveList[self.frameCount]
        gameDisplay.blit(imageDic['arrow'], (self.currentX-50, Tracker.trackerY))
        self.frameCount += 1
        if self.frameCount == Tracker.totalFrame:
            self.animating = False

    # Return the list of move steps of the animation
    def __getMoveList(self):
        f = Tracker.totalFrame
        # Ease in/ease out intervals in range [0, 1] 
        intervals = [self.__parametricBlend((i+1)/f) for i in range(f)]
        self.moveList = [int((self.targetX-self.currentX)*i+self.currentX) for i in intervals]

    # Calculate the parametric equation to achieve ease in/ease out animation
    def __parametricBlend(self, t):
        sqt = t**2
        return sqt / (2.0 * (sqt - t) + 1.0)


class Pieces:
    '''
    Game piece object implemented in pygame. Animates the piece dropping effect.
    '''

    # Class constants: x and y values for pieces
    xList = [boardFrontPos[0]+74+i*92 for i in range(7)]
    yList = [boardFrontPos[1]+33+i*92 for i in range(6)]
    # Frames used for one animation
    totalFrame = int(fps/2)

    def __init__(self):
        self.animating = False # Assume one piece animation at a time
        self.frameCount = 0
        self.pieceList = [] # A piece is added to pieceList after its animation

    # Animate dropping a piece, lastMove is encoded as (x, y, color(1 for red, 0 for yellow))
    def dropPiece(self, lastMove):



        self.pieceList.append(lastMove)

    def update(self):
        # Render static pieces
        for (x, y, red) in self.pieceList:
            if red:
                gameDisplay.blit(imageDic['red_piece'], (Pieces.xList[x], Pieces.yList[y]))
            else:
                gameDisplay.blit(imageDic['yellow_piece'], (Pieces.xList[x], Pieces.yList[y]))
        # Render dropping piece
        return


# Initialize pygame
pygame.init()
root = pygame.display.set_mode((defaultWidth, defaultHeight))
gameDisplay = root.copy()
pygame.display.set_caption('Alpha Connect')
clock = pygame.time.Clock()
# Load and play background music
pygame.mixer.init()
pygame.mixer.music.load('./bg_music.mp3')
pygame.mixer.music.play()
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
    showStartScreen()