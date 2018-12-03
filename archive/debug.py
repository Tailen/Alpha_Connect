from game import board

gameBoard = board(cOut=True)
gameBoard.slots = [['x','o','o','o','x','o'],
                   ['o','o','x','x','x','o'],
                   ['o','x','o','o','x','x'],
                   ['o','x','x','x','o','x'],
                   ['x','x','o','o','x','o'],
                   ['o','o','x','o','x','x'],
                   ['-','o','x','o','x','o']]
gameBoard.placeMove(6)
print(gameBoard.gameEnded)
