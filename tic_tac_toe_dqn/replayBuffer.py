from collections import deque
import numpy as np

# a class to keep snapshots for training
class ReplayBuffer():
    # init
    def __init__(self, buffer_size = 100):
        self._buffer = deque(maxlen = buffer_size)

    def add_data(self, data):
        self._buffer.append(data)

    def sample(self, size = None):
        if size is None or not (0 < size and size <= len(self._buffer)):
            size = int(0.1 * len(self._buffer))

        idx = np.random.choice(list(range(len(self._buffer))), size)
        states, nums, actions, discounted_rewards = [], [], [], []
        for i in idx:
            states.append(self._buffer[i][0])
            nums.append(self._buffer[i][1])
            actions.append(self._buffer[i][2])
            discounted_rewards.append(self._buffer[i][3])

        return np.concatenate([np.array(nums).reshape(-1, 1), np.array(states)], axis = 1), \
               np.concatenate(actions, axis = 0), \
               np.array(discounted_rewards)
