'''Training pipeline of the policy-value-network through self-play'''


# Import outside libraries
import numpy as np
from collections import deque
import time, os, sys
from copy import deepcopy
from pytorch_classification.utils import Bar, AverageMeter
from pickle import Pickler, Unpickler
from random import shuffle
# Import other project files
from game import game
from model import policyValueNet
from players import AlphaConnectPlayer
from utils import dotdict


args = dotdict({
    'numIters': 1000,
    'numEps': 100,
    'tempThreshold': 15,
    'updateThreshold': 0.6,
    'maxlenOfQueue': 200000,
    'numMCTSSims': 100,
    'arenaCompare': 50,
    'cpuct': 5,

    'checkpoint': './checkpoints/',
    'load_model': False,
    'load_folder_file': ('/weights','best.pth.tar'),
    'numItersForTrainExamplesHistory': 20,
})


class selfTrain(object):
    """
    This class executes the self-play + learning. It uses the functions defined
    in Game and NeuralNet. args are specified in main.py.
    """

    def __init__(self):
        if args.load_model:
            modelFile = os.path.join(args.load_folder_file[0], args.load_folder_file[1])
            self.player1 = AlphaConnectPlayer(modelFile)
        else:
            self.player1 = AlphaConnectPlayer()
        self.player2 = deepcopy(self.player1) # The competitor player
        self.trainExamplesHistory = [] # History of examples from args.numItersForTrainExamplesHistory latest iterations
        self.skipFirstSelfPlay = False # Can be overriden in loadTrainExamples()

    def executeEpisode(self):
        """
        This function executes one episode of self-play, starting with player 1.
        As the game is played, each turn is added as a training example to
        trainExamples. The game is played till the game ends. After the game
        ends, the outcome of the game is used to assign values to each example
        in trainExamples.

        It uses a temp=1 if episodeStep < tempThreshold, and thereafter
        uses temp=0.

        Returns:
            trainExamples: a list of examples of the form (canonicalBoard,pi,v)
                           pi is the MCTS informed policy vector, v is +1 if
                           the player eventually won the game, else -1.
        """
        trainExamples = []
        game = game(self.player1, player2, cout=False)
        self.curPlayer = 1
        episodeStep = 0
        while True:
            episodeStep += 1
            canonicalBoard = self.game.getCanonicalForm(board,self.curPlayer)
            pi = self.mcts.getActionProb(canonicalBoard, temp=temp)
            sym = self.game.getSymmetries(canonicalBoard, pi)
            for b,p in sym:
                trainExamples.append([b, self.curPlayer, p, None])

            action = np.random.choice(len(pi), p=pi)
            board, self.curPlayer = self.game.getNextState(board, self.curPlayer, action)
            winner = self.game.winner(board, self.curPlayer)

            if winner != None:
                return [(x[0], x[2], winner*((-1)**(x[1]!=self.curPlayer))) for x in trainExamples]

    def learn(self):
        """
        Performs numIters iterations with numEps episodes of self-play in each
        iteration. After every iteration, it retrains neural network with
        examples in trainExamples (which has a maximium length of maxlenofQueue).
        It then pits the new neural network against the old one and accepts it
        only if it wins >= updateThreshold fraction of games.
        """

        for i in range(1, args.numIters+1):
            # bookkeeping
            print('------ITER ' + str(i) + '------')
            # examples of the iteration
            if not self.skipFirstSelfPlay or i>1:
                iterationTrainExamples = deque([], maxlen=args.maxlenOfQueue)
    
                eps_time = AverageMeter()
                bar = Bar('Self Play', max=args.numEps)
                end = time.time()
    
                for eps in range(args.numEps):
                    self.mcts = MCTS(self.game, self.player1, args)   # reset search tree
                    iterationTrainExamples += self.executeEpisode()
    
                    # bookkeeping + plot progress
                    eps_time.update(time.time() - end)
                    end = time.time()
                    bar.suffix  = '({eps}/{maxeps}) Eps Time: {et:.3f}s | Total: {total:} | ETA: {eta:}'.format(eps=eps+1, maxeps=args.numEps, et=eps_time.avg,
                                                                                                               total=bar.elapsed_td, eta=bar.eta_td)
                    bar.next()
                bar.finish()

                # save the iteration examples to the history 
                self.trainExamplesHistory.append(iterationTrainExamples)
                
            if len(self.trainExamplesHistory) > args.numItersForTrainExamplesHistory:
                print("len(trainExamplesHistory) =", len(self.trainExamplesHistory), " => remove the oldest trainExamples")
                self.trainExamplesHistory.pop(0)
            # backup history to a file
            # NB! the examples were collected using the model from the previous iteration, so (i-1)  
            self.saveTrainExamples(i-1)
            
            # shuffle examlpes before training
            trainExamples = []
            for e in self.trainExamplesHistory:
                trainExamples.extend(e)
            shuffle(trainExamples)

            # training new network, keeping a copy of the old one
            self.player1.network.saveWeights(folder=args.checkpoint, filename='temp.pth.tar')
            self.player2.network.loadWeights(folder=args.checkpoint, filename='temp.pth.tar')
            pmcts = MCTS(self.game, self.player2, args)
            
            self.player1.train(trainExamples)
            nmcts = MCTS(self.game, self.player1, args)

            print('PITTING AGAINST PREVIOUS VERSION')
            arena = Arena(lambda x: np.argmax(pmcts.getActionProb(x, temp=0)),
                          lambda x: np.argmax(nmcts.getActionProb(x, temp=0)), self.game)
            pwins, nwins, draws = arena.playGames(args.arenaCompare)

            print('NEW/PREV WINS : %d / %d ; DRAWS : %d' % (nwins, pwins, draws))
            if pwins+nwins > 0 and float(nwins)/(pwins+nwins) < args.updateThreshold:
                print('REJECTING NEW MODEL')
                self.player1.load_checkpoint(folder=args.checkpoint, filename='temp.pth.tar')
            else:
                print('ACCEPTING NEW MODEL')
                self.player1.save_checkpoint(os.path.join(folder=args.checkpoint, filename=self.getCheckpointFile(i)))
                self.player1.save_checkpoint(os.path.join(folder=args.checkpoint, filename='best.pth.tar'))

    def getCheckpointFile(self, iteration):
        return 'checkpoint_' + str(iteration) + '.pth.tar'

    def saveTrainExamples(self, iteration):
        folder = args.checkpoint
        if not os.path.exists(folder):
            os.makedirs(folder)
        filename = os.path.join(folder, self.getCheckpointFile(iteration)+".examples")
        with open(filename, "wb+") as f:
            Pickler(f).dump(self.trainExamplesHistory)
        f.closed

    def loadTrainExamples(self):
        modelFile = os.path.join(args.load_folder_file[0], args.load_folder_file[1])
        examplesFile = modelFile+".examples"
        if not os.path.isfile(examplesFile):
            print(examplesFile)
            r = input("File with trainExamples not found. Continue? [y|n]")
            if r != "y":
                sys.exit()
        else:
            print("File with trainExamples found. Read it.")
            with open(examplesFile, "rb") as f:
                self.trainExamplesHistory = Unpickler(f).load()
            f.closed
            # examples based on the model were already collected (loaded)
            self.skipFirstSelfPlay = True


if __name__=="__main__":
    c = selfTrain()
    if args.load_model:
        print("Load trainExamples from file")
        c.loadTrainExamples()
    c.learn()