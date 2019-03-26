import numpy as np

# replay buffer
from replayBuffer import ReplayBuffer

# import tensor libraries
from keras.models import Model, Sequential
from keras.layers import (Input, Conv2D, Dense,
        Flatten, Concatenate, Multiply, Lambda)
from keras.optimizers import Adam, SGD
import keras.backend as K

# random agent to help with training
class RandomAgent:
    def __init__(self, board_size):
        self._board_size = board_size

    def move(self, move_type, board):
        valid_moves = [i for i in range(len(board)) if board[i] == 0]
        assert len(valid_moves) > 0, "Invalid board for random agent"
        return int(np.random.choice(valid_moves, 1)[0])

# novice player is slightly smart, will try to form a 3 in a row
# or block, as we want the agent to learn these strategies
# strategy is not really scalable to boards of sizes more than 3
class NoviceAgent:
    def __init__(self, board_size):
        self._board_size = board_size

    def move(self, move_type, board):
        board_mod = board.reshape(self._board_size, self._board_size)
        # check if either move_type or opposite are being formed
        for i in range(self._board_size):
            # check in row
            if(abs(board_mod[i, :].sum()) == (self._board_size-1)):
                for j in range(self._board_size):
                    if(board_mod[i, j] == 0):
                        return i*self._board_size + j

            # check in column
            if(abs(board_mod[:, i].sum()) == (self._board_size-1)):
                for j in range(self._board_size):
                    if(board_mod[j, i] == 0):
                        return j*self._board_size + i

        # check the \ diagonal
        if(abs(sum([board_mod[i, i] for i in range(self._board_size)])) == (self._board_size-1)):
            for i in range(self._board_size):
                if(board_mod[i, i] == 0):
                    return i*self._board_size + i

        # check the / diagonal
        if(abs(sum([board_mod[i, self._board_size-1 - i] for i in range(self._board_size)])) == (self._board_size-1)):
            for i in range(self._board_size):
                if(board_mod[i, self._board_size - 1 - i] == 0):
                    return i*self._board_size + self._board_size - 1 - i

        # if none of the above combo is possible, return a random cell
        valid_moves = [i for i in range(len(board)) if board[i] == 0]
        return int(np.random.choice(valid_moves, 1)[0])

# class for the rl agent playing tic tac toe
# aim is to force the bot to learn rules as well
class Agent:
    # initialization function
    def __init__(self, board_size, epsilon = 0.01, gamma = 0.9,
                 buffer_size = 30000, use_target_net = False):
        assert 0 <= epsilon and epsilon <= 1, "epsilon should be in 0 to 1, got {}".format(epsilon)
        assert 0 <= gamma and gamma <= 1, "gamma should be in 0 to 1, got {}".format(gamma)

        self._board_size = board_size
        self._epsilon = epsilon
        self._gamma = gamma

        self._buffer = ReplayBuffer(buffer_size)
        self._buffer_size = buffer_size

        self._input_shape = (self._board_size, self._board_size, 1)
        self._model_train, self._model_pred = self.agent_model()
        self._use_target_net = use_target_net
        if(use_target_net):
            _, self._target_net = self.agent_model()
            self.update_target_net()

    def get_epsilon(self):
        return self._epsilon

    def set_epsilon(self, epsilon):
        self._epsilon = epsilon

    # get action value
    def get_qvalues(self, move_type, board, model = None):
        # board is assumed to be a list
        if model is None:
            model = self._model_pred
        model_input = np.concatenate([np.array([move_type]), board]).reshape(1, -1)
        q_values = model.predict(model_input)
        return q_values

    # get the action using epsilon greedy policy
    def move(self, move_type, board):
        q_values = self.get_qvalues(move_type, board, self._model_pred)
        action = int(np.argmax(q_values))
        if(np.random.random() <= self._epsilon):
            action = int(np.random.choice(list(range(len(board))), 1)[0])
        return action

    def agent_model(self):
        # move type added to the board itself in the input
        input_board = Input((1 + self._board_size ** 2,))
        input_action = Input((self._board_size ** 2,))
        # total rows + columns + diagonals is total units
        x = Dense(self._board_size ** 2, activation = 'relu')(input_board)
        x = Dense(self._board_size ** 2, activation = 'relu')(x)
        x = Dense(self._board_size ** 2, activation = 'linear', name = 'action_values')(x)
        x = Multiply()([input_action, x])
        out = Lambda(lambda x: K.sum(x, axis = 1), output_shape = (1,))(x)

        model_train = Model(inputs = [input_board, input_action], outputs = out)
        model_train.compile(optimizer = Adam(1e-4), loss = 'mean_squared_error')

        model_pred = Model(inputs = input_board,
                           outputs = model_train.get_layer('action_values').output)

        return model_train, model_pred

    # save the current models, note that all models are saved
    def save_model(self, file_path = '', iteration = None):
        if(iteration is not None):
            assert isinstance(iteration, int), "iteration should be an integer"
        else:
            iteration = 0
        self._model_pred.save("{}/model_{:04d}_prediction.h5".format(file_path, iteration))
        self._model_train.save("{}/model_{:04d}_train.h5".format(file_path, iteration))
        self._target_net.save("{}/model_{:04d}_target.h5".format(file_path, iteration))

    # load any existing models
    def load_model(self, file_path = '', iteration = None):
        if(iteration is not None):
            assert isinstance(iteration, int), "iteration should be an integer"
        else:
            iteration = 0
        try:
            self._model_pred  = load_model("{}/model_{:04d}_prediction.h5".format(file_path, iteration))
            self._model_train = load_model("{}/model_{:04d}_train.h5".format(file_path, iteration))
            self._target_net  = load_model("{}/model_{:04d}_target.h5".format(file_path, iteration))
        except FileNotFoundError:
            print("Couldn't locate models at {}, check provided path".format(file_path))

    def print_model(self):
        print('Training Model')
        print(self._model_train.summary())
        print('Prediction Model')
        print(self._model_pred.summary())
        print('Target Network')
        print(self._target_net.summary())

    # add current game step to the replay buffer
    def add_to_buffer(self, move_type, board, next_board, reward, action, done):
        if(done):
            discounted_reward = reward
        else:
            current_model = self._target_net if self._use_target_net else self._model_pred
            discounted_reward = reward + self._gamma * \
                     np.max(self.get_qvalues(move_type, next_board, current_model))

        # one hot encoding to convert the discounted rewards
        one_hot_action = np.zeros((1, self._board_size ** 2))
        one_hot_action[0, action] = 1

        add_times = 1
        if(done and reward > 0):
            add_times = 10
        for _ in range(add_times):
            self._buffer.add_data([board, move_type,
                            one_hot_action, discounted_reward])

    def reset_buffer(self, buffer_size = None):
        if(buffer_size is not None):
            self._buffer_size = buffer_size
        self._buffer = ReplayBuffer(self._buffer_size)

    def train_agent(self, sample_size = 10000, epochs = 10, verbose = 0):
        X1, X2, y = self._buffer.sample(sample_size)
        self._model_train.fit([X1, X2], y, epochs = epochs, verbose = verbose)
        return self._model_train.evaluate([X1, X2], y)

    # target network outputs is what we try to predict
    # this network is static for a while and serves as "ground truth"
    def update_target_net(self):
        if(self._use_target_net):
            self._target_net.set_weights(self._model_pred.get_weights())

    # to update weights between competing agents
    def copy_weights_from_agent(self, agent_for_copy):
        assert isinstance(agent_for_copy, Agent), "Agent type is required for copy"

        self._model_train.set_weights(agent_for_copy._model_train.get_weights())
        self._target_net.set_weights(agent_for_copy._model_pred.get_weights())
