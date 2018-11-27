from mcts import MCTSPlayer
from game import board

gameBoard = board(cout=False)
while not gameBoard.gameEnded:
    print(gameBoard)
    move = int(input('Your move: '))
    while not gameBoard.validMove(move)[0]:
        move = int(input('Your move: '))
    gameBoard.placeMove(move)
    # mctsPlayer = MCTSPlayer(gameBoard)
    # move = mctsPlayer.returnMove()
    print(gameBoard)
    mctsPlayer2 = MCTSPlayer(gameBoard)
    move = mctsPlayer2.returnMove()
    gameBoard.placeMove(move)
print(gameBoard)