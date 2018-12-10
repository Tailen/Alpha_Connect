# Import outside libraries
import tensorflow as tf
import numpy as np
from keras.layers import Input, Dense, Conv2D, Flatten, LeakyReLU, BatchNormalization, add
from keras.regularizers import l2
from keras.models import Model
from keras.optimizers import Adam
import pickle # Save and load model weights
# Import other project files
from simulateGame import simulatedGame


global graph
graph = tf.get_default_graph()


class policyValueNet(object):
    '''
    This class creates the policy-value-network, save and load weights, fit and predict
    '''

    BOARD_WIDTH = 7
    BOARD_HEIGHT = 6
    lr = 1e-3 # 1e-3 is the default learning rate for Adam in Keras
    l2_factor = 1e-4 # 1e-2 is the default factor of l2 regularization in Keras
    

    def __init__(self, weights_filepath=None):
        # Build the model
        self.model = self.createModel() 
        # Load weights if the filename is given
        if weights_filepath:
            weights = pickle.load(open(weights_filepath, 'rb'))
            self.model.set_weights(weights)

    # Creat the policy-value-network
    def createModel(self):
        # Input layer
        modelInput = Input(shape=(self.BOARD_WIDTH, self.BOARD_HEIGHT, 1), name='modelInput')
        # Convolutional layers (shared by value and policy networks)
        # conv1
        convNet = Conv2D(filters=16, kernel_size=(3, 3), data_format='channels_last', padding='same',
            activation='relu', kernel_regularizer=l2(self.l2_factor), name='conv1')(modelInput)
        convNet = BatchNormalization(axis=-1, name='bn1')(convNet)
        # conv2
        convNet = Conv2D(filters=32, kernel_size=(3, 3), data_format='channels_last', padding='same',
            activation='relu', kernel_regularizer=l2(self.l2_factor), name='conv2')(convNet)
        convNet = BatchNormalization(axis=-1, name='bn2')(convNet)
        # conv3
        convNet = Conv2D(filters=64, kernel_size=(3, 3), data_format='channels_last', padding='same',
            activation='relu', kernel_regularizer=l2(self.l2_factor), name='conv3')(convNet)
        convNet = BatchNormalization(axis=-1, name='bn3')(convNet)
        # conv4
        convNet = Conv2D(filters=64, kernel_size=(3, 3), data_format='channels_last', padding='same',
            activation='relu', kernel_regularizer=l2(self.l2_factor), name='conv4')(convNet)
        convNet = BatchNormalization(axis=-1, name='bn4')(convNet)
        # conv5
        convNet = Conv2D(filters=64, kernel_size=(3, 3), data_format='channels_last', padding='same',
            activation='relu', kernel_regularizer=l2(self.l2_factor), name='conv5')(convNet)
        convNet = BatchNormalization(axis=-1, name='bn5')(convNet)

        # Policy network layers
        # 1x1 Feature Compression Conv Layer
        policyNet = Conv2D(filters=1, kernel_size=(1, 1), data_format="channels_last", 
            activation="relu", kernel_regularizer=l2(self.l2_factor), name='policy_conv')(convNet)
        policyNet = BatchNormalization(axis=-1, name='policy_bn')(policyNet)
        policyNet = Flatten(name='policy_flatten')(policyNet)
        # Policy network out layer, one-hot array of the width of the board
        policyNetOut = Dense(self.BOARD_WIDTH, activation="softmax", 
            kernel_regularizer=l2(self.l2_factor), name='policyNetOut')(policyNet)

        # Value network layers
        # 1x1 Feature Compression Conv Layer
        valueNet = Conv2D(filters=2, kernel_size=(1, 1), data_format="channels_last", 
            activation="relu", kernel_regularizer=l2(self.l2_factor), name='value_conv')(convNet)
        valueNet = BatchNormalization(axis=-1, name='value_bn')(valueNet)
        valueNet = Flatten(name='value_flatten')(valueNet)
        # Dense Layer before output
        valueNet = Dense(32, kernel_regularizer=l2(self.l2_factor), name='value_dense')(valueNet)
        # Value network out layer, outputs game outcome prediction from -1 to 1
        valueNetOut = Dense(1, activation="tanh", 
            kernel_regularizer=l2(self.l2_factor), name='valueNetOut')(valueNet)

        # Build the whole network
        model = Model(inputs=modelInput, outputs=[policyNetOut, valueNetOut])
        model.compile(loss={'policyNetOut': 'categorical_crossentropy', 'valueNetOut': 'mse'},
                      optimizer=Adam(lr=self.lr), loss_weights={'policyNetOut': 0.5, 'valueNetOut': 0.5},
                      metrics={'policyNetOut': 'acc', 'valueNetOut': 'mse'})
        return model

    def fit(self, x, y, epochs, validation_split, batch_size):
        return self.model.fit(x, y, epochs=epochs, 
            validation_split = validation_split, batch_size = batch_size)     
    
    # Convert board to np array, then predict the input
    def predict(self, board):
        x = self.convertInput(board)
        with graph.as_default():
            return self.model.predict(x)

    # Save weights to filepath
    def saveWeights(self, filepath):
        weights = self.model.get_weights()  
        pickle.dump(weights, open(filepath, 'wb'), protocol=2)

    # Load weights from filepath
    def loadWeights(self, filepath):
        weights = pickle.load(open(filepath, 'rb'))
        self.model.set_weights(weights)

    # Convert input from a 7x6 2D List to the network input of (?, 7, 6, 1) numpy array
    # Red pieces are 1, yellow pieces are -1, and empty positions are 0
    def convertInput(self, board):
        board = np.array(board)
        return board.reshape(-1, self.BOARD_WIDTH, self.BOARD_HEIGHT, 1)

    # Save the graph of the current neural network to model.png
    def getNNGraph(self):
        from keras.utils import plot_model
        plot_model(self.model, to_file='./model.png', show_shapes = True)


model = policyValueNet('./weights.h5')

# model.saveWeights('./weights.h5')

# slots = [['x','o','o','o','x','o'],
#         ['o','o','x','x','x','o'],
#         ['o','x','o','o','x','x'],
#         ['o','x','x','x','o','x'],
#         ['x','x','o','o','x','o'],
#         ['o','o','x','o','x','x'],
#         ['-','o','x','o','x','o']]
# output = model.predict(slots)
# a = output[0][0]
# b = output[1][0][0]
# print(output)
# print(a)
# print(b)