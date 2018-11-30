from tkinter import Tk, Frame, Label, Canvas, mainloop
from random import randint
from time import time
from game import game
from mcts import MCTSPlayer
from players import humanGUIPlayer


class gameBoard:

    def __init__(self, wnd, players):
        # Create main window
        self.wnd = wnd
        self.wnd.title('Connect++')
        self.game = game(players, cout=False)
        # Set Grid to resize with main window
        for i in range(7):
            self.wnd.columnconfigure(i, weight=1)
        for i in range(7):
            self.wnd.rowconfigure(i, weight=1)
        # Create 42 slots in main window
        self.slotList = [[] for i in range(7)]
        for x in range(7):
            for y in range(6):
                self.slotList[x].append(slot(self.wnd, x, y, self))
        # Create Frame and label below all slots
        self.bottomFrame = Frame(self.wnd, borderwidth=1, relief='solid')
        self.bottomFrame.grid(column=0, row=6, columnspan=7, sticky='EWSN')
        self.label = Label(self.bottomFrame, text='Good Luck, Have Fun!', font=("Courier", 18))
        self.label.pack()
        # Initialize last_time
        self.last_time = time()
        # get the first player
        self.turn = False

    def makeMove(self, x):
        if (not self.game.gameEnded) and (time()-self.last_time) > 1.5:
            valid, y, redTurn = self.game.placeMove(x) # Input of placeMove is 0-6
            if valid:
                self.slotList[x][y].placePiece(redTurn)
            # # If msg is not empty, update the msg
            # if bool(msg):
            #     self.label.config(text=msg)
            self.last_time = time()

    def AIMove(self):
        mctsPlayer = MCTSPlayer(self.game)
        move = mctsPlayer.returnMove()
        self.makeMove(move)


class slot:

    # Canvas in a frame
    def __init__(self, wnd, x, y, board):
        self.board = board
        # colorList = ['red','yellow','blue','purple','pink','black','white','orange','green']
        self.frame = Frame(wnd, borderwidth=1, relief='solid')
        self.frame.grid(column=x, row=y, sticky='EWSN')
        self.canvas = Canvas(self.frame, width=100, height=100)
        self.canvas.bind('<Button-1>', lambda _: self.board.makeMove(x))
        self.canvas.pack(fill='both', expand=True)

    # Pass move to game engine and draw a circle
    def placePiece(self, redTurn):
        # print("clicked at", event.x, event.y)
        # self.game.placeMove(x)
        # if self.game.redTurn:
        if redTurn:
            self.canvas.create_oval(2,2,101,101, fill='red')
            # self.canvas.create_oval(0,0,int(self.canvas.cget('width'))/2,int(self.canvas.cget('height'))/2, fill='red')
        else:
            self.canvas.create_oval(2,2,101,101, fill='yellow')

        # # Immediately followed by AI move
        # self.board.turn = not self.board.turn
        # if self.board.turn:
        #     self.board.AIMove()


if __name__ == '__main__':
    wnd = Tk()
    player1 = humanGUIPlayer()
    player2 = humanGUIPlayer()
    game = gameBoard(wnd, [player1, player2])
    mainloop()