from gui_static import gameBoard
from tkinter import Tk, mainloop


def playgame():
    wnd = Tk()
    gameBoard(wnd)
    mainloop()
    
if __name__ == '__main__':
    playgame()